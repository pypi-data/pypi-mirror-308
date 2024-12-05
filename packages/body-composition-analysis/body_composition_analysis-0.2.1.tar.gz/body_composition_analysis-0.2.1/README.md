# Body Composition Analysis Tool

## Project Description
A command-line based tool for body composition analysis using CT images. This tool analyzes and tracks body composition changes, specifically targeting the liver, pancreas, and various tissue types. See below for more detailed usage instructions.

## Body Composition Changes Visualization
![Body Composition Changes](resources/description_img.png)  
*The above image will be replaced before any publication."
*(Inherited by Damm et al. 2023) Example visualization of body composition changes over time.*

---

## Installation

### Installation Dependencies
- **Python**: `>=3.9`
- **Other requirements**:
  - [TotalSegmentator](https://github.com/wasserth/TotalSegmentator) (follow link for more details)

### Installation
```bash
pip install body_composition_analysis
```

## Usage

### Command line
```bash
body_composition -Patient_Identifier 123456 -dicom_path_T0 /path/to/dicom_directory_T0 - dicom_path_T1 /path/to/dicom_directory_T1 -time_interval 180 -save_file /path/to/save_file -verbose 1
```
```bash
body_composition_batch -master_list_path /path/to/master_list -batch_run_save_file /path/to/batch_run_save_file -verbose 1
```
## Units of output metrics
| Output | Unit | Notes |
| --- | --- | --- |
| liver or pancreas | mm3 | ... |
| VAF & SAF & SMA | mm2 | * at center of L3 vertebrae |
| Slice thickness | mm | ... |
| Time interval | days | * Check before run |