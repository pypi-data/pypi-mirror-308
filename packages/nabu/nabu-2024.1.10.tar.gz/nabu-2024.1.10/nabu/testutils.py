from itertools import product
import tarfile
import os
import numpy as np
from scipy.signal.windows import gaussian
from silx.resources import ExternalResources
from silx.io.dictdump import dicttoh5, nxtodict, dicttonx
from silx.io.url import DataUrl
from tomoscan.io import HDF5File
from .io.utils import get_compacted_dataslices

utilstest = ExternalResources(
    project="nabu", url_base="http://www.silx.org/pub/nabu/data/", env_key="NABU_DATA", timeout=60
)

__big_testdata_dir__ = os.environ.get("NABU_BIGDATA_DIR")
if __big_testdata_dir__ is None or not (os.path.isdir(__big_testdata_dir__)):
    __big_testdata_dir__ = None

__do_long_tests__ = os.environ.get("NABU_LONG_TESTS", False)
if __do_long_tests__:
    try:
        __do_long_tests__ = bool(int(__do_long_tests__))
    except:
        __do_long_tests__ = False

__do_large_mem_tests__ = os.environ.get("NABU_LARGE_MEM_TESTS", False)
if __do_large_mem_tests__:
    try:
        __do_large_mem_tests__ = bool(int(__do_large_mem_tests__))
    except:
        __do_large_mem_tests__ = False


def generate_tests_scenarios(configurations):
    """
    Generate "scenarios" of tests.

    The parameter is a dictionary where:
      - the key is the name of a parameter
      - the value is a list of possible parameters

    This function returns a list of dictionary where:
      - the key is the name of a parameter
      - the value is one value of this parameter
    """
    scenarios = [{key: val for key, val in zip(configurations.keys(), p_)} for p_ in product(*configurations.values())]
    return scenarios


def get_data(*dataset_path):
    """
    Get a dataset file from silx.org/pub/nabu/data
    dataset_args is a list describing a nested folder structures, ex.
    ["path", "to", "my", "dataset.h5"]
    """
    dataset_relpath = os.path.join(*dataset_path)
    dataset_downloaded_path = utilstest.getfile(dataset_relpath)
    return np.load(dataset_downloaded_path)


def get_array_of_given_shape(img, shape, dtype):
    """
    From a given image, returns an array of the wanted shape and dtype.
    """

    # Tile image until it's big enough.
    # "fun" fact: using any(blabla) crashes but using any([blabla]) does not, because of variables re-evaluation
    while any([i_dim <= s_dim for i_dim, s_dim in zip(img.shape, shape)]):
        img = np.tile(img, (2, 2))
    if len(shape) == 1:
        arr = img[: shape[0], 0]
    elif len(shape) == 2:
        arr = img[: shape[0], : shape[1]]
    else:
        arr = np.tile(img, (shape[0], 1, 1))[: shape[0], : shape[1], : shape[2]]
    return np.ascontiguousarray(np.squeeze(arr), dtype=dtype)


def get_big_data(filename):
    if __big_testdata_dir__ is None:
        return None
    return np.load(os.path.join(__big_testdata_dir__, filename))


def uncompress_file(compressed_file_path, target_directory):
    with tarfile.open(compressed_file_path) as f:
        f.extractall(path=target_directory)


def get_file(fname):
    downloaded_file = dataset_downloaded_path = utilstest.getfile(fname)
    if ".tar" in fname:
        uncompress_file(downloaded_file, os.path.dirname(downloaded_file))
        downloaded_file = downloaded_file.split(".tar")[0]
    return downloaded_file


