# body_composition/__init__.py

# Import key classes for single-case and batch processing
from .python_api import DataProcessor
from .python_batch_api import BatchAPIProcessor

# Import all utility modules and functions
from .utils.dicom2nifti import dicom2nifti, is_dicom_series, process_batch_conversion
from .utils.run_total_segmentator import run_total_segmentator, run_segmentator_for_body_comp
from .utils.vol_and_int_extraction import get_img_and_arr_from_nii, is_organ_truncated, get_volume_from_mask_nii, get_intensity, find_cetner_of_vertebrae, \
    get_center_L3, get_roi_center_L3_arr, get_area_and_axial_thickness_at_center_L3, get_intensity_at_center_L3
from .utils.calculate_changes import get_volume_perc_of_roi, perc_volPerc_diff, rate_perc_volPerc_diff, perc_area_diff, rate_perc_area_diff


# Specify what should be available when importing *
__all__ = [
    "DataProcessor",
    "BatchAPIProcessor",
    "dicom2nifti",
    "is_dicom_series",
    "process_batch_conversion",
    "run_total_segmentator",
    "run_segmentator_for_body_comp",
    "get_img_and_arr_from_nii",
    "is_organ_truncated",
    "get_volume_from_mask_nii",
    "get_intensity",
    "find_cetner_of_vertebrae",
    "get_center_L3",
    "get_roi_center_L3_arr",
    "get_area_and_axial_thickness_at_center_L3",
    "get_intensity_at_center_L3",
    "get_volume_perc_of_roi",
    "perc_volPerc_diff",
    "rate_perc_volPerc_diff",
    "perc_area_diff",
    "rate_perc_area_diff"
]
