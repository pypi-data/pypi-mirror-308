#%% Axial

import os
import numpy as np
import pydicom

# Define the directory where patient folders are located
data_dir = r"C:\Users\physics\Desktop\modified_data"

# Define the standard axial plane orientation (1, 0, 0, 0, 1)
standard_orientation_axial = np.array([1, 0, 0, 0, 1])

# Function to calculate the difference between orientations in the axial plane
def calculate_rotation_in_axial_plane(orientation1, orientation2):
    return np.linalg.norm(orientation1[:4] - orientation2[:4])

# List to store the top 10 most rotated images in the axial plane
top_rotated_images = []

# Set to store processed SeriesInstanceUIDs to avoid duplicates
processed_series = set()

# Loop through the patient folders and subfolders to find the 10 most rotated images in the axial plane
for root, dirs, files in os.walk(data_dir):
    for file in files:
        file_path = os.path.join(root, file)
        try:
            # Read the DICOM file
            ds = pydicom.dcmread(file_path, stop_before_pixels=True)
            
            # Get the SeriesInstanceUID to avoid processing multiple slices from the same series
            if 'SeriesInstanceUID' in ds:
                series_uid = ds.SeriesInstanceUID
                if series_uid in processed_series:
                    continue  # Skip this file if we've already processed this series
                processed_series.add(series_uid)
            
            # Get the image orientation patient tag (0020,0037)
            if 'ImageOrientationPatient' in ds:
                image_orientation = np.array(ds.ImageOrientationPatient)
                # Calculate the rotation difference in the axial plane
                difference = calculate_rotation_in_axial_plane(image_orientation, standard_orientation_axial)
                
                # Add the result to the list and sort it by difference
                top_rotated_images.append((file_path, difference))
                top_rotated_images = sorted(top_rotated_images, key=lambda x: x[1], reverse=True)
                
                # Keep only the top 10 results
                if len(top_rotated_images) > 10:
                    top_rotated_images.pop()
                    
        except Exception as e:
            print(f"Error reading {file_path}: {e}")

# Display the 10 most rotated images in the axial plane and their differences
if top_rotated_images:
    print("Top 10 most rotated images in the axial plane (one per series):")
    for file_path, difference in top_rotated_images:
        print(f"Image: {file_path}, Rotation Difference: {difference}")
else:
    print("No DICOM images found or processed.")

#%% Sagittal

#%%
import os
import numpy as np
import pydicom

# Define the directory where patient folders are located
data_dir = r"C:\Users\physics\Desktop\modified_data"

# Define the standard sagittal plane orientation
# For the sagittal plane:
# - The row direction is typically superior to inferior: [0, 1, 0]
# - The column direction is typically anterior to posterior: [0, 0, 1]
standard_orientation_sagittal = np.array([0, 1, 0, 0, 0, 1])

# Function to calculate the difference between orientations in the sagittal plane
def calculate_rotation_in_sagittal_plane(orientation1, orientation2):
    # Calculate the Frobenius norm of the difference between the two orientation matrices
    return np.linalg.norm(orientation1 - orientation2)

# List to store the top 10 most unaligned images in the sagittal plane
top_unaligned_images = []

# Set to store processed SeriesInstanceUIDs to avoid duplicates
processed_series = set()

# Loop through the patient folders and subfolders to find the 10 most unaligned images in the sagittal plane
for root, dirs, files in os.walk(data_dir):
    for file in files:
        file_path = os.path.join(root, file)
        try:
            # Read the DICOM file
            ds = pydicom.dcmread(file_path, stop_before_pixels=True)
            
            # Get the SeriesInstanceUID to avoid processing multiple slices from the same series
            if 'SeriesInstanceUID' in ds:
                series_uid = ds.SeriesInstanceUID
                if series_uid in processed_series:
                    continue  # Skip this file if we've already processed this series
                processed_series.add(series_uid)
            
            # Get the image orientation patient tag (0020,0037)
            if 'ImageOrientationPatient' in ds:
                image_orientation = np.array(ds.ImageOrientationPatient)
                
                # Ensure that the ImageOrientationPatient has 6 elements
                if image_orientation.size != 6:
                    print(f"Invalid ImageOrientationPatient in {file_path}")
                    continue
                
                # Calculate the rotation difference in the sagittal plane
                difference = calculate_rotation_in_sagittal_plane(image_orientation, standard_orientation_sagittal)
                
                # Add the result to the list and sort it by difference
                top_unaligned_images.append((file_path, difference))
                top_unaligned_images = sorted(top_unaligned_images, key=lambda x: x[1], reverse=True)
                
                # Keep only the top 10 results
                if len(top_unaligned_images) > 10:
                    top_unaligned_images.pop()
                    
        except Exception as e:
            print(f"Error reading {file_path}: {e}")

# Display the 10 most unaligned images in the sagittal plane and their differences
if top_unaligned_images:
    print("Top 10 most unaligned images in the sagittal plane (one per series):")
    for file_path, difference in top_unaligned_images:
        print(f"Image: {file_path}, Rotation Difference: {difference}")
else:
    print("No DICOM images found or processed.")