def compare_arrays(arr1, arr2, tol, diff=None, absolute_value=True, percent=None, method="max", return_residual=False):
    """
    Utility to compare two arrays.

    Parameters
    ----------
    arr1: numpy.ndarray
        First array to compare
    arr2: numpy.ndarray
        Second array to compare
    tol: float
        Tolerance indicating whether arrays are close to eachother.
    diff: numpy.ndarray, optional
        Difference `arr1 - arr2`. If provided, this array is taken instead of `arr1`
        and `arr2`.
    absolute_value: bool, optional
        Whether to take absolute value of the difference.
    percent: float
        If set, a "relative" comparison is performed instead of a subtraction:
        `red(|arr1 - arr2|) / (red(|arr1|) * percent) < tol`
        where "red" is the reduction method (mean, max or median).
    method:
        Reduction method. Can be "max", "mean", or "median".

    Returns
    --------
    (is_close, residual) if return_residual is set to True
    is_close otherwise

    Examples
    --------
    When using method="mean" and absolute_value=True, this function computes
    the Mean Absolute Difference (MAD) metric.
    When also using percent=1.0, this computes the Relative Mean Absolute Difference
    (RMD) metric.
    """
    reductions = {
        "max": np.max,
        "mean": np.mean,
        "median": np.median,
    }
    if method not in reductions:
        raise ValueError("reduction method should be in %s" % str(list(reductions.keys())))
    if diff is None:
        diff = arr1 - arr2
    if absolute_value is not None:
        diff = np.abs(diff)
    residual = reductions[method](diff)
    if percent is not None:
        a1 = np.abs(arr1) if absolute_value else arr1
        residual /= reductions[method](a1)

    res = residual < tol
    if return_residual:
        res = res, residual
    return res


def gaussian_apodization_window(shape, fwhm_ratio=0.7):
    fwhm = fwhm_ratio * np.array(shape)
    sigma = fwhm / 2.355
    return np.outer(*[gaussian(n, s) for n, s in zip(shape, sigma)])


def compare_shifted_images(img1, img2, fwhm_ratio=0.7, return_upper_bound=False):
    """
    Compare two images that are slightly shifted from one another.
    Typically, tomography reconstruction wight slightly different CoR.
    Each image is Fourier-transformed, and the modulus is taken to get rid of the shift between the images.
    An apodization is done to filter the high frequencies that are usually less relevant.

    Parameters
    ----------
    img1: numpy.ndarray
        First image
    img2: numpy.ndarray
        Second image
    fwhm_ratio: float, optional
        Ratio defining the apodization in the frequency domain.
        A small value (eg. 0.2) means that essentually only the low frequencies will be compared.
        A value of 1.0 means no apodization
    return_upper_bound: bool, optional
        Whether to return a (coarse) upper bound of the comparison metric

    Notes
    -----
    This function roughly computes
        |phi(F(img1)) - phi(F(img2))|
    where F is the absolute value of the Fourier transform, and phi some shrinking function (here arcsinh).
    """

    def _fourier_transform(img):
        return np.arcsinh(np.abs(np.fft.fftshift(np.fft.fft2(img))))

    diff = _fourier_transform(img1) - _fourier_transform(img2)
    diff *= gaussian_apodization_window(img1.shape, fwhm_ratio=fwhm_ratio)
    res = np.abs(diff).max()
    if return_upper_bound:
        data_range = np.max(np.abs(img1))
        return res, np.arcsinh(np.prod(img1.shape) * data_range)
    else:
        return res


class SimpleHDF5TomoScanMock:
    def __init__(self, image_key):
        self._image_key = image_key

    @property
    def image_key(self):
        return self._image_key

    @image_key.setter
    def image_key(self, image_key):
        self._image_key = image_key

    def save_reduced_flats(self, *args, **kwargs):
        pass

    def save_reduced_darks(self, *args, **kwargs):
        pass


