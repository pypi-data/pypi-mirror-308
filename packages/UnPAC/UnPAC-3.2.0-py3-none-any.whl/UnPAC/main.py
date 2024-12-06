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


def Acquirer(path, series_numbers, series_descriptions):
    start_time = time.time()
    path = Path(path)

    # Collect all initial DICOM files
    dicom_files = list(path.rglob("*.dcm"))
    print(f'{len(dicom_files)} DICOM files found.')

    count = 0
    files_to_delete = []  # Track original files that don't meet the criteria

    for dicom_loc in dicom_files:
        try:
            # Read the DICOM file
            ds = pydicom.dcmread(dicom_loc, force=True)

            # Extract metadata fields
            series_number = ds.get("SeriesNumber", "NA")
            series_description = clean_text(ds.get("SeriesDescription", "NA"))

            # Check if file meets criteria for renaming
            if series_number in series_numbers and series_description in series_descriptions:
                
                # Generate standardized filename
                modality = ds.get("Modality", "NA")
                series_instance_uid = ds.get("SeriesInstanceUID", "NA")
                instance_number = str(ds.get("InstanceNumber", "0"))
                file_name = f"{modality}.{series_instance_uid}.{instance_number}.dcm"
                
                # Set the save path to the original file's location with the new filename
                save_path = dicom_loc.with_name(file_name)

                # Decompress if needed
                try:
                    ds.decompress()
                except Exception as e:
                    print(f"File {dicom_loc} could not be decompressed: {e}")
                    continue

                # Save the file in the original directory with the standardized name
                ds.save_as(save_path)
                count += 1
                print(f"Saved file: {save_path.name} ({count} of {len(dicom_files)})")

                # If the original and saved paths differ, add original to delete list
                if save_path != dicom_loc:
                    files_to_delete.append(dicom_loc)

            else:
                # If file does not meet criteria, add to delete list
                files_to_delete.append(dicom_loc)

        except Exception as e:
            print(f"Error processing file {dicom_loc}: {e}")

    # Remove all files in files_to_delete list
    for file_path in files_to_delete:
        try:
            file_path.unlink()  # Safely remove unmatched .dcm files
        except FileNotFoundError:
            pass  # Ignore if the file has already been deleted

    print("Done")
    avg_time = (time.time() - start_time) / (len(dicom_files) or 1)
    print(f"--- {avg_time:.2f} seconds per file ---")
    
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