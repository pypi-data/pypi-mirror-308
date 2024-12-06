from os import path
from time import time
from math import ceil
import numpy as np
from silx.io.url import DataUrl
from ...utils import remove_items_from_list
from ...resources.logger import LoggerOrPrint
from ...resources.utils import extract_parameters
from ...io.reader import ChunkReader, HDF5Loader
from ...preproc.ccd import Log, CCDFilter
from ...preproc.flatfield import FlatFieldDataUrls
from ...preproc.distortion import DistortionCorrection
from ...preproc.shift import VerticalShift
from ...preproc.double_flatfield import DoubleFlatField
from ...preproc.phase import PaganinPhaseRetrieval
from ...preproc.ctf import CTFPhaseRetrieval, GeoPars
from ...reconstruction.sinogram import SinoNormalization
from ...reconstruction.filtering import SinoFilter
from ...processing.rotation import Rotation
from ...reconstruction.rings import MunchDeringer, SinoMeanDeringer, VoDeringer
from ...processing.unsharp import UnsharpMask
from ...processing.histogram import PartialHistogram, hist_as_2Darray
from ..utils import use_options, pipeline_step, get_subregion
from ..datadump import DataDumpManager
from ..writer import WriterManager
from ..detector_distortion_provider import DetectorDistortionProvider

# For now we don't have a plain python/numpy backend for reconstruction
try:
    from ...reconstruction.fbp_opencl import OpenCLBackprojector as Backprojector
except:
    Backprojector = None


