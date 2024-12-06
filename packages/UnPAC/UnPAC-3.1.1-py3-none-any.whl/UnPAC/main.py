# -*- coding: utf-8 -*-
"""
Created on Tue Nov 12 10:14:13 2024

@author: OKEEFFR1
"""

import os
import fnmatch
import zipfile
import shutil

def unzipper(path):
    pattern = '*.zip'
    for root, _, files in os.walk(path):
        for filename in fnmatch.filter(files, pattern):
            zip_path = os.path.join(root, filename)
            extract_dir = os.path.join(root, os.path.splitext(filename)[0])

            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(extract_dir)

            os.remove(zip_path)

    print("Unzipping complete")
    

def parser(path, exclusion_df, id_variable_name):
    # Convert exclusion list to a set for faster lookup
    excluded_ids = set(exclusion_df[id_variable_name].astype(str))

    for dirname in os.listdir(path):
        dir_path = os.path.join(path, dirname)
        # Check if it is a directory and not in the exclusion list
        if os.path.isdir(dir_path) and dirname[:7] not in excluded_ids:
            shutil.rmtree(dir_path)

    print("Parsing complete")
    
def clean_text(string):
    # Use regex to replace forbidden symbols in one operation
    import re
    forbidden_pattern = r"[*.,\"\\/\[\]|:; ]"
    return re.sub(forbidden_pattern, "_", string).lower()
    
import time
import pydicom
from pathlib import Path


def acquirer(path, series_numbers, series_descriptions):
    start_time = time.time()
    path = Path(path)

    # Collect all initial DICOM files in one scan
    unsorted_list = list(path.rglob("*.dcm"))
    print(f'{len(unsorted_list)} DICOM files found.')

    saved_files = set()
    count = 0

    for dicom_loc in unsorted_list:
        try:
            # Read the DICOM file
            ds = pydicom.dcmread(dicom_loc, force=True)

            # Extract and clean metadata fields
            patient_id = path.name
            study_date = clean_text(ds.get("StudyDate", "NA"))
            study_description = clean_text(ds.get("StudyDescription", "NA"))
            series_description = clean_text(ds.get("SeriesDescription", "NA"))
            series_number = ds.get("SeriesNumber", "NA")

            # Generate new file name
            modality = ds.get("Modality", "NA")
            series_instance_uid = ds.get("SeriesInstanceUID", "NA")
            instance_number = str(ds.get("InstanceNumber", "0"))
            file_name = f"{modality}.{series_instance_uid}.{instance_number}.dcm"

            # Decompress if compressed
            try:
                ds.decompress()
            except Exception:
                print(f"File {dicom_loc} could not be decompressed.")

            # Check series number and description, then create directory structure if needed
            if series_number in series_numbers and series_description in series_descriptions:
                save_dir = path / study_date / study_description / series_description
                save_dir.mkdir(parents=True, exist_ok=True)

                # Save file and track saved file path
                save_path = save_dir / file_name
                ds.save_as(save_path)
                saved_files.add(dicom_loc)
                count += 1
                print(f"Saved file: {file_name} - Count: {count} of {len(unsorted_list)}")

        except Exception as e:
            print(f"Error processing file {dicom_loc}: {e}")

    # Remove any original DICOM files not saved in the new directories
    unsaved_files = set(unsorted_list) - saved_files
    for file_path in unsaved_files:
        file_path.unlink()  # Remove unsaved .dcm files

    print("Done")
    avg_time = (time.time() - start_time) / (len(os.listdir(path)) or 1)
    print(f"--- {avg_time:.2f} seconds per patient ---")
    
import dicom2nifti

def converter(path):
    path = Path(path)
    directories = [d for d in path.iterdir() if d.is_dir()]
    
    for count, dirname in enumerate(directories, start=1):
        try:
            dicom2nifti.convert_directory(dirname, dirname)
            print(f"{dirname.name} has been converted to NIfTI format ({count}/{len(directories)})")
        except Exception as e:
            print(f"Failed to convert {dirname.name}: {e}")

    print("Conversion complete.")