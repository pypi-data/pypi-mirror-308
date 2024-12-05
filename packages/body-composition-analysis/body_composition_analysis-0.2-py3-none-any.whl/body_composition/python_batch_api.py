import os
import numpy as np
import pandas as pd
from body_composition.processor import DataProcessor

class BatchAPIProcessor:
    def __init__(self, master_list_path, batch_run_save_file, verbose = 1):
        if self.check_initial_requirements(master_list_path):
            self.master_list_path = master_list_path
            self.batch_run_save_file = batch_run_save_file
            self.verbose = verbose
        self.batch_run()

    def check_initial_requirements(self, master_list_path):
        return True

    def prepare_args_from_master_list(self):
        self.master_df = pd.read_csv(self.master_list_path)
        self.Patient_Identifiers = self.master_df["Patient_Identifier"]
        self.dicom_path_T0s = self.master_df["dicom_path_T0"]
        self.dicom_path_T1s = self.master_df["dicom_path_T1"]
        self.time_intervals = self.master_df["time_interval"]
        self.save_files = self.master_df["save_file"]

    
    def batch_run(self):
        self.prepare_args_from_master_list()

        for pt_i, case in enumerate(self.Patient_Identifiers, start=0):
            if self.verbose > 0:
                print(f">> Processing batch case {pt_i+1}/{len(self.Patient_Identifiers)}")

            # Extract individual case parameters
            patient_id = self.Patient_Identifiers[pt_i]
            dicom_path_T0 = self.dicom_path_T0s[pt_i]
            dicom_path_T1 = self.dicom_path_T1s[pt_i]
            time_interval = self.time_intervals[pt_i]
            save_file = self.save_files[pt_i]
            try:
                processor = DataProcessor(Patient_Identifier=patient_id, \
                                        dicom_path_T0=dicom_path_T0, dicom_path_T1=dicom_path_T1, \
                                        time_interval=time_interval, save_file=save_file, verbose=self.verbose)
            except Exception as e:
                print(f"An unexpected error occurred: {e}") if verbose > 0 else None

        self.batch_run_df = pd.concat((pd.read_csv(file) for file in self.save_files), ignore_index=True)
        self.batch_run_df.to_csv(self.batch_run_save_file, index=False)
        print(f'The batch run has completed.') if self.verbose >0 else None

if __name__ == "__main__":
    # Input: a csv or excel file with PT_ID, DICOM_file_path_T0, DICOM_file_path_T1, time_gap, save_file_path (if exist, accumulate)
    # Output: a csv file with all results accumulated
    dir_path =  "/Radonc/Cancer Physics and Engineering Lab/Yeseul Kim/Alliance_Trial_Body_Composition_Project/pypi_body_composition/Alliance_Trial"

    master_list_path = os.path.join(dir_path, "Alliance_Trial_master_list.csv")
    batch_run_save_file = os.path.join(dir_path, "Alliance_Trial_batch_run_output.csv")
    verbose = 1

    BatchAPIProcessor(master_list_path=master_list_path, batch_run_save_file = batch_run_save_file, verbose=verbose)
