import os
import numpy as np
import pytest
import scipy.ndimage
import h5py
from nabu.testutils import utilstest, __do_long_tests__
from nabu.testutils import get_data as nabu_get_data

from nabu.estimation.cor import (
    CenterOfRotation,
    CenterOfRotationAdaptiveSearch,
    CenterOfRotationGrowingWindow,
    CenterOfRotationSlidingWindow,
    CenterOfRotationFourierAngles,
    CenterOfRotationOctaveAccurate,
)
from nabu.estimation.cor_sino import SinoCor


@pytest.fixture(scope="class")
def bootstrap_cor(request):
    cls = request.cls
    cls.abs_tol = 0.2
    cls.data, calib_data = get_cor_data_h5("test_alignment_cor.h5")
    cls.cor_gl_pix, cls.cor_hl_pix, cls.tilt_deg = calib_data


@pytest.fixture(scope="class")
def bootstrap_cor_win(request):
    cls = request.cls
    cls.abs_tol = 0.2
    cls.data_ha_proj, cls.cor_ha_pr_pix = get_cor_win_proj_data_h5("ha_autocor_radios.npz")
    cls.data_ha_sino, cls.cor_ha_sn_pix = get_cor_win_sino_data_h5("halftomo_1_sino.npz")


@pytest.fixture(scope="class")
def bootstrap_cor_accurate(request):
    cls = request.cls
    cls.abs_tol = 0.2
    cls.image_pair_stylo, cls.cor_pos_abs_stylo = get_cor_win_proj_data_h5("stylo_accurate.npz")
    cls.image_pair_blc12781, cls.cor_pos_abs_blc12781 = get_cor_win_proj_data_h5("blc12781_accurate.npz")


@pytest.fixture(scope="class")
def bootstrap_cor_fourier(request):
    cls = request.cls
    cls.abs_tol = 0.2
    dataset_relpath = os.path.join("sino_bamboo_hercules_for_test.npz")
    dataset_downloaded_path = utilstest.getfile(dataset_relpath)
    a = np.load(dataset_downloaded_path)
    cls.sinos = a["sinos"]
    cls.angles = a["angles"]
    cls.true_cor = a["true_cor"]
    cls.estimated_cor_from_motor = a["estimated_cor_from_motor"]


def get_cor_data_h5(*dataset_path):
    """
    Get a dataset file from silx.org/pub/nabu/data
    dataset_args is a list describing a nested folder structures, ex.
    ["path", "to", "my", "dataset.h5"]
    """
    dataset_relpath = os.path.join(*dataset_path)
    dataset_downloaded_path = utilstest.getfile(dataset_relpath)
    with h5py.File(dataset_downloaded_path, "r") as hf:
        data = hf["/entry/instrument/detector/data"][()]

        cor_global_pix = hf["/calibration/alignment/global/x_rotation_axis_pixel_position"][()]

        cor_highlow_pix = hf["/calibration/alignment/highlow/x_rotation_axis_pixel_position"][()]
        tilt_deg = hf["/calibration/alignment/highlow/z_camera_tilt"][()]

    return data, (cor_global_pix, cor_highlow_pix, tilt_deg)


def get_cor_win_proj_data_h5(*dataset_path):
    """
    Get a dataset file from silx.org/pub/nabu/data
    dataset_args is a list describing a nested folder structures, ex.
    ["path", "to", "my", "dataset.h5"]
    """
    dataset_relpath = os.path.join(*dataset_path)
    dataset_downloaded_path = utilstest.getfile(dataset_relpath)
    data = np.load(dataset_downloaded_path)
    radios = np.stack((data["radio1"], data["radio2"]), axis=0)

    return radios, data["cor_pos"]