class ChunkedPipeline:
    """
    Pipeline for "regular" full-field tomography.
    Data is processed by chunks. A chunk consists in K contiguous lines of all the radios.
    In parallel geometry, a chunk of K radios lines gives K sinograms,
    and equivalently K reconstructed slices.
    """

    backend = "numpy"
    FlatFieldClass = FlatFieldDataUrls
    DoubleFlatFieldClass = DoubleFlatField
    CCDCorrectionClass = CCDFilter
    PaganinPhaseRetrievalClass = PaganinPhaseRetrieval
    CTFPhaseRetrievalClass = CTFPhaseRetrieval
    UnsharpMaskClass = UnsharpMask
    ImageRotationClass = Rotation
    VerticalShiftClass = VerticalShift
    MunchDeringerClass = MunchDeringer
    SinoMeanDeringerClass = SinoMeanDeringer
    VoDeringerClass = VoDeringer
    MLogClass = Log
    SinoNormalizationClass = SinoNormalization
    SinoFilterClass = SinoFilter
    FBPClass = Backprojector
    ConebeamClass = None  # unsupported on CPU
    HistogramClass = PartialHistogram

    _default_extra_options = {}

    # These steps are skipped if the reconstruction is done in two stages.
    # The first stage will skip these steps, and the second stage will do these stages after merging sinograms.
    _reconstruction_steps = ["sino_rings_correction", "reconstruction", "save", "histogram"]

    def __init__(
        self, process_config, chunk_shape, margin=None, logger=None, use_grouped_mode=False, extra_options=None
    ):
        """
        Initialize a "Chunked" pipeline.

        Parameters
        ----------
        processing_config: `ProcessConfig`
            Process configuration.
        chunk_shape: tuple
            Shape of the chunk of data to process, in the form (n_angles, n_z, n_x).
            It has to account for possible cropping of the data, eg. [:, start_z:end_z, start_x:end_x]
            where start_xz and/or end_xz can be other than None.
        margin: tuple, optional
            Margin to use, in the form ((up, down), (left, right)).
            It is used for example when performing phase retrieval or a convolution-like operation:
            some extra data is kept to avoid boundaries issues.
            These boundaries are then discarded: the data volume is eventually cropped as
            `data[U:D, L:R]` where `((U, D), (L, R)) = margin`
            If not provided, no margin is applied.
        logger: `nabu.app.logger.Logger`, optional
            Logger class
        extra_options: dict, optional
            Advanced extra options.


        Notes
        ------

        Using `margin` results in a lesser number of reconstructed slices.
        More specifically, if `margin = (V, H)`, then there will be `delta_z - 2*V`
        reconstructed slices (if the sub-region is in the middle of the volume)
        or `delta_z - V` reconstructed slices (if the sub-region is on top or bottom
        of the volume).
        """
        self.logger = LoggerOrPrint(logger)
        self._set_params(process_config, chunk_shape, extra_options, margin, use_grouped_mode)
        self._init_pipeline()

    def _set_params(self, process_config, chunk_shape, extra_options, margin, use_grouped_mode):
        self.process_config = process_config
        self.dataset_info = self.process_config.dataset_info
        self.processing_steps = self.process_config.processing_steps.copy()
        self.processing_options = self.process_config.processing_options
        self._set_chunk_shape(chunk_shape, use_grouped_mode)
        self.set_subregion(None)
        self._set_margin(margin)
        self._set_extra_options(extra_options)
        self._callbacks = {}
        self._steps_name2component = {}
        self._steps_component2name = {}

    def _set_chunk_shape(self, chunk_shape, use_grouped_mode):
        if len(chunk_shape) != 3:
            raise ValueError("Expected chunk_shape to be a tuple of length 3 in the form (n_z, n_y, n_x)")
        self.chunk_shape = tuple(int(c) for c in chunk_shape)  # cast to int, as numpy.int64 can make pycuda crash
        # TODO: sanity check (eg. compare to size of radios in dataset_info) ?
        # (n_a, n_z, n_x)
        self.radios_shape = (
            ceil(self.chunk_shape[0] / self.process_config.subsampling_factor),
            self.chunk_shape[1] // self.process_config.binning[1],
            self.chunk_shape[2] // self.process_config.binning[0],
        )
        self.n_angles = self.radios_shape[0]
        self.n_slices = self.radios_shape[1]
        self._grouped_processing = False
        if use_grouped_mode or self.chunk_shape[0] < len(self.process_config.rotation_angles(subsampling=False)):
            # TODO allow a certain tolerance in this case ?
            # Reconstruction is still possible (albeit less accurate) if delta is small
            self._grouped_processing = True
            self.logger.debug("Only a subset of angles is processed - Reconstruction will be skipped")
            self.processing_steps, _ = remove_items_from_list(self.processing_steps, self._reconstruction_steps)

    def _set_margin(self, margin):
        if margin is None:
            U, D, L, R = None, None, None, None
        else:
            ((U, D), (L, R)) = get_subregion(margin, ndim=2)

        # Replace "None" with zeros
        U, D, L, R = U or 0, D or 0, L or 0, R or 0

        self.margin = ((U, D), (L, R))
        self._margin_up = U
        self._margin_down = D
        self._margin_left = L
        self._margin_right = R
        self.use_margin = (U + D + L + R) > 0
        self.n_recs = self.chunk_shape[1] - sum(self.margin[0])
        self.radios_cropped_shape = (self.radios_shape[0], self.radios_shape[1] - U - D, self.radios_shape[2] - L - R)
        if self.use_margin:
            self.n_slices -= sum(self.margin[0])

    def set_subregion(self, sub_region):
        """
        Set the data volume sub-region to process.
        Note that processing margin, if any, is contained within the sub-region.

        Parameters
        -----------
        sub_region: tuple
            Data volume sub-region, in the form ((start_a, end_a), (start_z, end_z), (start_x, end_x))
            where the data volume has a layout (angles, Z, X)
        """
        n_angles = self.dataset_info.n_angles
        n_x, n_z = self.dataset_info.radio_dims
        c_a, c_z, c_x = self.chunk_shape
        if sub_region is None:
            # By default, take the sub-region around central slice
            sub_region = (
                (0, c_a),
                (n_z // 2 - c_z // 2, n_z // 2 - c_z // 2 + c_z),
                (n_x // 2 - c_x // 2, n_x // 2 - c_x // 2 + c_x),
            )
        else:
            sub_region = get_subregion(sub_region, ndim=3)
            # check sub-region
            for i, start_end in enumerate(sub_region):
                start, end = start_end
                if start is not None and end is not None:
                    if end - start != self.chunk_shape[i]:
                        raise ValueError(
                            "Invalid (start, end)=(%d, %d) for sub-region (dimension %d): chunk shape is %s, but %d-%d=%d != %d"
                            % (start, end, i, str(self.chunk_shape), end, start, end - start, self.chunk_shape[i])
                        )
            #
        self.logger.debug("Set sub-region to %s" % (str(sub_region)))
        self.sub_region = sub_region
        self._sub_region_xz = sub_region[2] + sub_region[1]

    def _set_extra_options(self, extra_options):
        self.extra_options = self._default_extra_options.copy()
        self.extra_options.update(extra_options or {})

    #
    # Callbacks
    #

    def register_callback(self, step_name, callback):
        """
        Register a callback for a pipeline processing step.

        Parameters
        ----------
        step_name: str
            processing step name
        callback: callable
            A function. It will be executed once the processing step `step_name`
            is finished. The function takes only one argument: the class instance.
        """
        if step_name not in self.processing_steps:
            raise ValueError("'%s' is not in processing steps %s" % (step_name, self.processing_steps))
        if step_name in self._callbacks:
            self._callbacks[step_name].append(callback)
        else:
            self._callbacks[step_name] = [callback]

    #
    # Memory management
    #

    def _allocate_array(self, shape, dtype, name=None):
        return np.zeros(shape, dtype=dtype)

    def _allocate_recs(self, ny, nx, n_slices=None):
        n_slices = n_slices or self.n_slices
        self.recs = self._allocate_array((n_slices, ny, nx), "f", name="recs")

    #
    # Runtime attributes
    #

    @property
    def sub_region_xz(self):
        """
        Return the currently processed sub-region in the form
        (start_x, end_x, start_z, end_z)
        """
        return self._sub_region_xz

    @property
    def z_min(self):
        return self._sub_region_xz[2]

    @property
    def sino_shape(self):
        return self.process_config.sino_shape(binning=True, subsampling=True)

    @property
    def sinos_shape(self):
        return (self.n_slices,) + self.sino_shape

    def get_slice_start_index(self):
        return self.z_min + self._margin_up

    #
    # Pipeline initialization
    #

    def _init_pipeline(self):
        self._allocate_radios()
        self._init_data_dump()
        self._init_reader()
        self._init_flatfield()
        self._init_double_flatfield()
        self._init_ccd_corrections()
        self._init_radios_rotation()
        self._init_phase()
        self._init_unsharp()
        self._init_radios_movements()
        self._init_mlog()
        self._init_sino_normalization()
        self._init_sino_rings_correction()
        self._init_reconstruction()
        self._init_histogram()
        self._init_writer()

    def _allocate_radios(self):
        self.radios = np.zeros(self.radios_shape, dtype=np.float32)
        self.data = self.radios  # alias

    def _init_data_dump(self):
        self._resume_from_step = self.processing_options["read_chunk"].get("step_name", None)
        self.datadump_manager = DataDumpManager(
            self.process_config, self.sub_region, margin=self.margin, logger=self.logger
        )
        # When using "grouped processing", sinogram has to be dumped.
        # If it was not specified by user, force sinogram dump
        # Perhaps these lines should be moved directly to DataDumpManager.
        if self._grouped_processing and not self.process_config.dump_sinogram:
            sino_dump_fname = self.process_config.get_save_steps_file("sinogram")
            self.datadump_manager._configure_dump("sinogram", force_dump_to_fname=sino_dump_fname)
            self.logger.debug("Will dump sinogram to %s" % self.datadump_manager.data_dump["sinogram"].fname)

    @use_options("read_chunk", "chunk_reader")
    def _init_reader(self):
        options = self.processing_options["read_chunk"]
        self._update_reader_configuration()

        process_file = options.get("process_file", None)
        if process_file is None:
            # Standard case - start pipeline from raw data
            if self.process_config.nabu_config["preproc"]["detector_distortion_correction"] is None:
                self.detector_corrector = None
            else:
                self.detector_corrector = DetectorDistortionProvider(
                    detector_full_shape_vh=self.process_config.dataset_info.radio_dims[::-1],
                    correction_type=self.process_config.nabu_config["preproc"]["detector_distortion_correction"],
                    options=self.process_config.nabu_config["preproc"]["detector_distortion_correction_options"],
                )
            # ChunkReader always take a non-subsampled dictionary "files".
            self.chunk_reader = ChunkReader(
                self._read_options["files"],
                sub_region=self.sub_region_xz,
                data_buffer=self.radios,
                pre_allocate=False,
                detector_corrector=self.detector_corrector,
                convert_float=True,
                binning=options["binning"],
                dataset_subsampling=options["dataset_subsampling"],
            )
        else:
            # Resume pipeline from dumped intermediate step
            self.chunk_reader = HDF5Loader(
                process_file,
                options["process_h5_path"],
                sub_region=self.datadump_manager.get_read_dump_subregion(),
                data_buffer=self.radios,
                pre_allocate=False,
            )
            self._resume_from_step = options["step_name"]
            self.logger.debug(
                "Load subregion %s from file %s" % (str(self.chunk_reader.sub_region), self.chunk_reader.fname)
            )

    def _update_reader_configuration(self):
        """
        Modify self.processing_options["read_chunk"] to select a subset of the files, if needed
        (i.e when processing only a subset of the images stack)
        """
        self._read_options = self.processing_options["read_chunk"].copy()
        if self.n_angles == self.process_config.n_angles(subsampling=True):
            # Nothing to do if the full angular range is processed in one shot
            return
        if self._resume_from_step is not None:
            if self._resume_from_step == "sinogram":
                msg = "It makes no sense to use 'grouped processing' when resuming from sinogram"
                self.logger.fatal(msg)
                raise ValueError(msg)
            # Nothing to do if we resume the processing from a given step
            return
        input_data_files = {}
        files_indices = sorted(self._read_options["files"].keys())
        angle_idx_start, angle_idx_end = self.sub_region[0]
        for i in range(angle_idx_start, angle_idx_end):
            idx = files_indices[i]
            input_data_files[idx] = self._read_options["files"][idx]
        self._read_options["files"] = input_data_files

    @use_options("flatfield", "flatfield")
    def _init_flatfield(self):
        self._ff_options = self.processing_options["flatfield"].copy()
        # Use chunk_reader.files instead of process_config.projs_indices(subsampling=True), because
        # chunk_reader might read only a subset of the files (in "grouped mode")
        self._ff_options["projs_indices"] = list(self.chunk_reader.files_subsampled.keys())
        if self._ff_options.get("normalize_srcurrent", False):
            a_start_idx, a_end_idx = self.sub_region[0]
            subs = self.process_config.subsampling_factor
            self._ff_options["radios_srcurrent"] = self._ff_options["radios_srcurrent"][a_start_idx:a_end_idx:subs]

        distortion_correction = None
        if self._ff_options["do_flat_distortion"]:
            self.logger.info("Flats distortion correction will be applied")
            self.FlatFieldClass = FlatFieldDataUrls  # no GPU implementation available, force this backend
            estimation_kwargs = {}
            estimation_kwargs.update(self._ff_options["flat_distortion_params"])
            estimation_kwargs["logger"] = self.logger
            distortion_correction = DistortionCorrection(
                estimation_method="fft-correlation", estimation_kwargs=estimation_kwargs, correction_method="interpn"
            )

        # FlatField parameter "radios_indices" must account for subsampling
        self.flatfield = self.FlatFieldClass(
            self.radios_shape,
            flats=self.dataset_info.flats,
            darks=self.dataset_info.darks,
            radios_indices=self._ff_options["projs_indices"],
            interpolation="linear",
            distortion_correction=distortion_correction,
            sub_region=self.sub_region_xz,
            detector_corrector=self.detector_corrector,
            binning=self._ff_options["binning"],
            radios_srcurrent=self._ff_options["radios_srcurrent"],
            flats_srcurrent=self._ff_options["flats_srcurrent"],
            convert_float=True,
        )

    @use_options("double_flatfield", "double_flatfield")
    def _init_double_flatfield(self):
        options = self.processing_options["double_flatfield"]
        avg_is_on_log = options["sigma"] is not None
        result_url = None
        if options["processes_file"] not in (None, ""):
            result_url = DataUrl(
                file_path=options["processes_file"],
                data_path=(self.dataset_info.hdf5_entry or "entry") + "/double_flatfield/results/data",
            )
            self.logger.info("Loading double flatfield from %s" % result_url.file_path())
        if (self.n_angles < self.process_config.n_angles(subsampling=True)) and result_url is None:
            raise ValueError(
                "Cannot use double-flatfield when processing subset of radios. Please use the 'nabu-double-flatfield' command"
            )
        self.double_flatfield = self.DoubleFlatFieldClass(
            self.radios_shape,
            result_url=result_url,
            sub_region=self.sub_region_xz,
            detector_corrector=self.detector_corrector,
            input_is_mlog=False,
            output_is_mlog=False,
            average_is_on_log=avg_is_on_log,
            sigma_filter=options["sigma"],
            log_clip_min=options["log_min_clip"],
            log_clip_max=options["log_max_clip"],
        )

    @use_options("ccd_correction", "ccd_correction")
    def _init_ccd_corrections(self):
        options = self.processing_options["ccd_correction"]
        self.ccd_correction = self.CCDCorrectionClass(
            self.radios_shape[1:], median_clip_thresh=options["median_clip_thresh"]
        )

    @use_options("rotate_projections", "projs_rot")
    def _init_radios_rotation(self):
        options = self.processing_options["rotate_projections"]
        center = options["center"]
        if center is None:
            nx, ny = self.radios_shape[1:][::-1]  # after binning
            center = (nx / 2 - 0.5, ny / 2 - 0.5)
        center = (center[0], center[1] - self.z_min)
        self.projs_rot = self.ImageRotationClass(
            self.radios_shape[1:], options["angle"], center=center, mode="edge", reshape=False
        )
        self._tmp_rotated_radio = self._allocate_array(self.radios_shape[1:], "f", name="tmp_rotated_radio")

    @use_options("radios_movements", "radios_movements")
    def _init_radios_movements(self):
        options = self.processing_options["radios_movements"]
        self._vertical_shifts = options["translation_movements"][:, 1]
        self.radios_movements = self.VerticalShiftClass(self.radios.shape, self._vertical_shifts)

    @use_options("phase", "phase_retrieval")
    def _init_phase(self):
        options = self.processing_options["phase"]
        if options["method"] == "CTF":
            translations_vh = getattr(self.dataset_info, "ctf_translations", None)
            geo_pars_params = options["ctf_geo_pars"].copy()
            geo_pars_params["logger"] = self.logger
            geo_pars = GeoPars(**geo_pars_params)
            self.phase_retrieval = self.CTFPhaseRetrievalClass(
                self.radios_shape[1:],
                geo_pars,
                options["delta_beta"],
                lim1=options["ctf_lim1"],
                lim2=options["ctf_lim2"],
                logger=self.logger,
                fft_num_threads=None,  # TODO tune in advanced params of nabu config file
                use_rfft=True,
                normalize_by_mean=options["ctf_normalize_by_mean"],
                translation_vh=translations_vh,
            )
        else:
            self.phase_retrieval = self.PaganinPhaseRetrievalClass(
                self.radios_shape[1:],
                distance=options["distance_m"],
                energy=options["energy_kev"],
                delta_beta=options["delta_beta"],
                pixel_size=options["pixel_size_m"],
                padding=options["padding_type"],
                # TODO tune in advanced params of nabu config file
                fft_num_threads=None,
            )

    @use_options("unsharp_mask", "unsharp_mask")
    def _init_unsharp(self):
        options = self.processing_options["unsharp_mask"]
        self.unsharp_mask = self.UnsharpMaskClass(
            self.radios_shape[1:],
            options["unsharp_sigma"],
            options["unsharp_coeff"],
            mode="reflect",
            method=options["unsharp_method"],
        )

    @use_options("take_log", "mlog")
    def _init_mlog(self):
        options = self.processing_options["take_log"]
        self.mlog = self.MLogClass(
            self.radios_shape, clip_min=options["log_min_clip"], clip_max=options["log_max_clip"]
        )

    @use_options("sino_normalization", "sino_normalization")
    def _init_sino_normalization(self):
        options = self.processing_options["sino_normalization"]
        self.sino_normalization = self.SinoNormalizationClass(
            kind=options["method"],
            radios_shape=self.radios_cropped_shape,
            normalization_array=options["normalization_array"],
        )

    @use_options("sino_rings_correction", "sino_deringer")
    def _init_sino_rings_correction(self):
        n_a, n_z, n_x = self.radios_cropped_shape
        sinos_shape = (n_z, n_a, n_x)
        options = self.processing_options["sino_rings_correction"]

        destriper_params = extract_parameters(options["user_options"])
        if options["method"] == "munch":
            # TODO MunchDeringer does not have an API consistent with the other deringers
            fw_sigma = destriper_params.pop("sigma", 1.0)
            self.sino_deringer = self.MunchDeringerClass(fw_sigma, sinos_shape, **destriper_params)
        elif options["method"] == "vo":
            self.sino_deringer = self.VoDeringerClass(sinos_shape, **destriper_params)
        elif options["method"] == "mean-subtraction":
            self.sino_deringer = self.SinoMeanDeringerClass(
                sinos_shape, mode="subtract", fft_num_threads=None, **destriper_params
            )
        elif options["method"] == "mean-division":
            self.sino_deringer = self.SinoMeanDeringerClass(
                sinos_shape, mode="divide", fft_num_threads=None, **destriper_params
            )

    @use_options("reconstruction", "reconstruction")
    def _init_reconstruction(self):
        options = self.processing_options["reconstruction"]
        if options["method"] == "FBP" and self.FBPClass is None:
            raise ValueError("No usable FBP module was found")
        if options["method"] == "cone" and self.ConebeamClass is None:
            raise ValueError("No usable cone-beam module was found")

        if options["method"] == "FBP":
            n_slices = self.n_slices
            self.reconstruction = self.FBPClass(
                self.sinos_shape[1:],
                angles=options["angles"],
                rot_center=options["rotation_axis_position"],
                filter_name=options["fbp_filter_type"] or "none",
                halftomo=options["enable_halftomo"],
                slice_roi=self.process_config.rec_roi,
                padding_mode=options["padding_type"],
                extra_options={
                    "scale_factor": 1.0 / options["voxel_size_cm"][0],
                    "axis_correction": options["axis_correction"],
                    "centered_axis": options["centered_axis"],
                    "clip_outer_circle": options["clip_outer_circle"],
                    "filter_cutoff": options["fbp_filter_cutoff"],
                },
            )

        if options["method"] == "cone":
            n_slices = self.n_slices + sum(self.margin[0])
            # For numerical stability, normalize all lengths with respect to detector pixel size
            pixel_size_m = self.dataset_info.pixel_size * 1e-6
            source_sample_dist = options["source_sample_dist"] / pixel_size_m
            sample_detector_dist = options["sample_detector_dist"] / pixel_size_m
            self.reconstruction = self.ConebeamClass(  # pylint: disable=E1102
                (self.radios_shape[1],) + self.sino_shape,
                source_sample_dist,
                sample_detector_dist,
                angles=-options["angles"],
                rot_center=options["rotation_axis_position"],
                axis_correction=(-options["axis_correction"] if options["axis_correction"] is not None else None),
                pixel_size=1,
                scale_factor=1.0 / options["voxel_size_cm"][0],
                padding_mode=options["padding_type"],
                slice_roi=self.process_config.rec_roi,
            )

        self._allocate_recs(*self.process_config.rec_shape, n_slices=n_slices)
        n_a, _, n_x = self.radios_cropped_shape
        self._tmp_sino = self._allocate_array((n_a, n_x), "f", name="tmp_sino")

    @use_options("histogram", "histogram")
    def _init_histogram(self):
        options = self.processing_options["histogram"]
        self.histogram = self.HistogramClass(method="fixed_bins_number", num_bins=options["histogram_bins"])

    @use_options("save", "writer")
    def _init_writer(self, **extra_options):
        options = self.processing_options["save"]
        metadata = {
            "process_name": "reconstruction",
            "processing_index": 0,
            # TODO this one takes too much time to write, not useful for partial files
            # "processing_options": self.processing_options,
            #
            "nabu_config": self.process_config.nabu_config,
            "entry": getattr(self.dataset_info.dataset_scanner, "entry", "entry"),
        }
        writer_extra_options = {
            "jpeg2000_compression_ratio": options["jpeg2000_compression_ratio"],
            "float_clip_values": options["float_clip_values"],
            "tiff_single_file": options.get("tiff_single_file", False),
            "single_output_file_initialized": getattr(self.process_config, "single_output_file_initialized", False),
            "raw_vol_metadata": {"voxelSize": self.dataset_info.pixel_size},  # legacy...
        }
        writer_extra_options.update(extra_options)
        self.writer = WriterManager(
            options["location"],
            options["file_prefix"],
            file_format=options["file_format"],
            overwrite=options["overwrite"],
            start_index=self.get_slice_start_index(),
            logger=self.logger,
            metadata=metadata,
            histogram=("histogram" in self.processing_steps),
            extra_options=writer_extra_options,
        )

    #
    # Pipeline execution
    #

    @pipeline_step("chunk_reader", "Reading data")
    def _read_data(self):
        self.logger.debug("Region = %s" % str(self.sub_region))
        t0 = time()
        self.chunk_reader.load_data()
        el = time() - t0
        shp = self.chunk_reader.data.shape
        self.logger.info("Read subvolume %s in %.2f s" % (str(shp), el))

    @pipeline_step("flatfield", "Applying flat-field")
    def _flatfield(self):
        self.flatfield.normalize_radios(self.radios)

    @pipeline_step("double_flatfield", "Applying double flat-field")
    def _double_flatfield(self, radios=None):
        if radios is None:
            radios = self.radios
        self.double_flatfield.apply_double_flatfield(radios)

    @pipeline_step("ccd_correction", "Applying CCD corrections")
    def _ccd_corrections(self, radios=None):
        if radios is None:
            radios = self.radios
        _tmp_radio = self._allocate_array(radios.shape[1:], "f", name="tmp_ccdcorr_radio")
        for i in range(radios.shape[0]):
            self.ccd_correction.median_clip_correction(radios[i], output=_tmp_radio)
            radios[i][:] = _tmp_radio[:]

    @pipeline_step("projs_rot", "Rotating projections")
    def _rotate_projections(self, radios=None):
        if radios is None:
            radios = self.radios
        tmp_radio = self._tmp_rotated_radio
        for i in range(radios.shape[0]):
            self.projs_rot.rotate(radios[i], output=tmp_radio)
            radios[i][:] = tmp_radio[:]

    @pipeline_step("phase_retrieval", "Performing phase retrieval")
    def _retrieve_phase(self):
        for i in range(self.radios.shape[0]):
            self.phase_retrieval.retrieve_phase(self.radios[i], output=self.radios[i])

    @pipeline_step("unsharp_mask", "Performing unsharp mask")
    def _apply_unsharp(self):
        for i in range(self.radios.shape[0]):
            self.radios[i] = self.unsharp_mask.unsharp(self.radios[i])

    @pipeline_step("mlog", "Taking logarithm")
    def _take_log(self):
        self.mlog.take_logarithm(self.radios)

    @pipeline_step("radios_movements", "Applying radios movements")
    def _radios_movements(self, radios=None):
        if radios is None:
            radios = self.radios
        self.radios_movements.apply_vertical_shifts(radios, list(range(radios.shape[0])))

    def _crop_radios(self):
        if self.use_margin:
            self._orig_radios = self.radios
            if self.processing_options.get("reconstruction", {}).get("method", None) == "cone":
                return
            ((U, D), (L, R)) = self.margin
            self.logger.debug(
                "Cropping radios from %s to %s" % (str(self.radios_shape), str(self.radios_cropped_shape))
            )
            U, D, L, R = U or None, -D or None, L or None, -R or None
            self.radios = self.radios[:, U:D, L:R]  # view

    @pipeline_step("sino_normalization", "Normalizing sinograms")
    def _normalize_sinos(self, radios=None):
        if radios is None:
            radios = self.radios
        sinos = radios.transpose((1, 0, 2))
        self.sino_normalization.normalize(sinos)

    def _dump_sinogram(self):
        if self.datadump_manager is not None:
            self.datadump_manager.dump_data_to_file("sinogram", self.radios)

    @pipeline_step("sino_deringer", "Removing rings on sinograms")
    def _destripe_sinos(self):
        sinos = np.rollaxis(self.radios, 1, 0)  # view
        self.sino_deringer.remove_rings(sinos)  # TODO check it works with non-contiguous view

    @pipeline_step("reconstruction", "Reconstruction")
    def _reconstruct(self):
        """
        Reconstruction for parallel geometry.
        For each target slice: get the corresponding sinogram, apply some processing, then reconstruct
        """
        options = self.processing_options["reconstruction"]
        if options["method"] == "cone":
            self._reconstruct_cone()
            return

        for i in range(self.n_slices):
            self._tmp_sino[:] = self.radios[:, i, :]  # copy into contiguous array
            self.reconstruction.fbp(self._tmp_sino, output=self.recs[i])

    def _reconstruct_cone(self):
        """
        This reconstructs the entire sinograms stack at once
        """

        n_angles, n_z, n_x = self.radios.shape

        # FIXME
        # can't do a discontiguous single copy...
        sinos_contig = self._allocate_array((n_z, n_angles, n_x), np.float32, "sinos_cone")
        for i in range(n_z):
            sinos_contig[i] = self.radios[:, i, :]
        # ---

        # In principle radios are not cropped at this stage,
        # so self.sub_region[2][0] can be used instead of self.get_slice_start_index() instead of self.sub_region[2][0]
        z_min, z_max = self.sub_region_xz[2:]
        n_z_tot = self.process_config.radio_shape(binning=True)[0]

        self.reconstruction.reconstruct(  # pylint: disable=E1101
            sinos_contig,
            output=self.recs,
            relative_z_position=((z_min + z_max) / self.process_config.binning_z / 2) - n_z_tot / 2,
        )

    @pipeline_step("histogram", "Computing histogram")
    def _compute_histogram(self, data=None):
        if data is None:
            data = self.recs
        self.recs_histogram = self.histogram.compute_histogram(data)

    @pipeline_step("writer", "Saving data")
    def _write_data(self, data=None):
        if data is None and self.reconstruction is not None:
            data = self.recs
        if data is None:
            self.logger.info("No data to write")
            return
        self.writer.write_data(data)
        self.logger.info("Wrote %s" % self.writer.fname)
        self._write_histogram()
        self.process_config.single_output_file_initialized = True

    def _write_histogram(self):
        if "histogram" not in self.processing_steps:
            return
        self.logger.info("Saving histogram")
        self.writer.write_histogram(
            hist_as_2Darray(self.recs_histogram),
            processing_index=1,
            config={
                "file": path.basename(self.writer.fname),
                "bins": self.processing_options["histogram"]["histogram_bins"],
            },
        )

    def _process_finalize(self):
        if self.use_margin:
            self.radios = self._orig_radios

    def __repr__(self):
        res = "%s(%s, margin=%s)" % (self.__class__.__name__, str(self.chunk_shape), str(self.margin))
        binning = self.process_config.binning
        subsampling = self.process_config.subsampling_factor

        if binning != (1, 1) or subsampling > 1:
            if binning != (1, 1):
                res += "\nImages binning: %s" % (str(binning))
            if subsampling:
                res += "\nAngles subsampling: %d" % subsampling
            res += "\nRadios chunk: %s ---> %s" % (self.chunk_shape, self.radios_shape)

        if self.use_margin:
            res += "\nMargin: %s" % (str(self.margin))
            res += "\nRadios chunk: %s ---> %s" % (str(self.radios_shape), str(self.radios_cropped_shape))

        res += "\nCurrent subregion: %s" % (str(self.sub_region))
        for step_name in self.processing_steps:
            res += "\n- %s" % (step_name)
        return res

    def _process_chunk(self):
        self._flatfield()
        self._double_flatfield()
        self._ccd_corrections()
        self._rotate_projections()
        self._retrieve_phase()
        self._apply_unsharp()
        self._take_log()
        self._radios_movements()
        self._crop_radios()
        self._normalize_sinos()
        self._destripe_sinos()
        self._dump_sinogram()
        self._reconstruct()
        self._compute_histogram()
        self._write_data()
        self._process_finalize()

    def _reset_reader_subregion(self):
        if self._resume_from_step is None:
            # Normal mode - read data from raw radios
            self.chunk_reader._set_subregion(self.sub_region_xz)
            self.chunk_reader._init_reader()
            self.chunk_reader._loaded = False
        else:
            # Resume from a checkpoint. In this case, we have to re-initialize "datadump manager"
            # sooner to configure start_xyz, end_xyz
            self._init_data_dump()
            self.chunk_reader._set_subregion(self.datadump_manager.get_read_dump_subregion())
            self.chunk_reader._loaded = False
        if self._grouped_processing:
            self._update_reader_configuration()
            self.chunk_reader._set_files(self._read_options["files"])

    def _reset_sub_region(self, sub_region):
        self.set_subregion(sub_region)
        # When sub_region is changed, all components involving files reading have to be updated
        self._reset_reader_subregion()
        self._init_flatfield()  # reset flatfield
        self._init_writer()
        self._init_double_flatfield()
        self._init_data_dump()

    def process_chunk(self, sub_region):
        self._reset_sub_region(sub_region)
        self._read_data()
        self._process_chunk()