class NXDatasetMock:
    """
    An alternative to tomoscan.esrf.mock.MockHDF5, with a different interface.
    Attributes are not supported !
    """

    def __init__(self, data_volume, image_keys, rotation_angles=None, incident_energy=19.0, other_params=None):
        self.data_volume = data_volume
        self.n_proj = data_volume.shape[0]
        self.image_key = image_keys
        if rotation_angles is None:
            rotation_angles = np.linspace(0, 180, self.n_proj, False)
        self.rotation_angle = rotation_angles
        self.incident_energy = incident_energy
        assert image_keys.size == self.n_proj
        self._finalize_init(other_params)
        self.dataset_dict = None
        self.fname = None
        # Mocks more attributes
        self.dataset_scanner = SimpleHDF5TomoScanMock(image_key=self.image_key)
        self.kind = "hdf5"

    def _finalize_init(self, other_params):
        if other_params is None:
            other_params = {}
        default_params = {
            "detector": {
                "count_time": 0.05 * np.ones(self.n_proj, dtype="f"),
                "distance": 0.5,
                "field_of_view": "Full",
                "image_key_control": np.copy(self.image_key),
                "x_pixel_size": 6.5e-6,
                "y_pixel_size": 6.5e-6,
                "x_magnified_pixel_size": 6.5e-5,
                "y_magnified_pixel_size": 6.5e-5,
            },
            "sample": {
                "name": "dummy sample",
                "x_translation": 5e-4 * np.ones(self.n_proj, dtype="f"),
                "y_translation": 5e-4 * np.ones(self.n_proj, dtype="f"),
                "z_translation": 5e-4 * np.ones(self.n_proj, dtype="f"),
            },
        }
        default_params.update(other_params)
        self.other_params = default_params

    def generate_dict(self):
        beam_group = {
            "incident_energy": self.incident_energy,
        }
        detector_other_params = self.other_params["detector"]
        detector_group = {
            "count_time": detector_other_params["count_time"],
            "data": self.data_volume,
            "distance": detector_other_params["distance"],
            "field_of_view": detector_other_params["field_of_view"],
            "image_key": self.image_key,
            "image_key_control": detector_other_params["image_key_control"],
            "x_pixel_size": detector_other_params["x_pixel_size"],
            "y_pixel_size": detector_other_params["y_pixel_size"],
            "x_magnified_pixel_size": detector_other_params["x_magnified_pixel_size"],
            "y_magnified_pixel_size": detector_other_params["y_magnified_pixel_size"],
        }
        sample_other_params = self.other_params["sample"]
        sample_group = {
            "name": sample_other_params["name"],
            "rotation_angle": self.rotation_angle,
            "x_translation": sample_other_params["x_translation"],
            "y_translation": sample_other_params["y_translation"],
            "z_translation": sample_other_params["z_translation"],
        }
        self.dataset_dict = {
            "beam": beam_group,
            "instrument": {
                "detector": detector_group,
            },
            "sample": sample_group,
        }

    def generate_hdf5_file(self, fname, h5path=None):
        self.fname = fname
        h5path = h5path or "/entry"
        if self.dataset_dict is None:
            self.generate_dict()
        dicttoh5(self.dataset_dict, fname, h5path=h5path, mode="a")
        # Patch the "data" field which is exported as string by dicttoh5 (?!)
        self.dataset_path = os.path.join(h5path, "instrument/detector/data")
        with HDF5File(fname, "a") as fid:
            del fid[self.dataset_path]
            fid[self.dataset_path] = self.dataset_dict["instrument"]["detector"]["data"]

    # Mock some of the HDF5DatasetAnalyzer attributes
    @property
    def dataset_hdf5_url(self):
        if self.fname is None:
            raise ValueError("generate_hdf5_file() was not called")
        return DataUrl(file_path=self.fname, data_path=self.dataset_path, scheme="silx")

    def _get_images_with_key(self, key):
        indices = np.arange(self.image_key.size)[self.image_key == key]
        urls = [
            DataUrl(
                file_path=self.fname,
                data_path=self.dataset_path,
                data_slice=slice(img_idx, img_idx + 1),
                scheme="silx",
            )
            for img_idx in indices
        ]
        return dict(zip(indices, urls))

    @property
    def flats(self):
        return self._get_images_with_key(1)

    @property
    def darks(self):
        return self._get_images_with_key(2)

    def get_data_slices(self, what):
        images = getattr(self, what)
        # we can't directly use set() on slice() object (unhashable). Use tuples
        tuples_list = list(
            set((du.data_slice().start, du.data_slice().stop) for du in get_compacted_dataslices(images).values())
        )
        slices_list = [slice(item[0], item[1]) for item in tuples_list]
        return slices_list


# To be improved
def generate_nx_dataset(out_fname, image_key, data_volume=None, rotation_angle=None):
    nx_template_file = get_file("dummy.nx.tar.gz")
    nx_dict = nxtodict(nx_template_file)
    nx_entry = nx_dict["entry"]

    def _get_field(dict_, path):
        if path.startswith("/"):
            path = path[1:]
        if path.endswith("/"):
            path = path[:-1]
        split_path = path.split("/")
        if len(split_path) == 1:
            return dict_[split_path[0]]
        return _get_field(dict_[split_path[0]], "/".join(split_path[1:]))

    for name in ["image_key", "image_key_control"]:
        nx_entry["data"][name] = image_key
        nx_entry["instrument"]["detector"][name] = image_key

    if rotation_angle is not None:
        nx_entry["data"]["rotation_angle"] = rotation_angle
        nx_entry["sample"]["rotation_angle"] = rotation_angle

    dicttonx(nx_dict, out_fname)