def get_cor_win_sino_data_h5(*dataset_path):
    """
    Get a dataset file from silx.org/pub/nabu/data
    dataset_args is a list describing a nested folder structures, ex.
    ["path", "to", "my", "dataset.h5"]
    """
    dataset_relpath = os.path.join(*dataset_path)
    dataset_downloaded_path = utilstest.getfile(dataset_relpath)
    data = np.load(dataset_downloaded_path)
    sino_shape = data["sino"].shape
    sinos = np.stack((data["sino"][: sino_shape[0] // 2], data["sino"][sino_shape[0] // 2 :]), axis=0)

    return sinos, data["cor"] - sino_shape[1] / 2


@pytest.mark.usefixtures("bootstrap_cor")
class TestCor:
    def test_cor_posx(self):
        radio1 = self.data[0, :, :]
        radio2 = np.fliplr(self.data[1, :, :])

        CoR_calc = CenterOfRotation()
        cor_position = CoR_calc.find_shift(radio1, radio2)
        assert np.isscalar(cor_position), f"cor_position expected to be a scale, {type(cor_position)} returned"

        message = "Computed CoR %f " % cor_position + " and real CoR %f do not coincide" % self.cor_gl_pix
        assert np.isclose(self.cor_gl_pix, cor_position, atol=self.abs_tol), message

        # testing again with the validity return value
        cor_position, result_validity = CoR_calc.find_shift(radio1, radio2, return_validity=True)
        assert np.isscalar(cor_position)

        message = (
            "returned result_validity is  %s " % result_validity
            + " while it should be unknown because the validity check is not yet implemented"
        )
        assert result_validity == "unknown", message

    def test_noisy_cor_posx(self):
        radio1 = np.fmax(self.data[0, :, :], 0)
        radio2 = np.fmax(self.data[1, :, :], 0)

        radio1 = np.random.poisson(radio1 * 400)
        radio2 = np.random.poisson(np.fliplr(radio2) * 400)

        CoR_calc = CenterOfRotation()
        cor_position = CoR_calc.find_shift(radio1, radio2, median_filt_shape=(3, 3))
        assert np.isscalar(cor_position), f"cor_position expected to be a scale, {type(cor_position)} returned"

        message = "Computed CoR %f " % cor_position + " and real CoR %f do not coincide" % self.cor_gl_pix
        assert np.isscalar(cor_position)
        assert np.isclose(self.cor_gl_pix, cor_position, atol=self.abs_tol), message

    def test_noisyHF_cor_posx(self):
        """test with noise at high frequencies"""
        radio1 = self.data[0, :, :]
        radio2 = np.fliplr(self.data[1, :, :])

        noise_level = radio1.max() / 16.0
        noise_ima1 = np.random.normal(0.0, size=radio1.shape) * noise_level
        noise_ima2 = np.random.normal(0.0, size=radio2.shape) * noise_level

        noise_ima1 = noise_ima1 - scipy.ndimage.gaussian_filter(noise_ima1, 2.0)
        noise_ima2 = noise_ima2 - scipy.ndimage.gaussian_filter(noise_ima2, 2.0)

        radio1 = radio1 + noise_ima1
        radio2 = radio2 + noise_ima2

        CoR_calc = CenterOfRotation()

        # cor_position = CoR_calc.find_shift(radio1, radio2)
        cor_position = CoR_calc.find_shift(radio1, radio2, low_pass=(6.0, 0.3))
        assert np.isscalar(cor_position), f"cor_position expected to be a scale, {type(cor_position)} returned"

        message = "Computed CoR %f " % cor_position + " and real CoR %f do not coincide" % self.cor_gl_pix
        assert np.isclose(self.cor_gl_pix, cor_position, atol=self.abs_tol), message

    @pytest.mark.skipif(not (__do_long_tests__), reason="need environment variable NABU_LONG_TESTS=1")
    def test_half_tomo_cor_exp(self):
        """test the half_tomo algorithm on experimental data"""

        radios = nabu_get_data("ha_autocor_radios.npz")
        radio1 = radios["radio1"]
        radio2 = radios["radio2"]
        cor_pos = radios["cor_pos"]

        radio2 = np.fliplr(radio2)

        CoR_calc = CenterOfRotationAdaptiveSearch()

        cor_position = CoR_calc.find_shift(radio1, radio2, low_pass=1, high_pass=20, filtered_cost=True)
        assert np.isscalar(cor_position), f"cor_position expected to be a scale, {type(cor_position)} returned"

        message = (
            "Computed CoR %f " % cor_position
            + " and real CoR %f should coincide when using the halftomo algorithm with hald tomo data" % cor_pos
        )
        assert np.isclose(cor_pos, cor_position, atol=self.abs_tol), message

    @pytest.mark.skipif(not (__do_long_tests__), reason="need environment variable NABU_LONG_TESTS=1")
    def test_half_tomo_cor_exp_limited(self):
        """test the hal_tomo algorithm on experimental data and global search with limits"""

        radios = nabu_get_data("ha_autocor_radios.npz")
        radio1 = radios["radio1"]
        radio2 = radios["radio2"]
        cor_pos = radios["cor_pos"]

        radio2 = np.fliplr(radio2)

        CoR_calc = CenterOfRotationAdaptiveSearch()

        cor_position, result_validity = CoR_calc.find_shift(
            radio1, radio2, low_pass=1, high_pass=20, margins=(100, 10), filtered_cost=False, return_validity=True
        )
        assert np.isscalar(cor_position), f"cor_position expected to be a scale, {type(cor_position)} returned"

        message = (
            "Computed CoR %f " % cor_position
            + " and real CoR %f should coincide when using the halftomo algorithm with hald tomo data" % cor_pos
        )
        assert np.isclose(cor_pos, cor_position, atol=self.abs_tol), message

        message = "returned result_validity is  %s " % result_validity + " while it should be sound"

        assert result_validity == "sound", message

    def test_cor_posx_linear(self):
        radio1 = self.data[0, :, :]
        radio2 = np.fliplr(self.data[1, :, :])

        CoR_calc = CenterOfRotation()
        cor_position = CoR_calc.find_shift(radio1, radio2, padding_mode="edge")
        assert np.isscalar(cor_position), f"cor_position expected to be a scale, {type(cor_position)} returned"

        message = "Computed CoR %f " % cor_position + " and real CoR %f do not coincide" % self.cor_gl_pix
        assert np.isclose(self.cor_gl_pix, cor_position, atol=self.abs_tol), message

    def test_error_checking_001(self):
        CoR_calc = CenterOfRotation()

        radio1 = self.data[0, :, :1:]
        radio2 = self.data[1, :, :]

        with pytest.raises(ValueError) as ex:
            CoR_calc.find_shift(radio1, radio2)

        message = "Error should have been raised about img #1 shape, other error raised instead:\n%s" % str(ex.value)
        assert "Images need to be 2-dimensional. Shape of image #1" in str(ex.value), message

    def test_error_checking_002(self):
        CoR_calc = CenterOfRotation()

        radio1 = self.data[0, :, :]
        radio2 = self.data

        with pytest.raises(ValueError) as ex:
            CoR_calc.find_shift(radio1, radio2)

        message = "Error should have been raised about img #2 shape, other error raised instead:\n%s" % str(ex.value)
        assert "Images need to be 2-dimensional. Shape of image #2" in str(ex.value), message

    def test_error_checking_003(self):
        CoR_calc = CenterOfRotation()

        radio1 = self.data[0, :, :]
        radio2 = self.data[1, :, 0:10]

        with pytest.raises(ValueError) as ex:
            CoR_calc.find_shift(radio1, radio2)

        message = (
            "Error should have been raised about different image shapes, "
            + "other error raised instead:\n%s" % str(ex.value)
        )
        assert "Images need to be of the same shape" in str(ex.value), message


@pytest.mark.skipif(not (__do_long_tests__), reason="Need NABU_LONG_TESTS=1 for this test")
@pytest.mark.usefixtures("bootstrap_cor", "bootstrap_cor_win")
class TestCorWindowSlide:
    def test_proj_center_axis_lft(self):
        radio1 = self.data[0, :, :]
        radio2 = np.fliplr(self.data[1, :, :])

        CoR_calc = CenterOfRotationSlidingWindow()
        cor_position = CoR_calc.find_shift(
            radio1, radio2, side="left", window_width=round(radio1.shape[-1] / 4.0 * 3.0)
        )
        assert np.isscalar(cor_position), f"cor_position expected to be a scale, {type(cor_position)} returned"

        message = "Computed CoR %f " % cor_position + " and expected CoR %f do not coincide" % self.cor_gl_pix
        assert np.isclose(self.cor_gl_pix, cor_position, atol=self.abs_tol), message

        cor_position, result_validity = CoR_calc.find_shift(
            radio1, radio2, side="left", window_width=round(radio1.shape[-1] / 4.0 * 3.0), return_validity=True
        )

        message = "returned result_validity is  %s " % result_validity + " while it should be sound"

        assert result_validity == "sound", message

    def test_proj_center_axis_cen(self):
        radio1 = self.data[0, :, :]
        radio2 = np.fliplr(self.data[1, :, :])

        CoR_calc = CenterOfRotationSlidingWindow()
        cor_position = CoR_calc.find_shift(radio1, radio2, side="center")
        assert np.isscalar(cor_position), f"cor_position expected to be a scale, {type(cor_position)} returned"

        message = "Computed CoR %f " % cor_position + " and expected CoR %f do not coincide" % self.cor_gl_pix
        assert np.isclose(self.cor_gl_pix, cor_position, atol=self.abs_tol), message

    def test_proj_right_axis_rgt(self):
        radio1 = self.data_ha_proj[0, :, :]
        radio2 = np.fliplr(self.data_ha_proj[1, :, :])

        CoR_calc = CenterOfRotationSlidingWindow()
        cor_position = CoR_calc.find_shift(radio1, radio2, side="right")
        assert np.isscalar(cor_position), f"cor_position expected to be a scale, {type(cor_position)} returned"

        message = "Computed CoR %f " % cor_position + " and expected CoR %f do not coincide" % self.cor_ha_pr_pix
        assert np.isclose(self.cor_ha_pr_pix, cor_position, atol=self.abs_tol), message

    def test_proj_left_axis_lft(self):
        radio1 = np.fliplr(self.data_ha_proj[0, :, :])
        radio2 = self.data_ha_proj[1, :, :]

        CoR_calc = CenterOfRotationSlidingWindow()
        cor_position = CoR_calc.find_shift(radio1, radio2, side="left")
        assert np.isscalar(cor_position), f"cor_position expected to be a scale, {type(cor_position)} returned"

        message = "Computed CoR %f " % cor_position + " and expected CoR %f do not coincide" % -self.cor_ha_pr_pix
        assert np.isclose(-self.cor_ha_pr_pix, cor_position, atol=self.abs_tol), message

    def test_sino_right_axis_rgt(self):
        sino1 = self.data_ha_sino[0, :, :]
        sino2 = np.fliplr(self.data_ha_sino[1, :, :])

        CoR_calc = CenterOfRotationSlidingWindow()
        cor_position = CoR_calc.find_shift(sino1, sino2, side="right")
        assert np.isscalar(cor_position), f"cor_position expected to be a scale, {type(cor_position)} returned"

        message = "Computed CoR %f " % cor_position + " and expected CoR %f do not coincide" % self.cor_ha_sn_pix
        assert np.isclose(self.cor_ha_sn_pix, cor_position, atol=self.abs_tol * 5), message


@pytest.mark.skipif(not (__do_long_tests__), reason="need NABU_LONG_TESTS for this test")
@pytest.mark.usefixtures("bootstrap_cor", "bootstrap_cor_win")
class TestCorWindowGrow:
    def test_proj_center_axis_cen(self):
        radio1 = self.data[0, :, :]
        radio2 = np.fliplr(self.data[1, :, :])

        CoR_calc = CenterOfRotationGrowingWindow()
        cor_position = CoR_calc.find_shift(radio1, radio2, side="center")
        assert np.isscalar(cor_position), f"cor_position expected to be a scale, {type(cor_position)} returned"
        message = "Computed CoR %f " % cor_position + " and expected CoR %f do not coincide" % self.cor_gl_pix
        assert np.isclose(self.cor_gl_pix, cor_position, atol=self.abs_tol), message

    def test_proj_right_axis_rgt(self):
        radio1 = self.data_ha_proj[0, :, :]
        radio2 = np.fliplr(self.data_ha_proj[1, :, :])

        CoR_calc = CenterOfRotationGrowingWindow()
        cor_position = CoR_calc.find_shift(radio1, radio2, side="right")
        assert np.isscalar(cor_position), f"cor_position expected to be a scale, {type(cor_position)} returned"

        message = "Computed CoR %f " % cor_position + " and expected CoR %f do not coincide" % self.cor_ha_pr_pix
        assert np.isclose(self.cor_ha_pr_pix, cor_position, atol=self.abs_tol), message

    def test_proj_left_axis_lft(self):
        radio1 = np.fliplr(self.data_ha_proj[0, :, :])
        radio2 = self.data_ha_proj[1, :, :]

        CoR_calc = CenterOfRotationGrowingWindow()
        cor_position = CoR_calc.find_shift(radio1, radio2, side="left")
        assert np.isscalar(cor_position), f"cor_position expected to be a scale, {type(cor_position)} returned"

        message = "Computed CoR %f " % cor_position + " and expected CoR %f do not coincide" % -self.cor_ha_pr_pix
        assert np.isclose(-self.cor_ha_pr_pix, cor_position, atol=self.abs_tol), message

        cor_position, result_validity = CoR_calc.find_shift(radio1, radio2, side="left", return_validity=True)

        message = "returned result_validity is  %s " % result_validity + " while it should be sound"

        assert result_validity == "sound", message

    def test_proj_right_axis_all(self):
        radio1 = self.data_ha_proj[0, :, :]
        radio2 = np.fliplr(self.data_ha_proj[1, :, :])

        CoR_calc = CenterOfRotationGrowingWindow()
        cor_position = CoR_calc.find_shift(radio1, radio2, side="all")
        assert np.isscalar(cor_position), f"cor_position expected to be a scale, {type(cor_position)} returned"

        message = "Computed CoR %f " % cor_position + " and expected CoR %f do not coincide" % self.cor_ha_pr_pix
        assert np.isclose(self.cor_ha_pr_pix, cor_position, atol=self.abs_tol), message

    def test_sino_right_axis_rgt(self):
        sino1 = self.data_ha_sino[0, :, :]
        sino2 = np.fliplr(self.data_ha_sino[1, :, :])

        CoR_calc = CenterOfRotationGrowingWindow()
        cor_position = CoR_calc.find_shift(sino1, sino2, side="right")
        assert np.isscalar(cor_position), f"cor_position expected to be a scale, {type(cor_position)} returned"

        message = "Computed CoR %f " % cor_position + " and expected CoR %f do not coincide" % self.cor_ha_sn_pix
        assert np.isclose(self.cor_ha_sn_pix, cor_position, atol=self.abs_tol * 4), message


@pytest.mark.usefixtures("bootstrap_cor_win")
class TestCoarseToFineSinoCor:
    def test_coarse_to_fine(self):
        """
        Test nabu.estimation.cor_sino.SinoCor
        """
        sino_halftomo = np.vstack([self.data_ha_sino[0], self.data_ha_sino[1]])
        sino_cor = SinoCor(self.data_ha_sino[0], np.fliplr(self.data_ha_sino[1]))
        cor_coarse = sino_cor.estimate_cor_coarse()
        assert np.isscalar(cor_coarse), f"cor_position expected to be a scalar, {type(cor_coarse)} returned"
        cor_fine = sino_cor.estimate_cor_fine()
        assert np.isscalar(cor_fine), f"cor_position expected to be a scale, {type(cor_fine)} returned"

        cor_ref = self.cor_ha_sn_pix + sino_halftomo.shape[-1] / 2.0
        message = "Computed CoR %f " % cor_fine + " and expected CoR %f do not coincide" % cor_ref
        assert abs(cor_fine - cor_ref) < self.abs_tol * 2, message


@pytest.mark.usefixtures("bootstrap_cor_accurate")
class TestCorOctaveAccurate:
    def test_cor_accurate_positive_shift(self):
        detector_width = self.image_pair_stylo[0].shape[1]
        CoR_calc = CenterOfRotationOctaveAccurate()
        cor_position = CoR_calc.find_shift(self.image_pair_stylo[0], np.fliplr(self.image_pair_stylo[1]), "center")
        cor_position = cor_position + detector_width / 2
        assert np.isscalar(cor_position), f"cor_position expected to be a scalar, {type(cor_position)} returned"
        message = f"Computed CoR {cor_position} and expected CoR {self.cor_pos_abs_stylo} do not coincide."
        assert np.isclose(self.cor_pos_abs_stylo, cor_position, atol=self.abs_tol), message

    def test_cor_accurate_negative_shift(self):
        detector_width = self.image_pair_blc12781[0].shape[1]
        CoR_calc = CenterOfRotationOctaveAccurate()
        cor_position = CoR_calc.find_shift(
            self.image_pair_blc12781[0], np.fliplr(self.image_pair_blc12781[1]), "center"
        )
        cor_position = cor_position + detector_width / 2
        assert np.isscalar(cor_position), f"cor_position expected to be a scalar, {type(cor_position)} returned"
        message = f"Computed CoR {cor_position} and expected CoR {self.cor_pos_abs_blc12781} do not coincide."
        assert np.isclose(self.cor_pos_abs_blc12781, cor_position, atol=self.abs_tol), message


@pytest.mark.usefixtures("bootstrap_cor_fourier", "bootstrap_cor_win")
class TestCorFourierAngle:
    def test_sino_right_axis_with_near_pos(self):
        sino1 = self.data_ha_sino[0, :, :]
        sino2 = np.fliplr(self.data_ha_sino[1, :, :])
        start_angle = np.pi / 4
        angles = np.linspace(start_angle, start_angle + 2 * np.pi, 2 * sino1.shape[0])

        cor_options = {"side": 740, "refine": True}

        CoR_calc = CenterOfRotationFourierAngles(cor_options=cor_options)
        cor_position = CoR_calc.find_shift(sino1, sino2, angles, side="right")
        assert np.isscalar(cor_position), f"cor_position expected to be a scale, {type(cor_position)} returned"

        message = "Computed CoR %f " % cor_position + " and expected CoR %f do not coincide" % self.cor_ha_sn_pix
        assert np.isclose(self.cor_ha_sn_pix, cor_position, atol=self.abs_tol * 3), message

    def test_sino_right_axis_with_ignore(self):
        sino1 = self.data_ha_sino[0, :, :]
        sino2 = np.fliplr(self.data_ha_sino[1, :, :])
        start_angle = np.pi / 4
        angles = np.linspace(start_angle, start_angle + 2 * np.pi, 2 * sino1.shape[0])

        cor_options = {"side": "ignore", "refine": True}

        CoR_calc = CenterOfRotationFourierAngles(cor_options=cor_options)
        cor_position = CoR_calc.find_shift(sino1, sino2, angles, side="right")
        assert np.isscalar(cor_position), f"cor_position expected to be a scale, {type(cor_position)} returned"

        message = "Computed CoR %f " % cor_position + " and expected CoR %f do not coincide" % self.cor_ha_sn_pix
        assert np.isclose(self.cor_ha_sn_pix, cor_position, atol=self.abs_tol * 3), message
