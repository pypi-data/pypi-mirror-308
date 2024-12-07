#%%
import os
import numpy as np
import pydicom
import nibabel as nib
import nrrd
from PIL import Image
from scipy.ndimage import zoom
from collections import Counter
import multiprocessing
from concurrent.futures import ProcessPoolExecutor, as_completed
import shutil

import SimpleITK as sitk
from rt_utils import RTStructBuilder

from header_map import DICOM_MODALITIES
from header_controls import *
from header_tag_conversions import anatomical_plane_dicom
from prepare_dicom_slice import prepare_dicom_slice


# For sorting DICOM slices/files
def sort_key(data):
    if hasattr(data, 'ImagePositionPatient'):
        origin = data.ImagePositionPatient
        orientation = data.ImageOrientationPatient
        col_i = orientation[:3]
        col_j = orientation[3:]
        col_k = np.cross(col_i, col_j)
        return np.dot(col_k, origin)
    elif hasattr(data, 'InstanceNumber'):
        return data.InstanceNumber
    elif hasattr(data, 'SliceLocation'):
        return data.SliceLocation

def make_3d_if_2d(arr):
    if arr.ndim == 2:
        arr = np.expand_dims(arr, axis=-1)
    return arr

def get_dicom_sitk_image(path_in, reader):
    # Get the available DICOM series in the directory
    dicom_series_uids = reader.GetGDCMSeriesIDs(path_in)

    dicom_img_sitk = None
    dicom_names = None

    if not dicom_series_uids:
        print("No DICOM series found in the directory.")
    else:
        print(f"Found {len(dicom_series_uids)} series in the directory.")

        # For each series UID, get the file names and print them
        for series_uid in dicom_series_uids:
            dicom_names = reader.GetGDCMSeriesFileNames(path_in, series_uid)
            
            print(f"Series UID: {series_uid}")
            print(f"Number of files in this series: {len(dicom_names)}")

            # Remove any files that are RTDOSE, RTPLAN, or RTSTRUCT from dicom_names
            dicom_names = list(dicom_names)
            for dicom_name in dicom_names:
                ds = pydicom.dcmread(dicom_name, stop_before_pixels=True)
                image_modalities = ["CT", "MR", "PT", "NM", "DX", "OT"]
                if ds.Modality not in image_modalities:
                    dicom_names.remove(dicom_name)
            dicom_names = tuple(dicom_names)

            if len(dicom_names) > 0:
                # Set the selected series to read the images
                reader.SetFileNames(dicom_names)
                dicom_img_sitk = reader.Execute()

                break  # Exit after finding and loading the image series

    return dicom_img_sitk, dicom_names

def sitk_image_parameters(sitk_image):

    if type(sitk_image) == list:
        sitk_image = sitk_image[0]

    parameters = {}

    # Store original parameters
    parameters["spacing"] = np.array(sitk_image.GetSpacing())
    parameters["origin"] = np.array(sitk_image.GetOrigin())
    parameters["size"] = np.array(sitk_image.GetSize())
    parameters["direction"] = np.array(sitk_image.GetDirection()).reshape(3, 3)

    return parameters

def align_to_identity(sitk_image, mask=False):
    """
    Resample the given SimpleITK image to align it with the identity direction matrix,
    adjusting the origin to keep the image centered in the same physical location.

    Parameters:
        sitk_image (sitk.Image): The input SimpleITK image.

    Returns:
        tuple: A tuple containing the resampled SimpleITK image aligned to the identity direction
               and a dictionary with the original parameters.
    """

    if not type(sitk_image) == list:
        sitk_image = [sitk_image]

    # Dictionary to store original parameters
    parameters = sitk_image_parameters(sitk_image[0])

    # Get parameters from the original image
    spacing = np.array(parameters["spacing"])
    origin = np.array(parameters["origin"])
    size = np.array(parameters["size"])
    direction = np.array(parameters["direction"]).reshape(3, 3)

    # Compute the physical coordinates of the image center
    original_center = origin + np.dot(direction, (size - 1) / 2.0 * spacing)

    # Desired output parameters
    desired_spacing = spacing
    desired_direction = np.identity(3).flatten()

    # Compute the new origin to keep the center in the same physical location
    new_origin = original_center - np.dot(np.identity(3), (size - 1) / 2.0 * spacing)
    desired_origin = new_origin.tolist()

    # Initialize the ResampleImageFilter
    resample_filter = sitk.ResampleImageFilter()
    resample_filter.SetInterpolator(sitk.sitkLinear if not mask else sitk.sitkNearestNeighbor)
    resample_filter.SetDefaultPixelValue(0)
    resample_filter.SetTransform(sitk.Transform())

    # Set desired output parameters
    resample_filter.SetOutputSpacing(desired_spacing.tolist())
    resample_filter.SetSize(size.astype(int).tolist())
    resample_filter.SetOutputOrigin(desired_origin)
    resample_filter.SetOutputDirection(desired_direction)

    # Execute the resampling on the original image
    for i, img in enumerate(sitk_image):
        sitk_image[i] = resample_filter.Execute(img)

    if len(sitk_image) == 1:
        sitk_image = sitk_image[0]

    return sitk_image

def any_to_numpy(path_in, viewing_or_converting='converting', apply_affine=False):
    print("any_to_numpy")

    slice_info_dict = None # For dicom
    is_dicom = False
    is_rtss = False
    voxel_spacing = [1, 1, 1] # Default
    rotation_matrix = np.eye(3)
    plane = 'axial' # Default
    input_format = ''

    try:
        data = pydicom.dcmread(path_in, stop_before_pixels=True)
        is_dicom = True
        
        if data.Modality == 'RTSTRUCT':
            is_rtss = True
    except:
        pass

    if '.nii' in path_in:
        input_format = 'nifti'

        nifti_img_sitk = sitk.ReadImage(path_in)

        original_params = sitk_image_parameters(nifti_img_sitk)
        voxel_spacing = original_params['spacing']
        voxel_spacing = [voxel_spacing[2], voxel_spacing[1], voxel_spacing[0]]

        if apply_affine:
            nifti_img_sitk = align_to_identity(nifti_img_sitk)
        
        image = sitk.GetArrayFromImage(nifti_img_sitk)
        image = make_3d_if_2d(image)

        plane = anatomical_plane_nifti(nifti_img_sitk)

    elif '.npy' in path_in:
        image = np.load(path_in)
        image = make_3d_if_2d(image)
        input_format = 'npy'

    elif '.npz' in path_in:
        image = np.load(path_in)['probabilities'][0]
        image = make_3d_if_2d(image)
        input_format = 'npz'

    elif '.nrrd' in path_in:
        input_format = 'nrrd'

        nrrd_img_sitk = sitk.ReadImage(path_in)

        original_params = sitk_image_parameters(nrrd_img_sitk)
        voxel_spacing = original_params['spacing']
        voxel_spacing = [voxel_spacing[2], voxel_spacing[1], voxel_spacing[0]]

        if apply_affine:
            nrrd_img_sitk = align_to_identity(nrrd_img_sitk)
        
        image = sitk.GetArrayFromImage(nrrd_img_sitk)
        image = make_3d_if_2d(image)

        plane = anatomical_plane_nifti(nrrd_img_sitk)

    elif '.tif' in path_in or '.tiff' in path_in:
        input_format = 'tiff'
        
        tiff_img_sitk = sitk.ReadImage(path_in)
        
        original_params = sitk_image_parameters(tiff_img_sitk)
        voxel_spacing = original_params['spacing']
        voxel_spacing = [voxel_spacing[2], voxel_spacing[1], voxel_spacing[0]]

        if apply_affine:
            tiff_img_sitk = align_to_identity(tiff_img_sitk)
            
        image = sitk.GetArrayFromImage(tiff_img_sitk)
        image = make_3d_if_2d(image)
        
        plane = anatomical_plane_nifti(tiff_img_sitk)

    elif '.mha' in path_in or '.mhd' in path_in:
        input_format = 'metaimage'
        
        meta_img_sitk = sitk.ReadImage(path_in)
        
        original_params = sitk_image_parameters(meta_img_sitk)
        voxel_spacing = original_params['spacing']
        voxel_spacing = [voxel_spacing[2], voxel_spacing[1], voxel_spacing[0]]

        if apply_affine:
            meta_img_sitk = align_to_identity(meta_img_sitk)
            
        image = sitk.GetArrayFromImage(meta_img_sitk)
        image = make_3d_if_2d(image)
        
        plane = anatomical_plane_nifti(meta_img_sitk)

    elif '.png' in path_in or '.jpeg' in path_in or '.jpg' in path_in:
        img = Image.open(path_in)
        image = np.array(img)
        image = make_3d_if_2d(image)
        image = np.rot90(image, k=-1, axes=(1, 0))
        input_format = 'png_or_jpeg'

    elif is_rtss:
        input_format = 'rtss'

        # Get list of reference SOP instance UIDs from the RTSS
        rtss_data = pydicom.dcmread(path_in, stop_before_pixels=True)
        ref_sop_instance_uids = []
        for structure in rtss_data.ROIContourSequence:
            for contour in structure.ContourSequence:
                ref_sop_instance_uids.append(contour.ContourImageSequence[0].ReferencedSOPInstanceUID)
        
        # Find the DICOM image directory containing the reference SOP instance UIDs
        sop_instance_uids_and_paths = get_sop_instance_uids(os.path.abspath(os.path.join(path_in, os.pardir, os.pardir)))
        image_dir = ''
        for ref_sop_uid in ref_sop_instance_uids:
            if ref_sop_uid in sop_instance_uids_and_paths:
                ds = pydicom.dcmread(sop_instance_uids_and_paths[ref_sop_uid], stop_before_pixels=True)
                if hasattr(ds, 'ImagePositionPatient'): # Check the file is a DICOM image
                    image_dir = os.path.abspath(os.path.join(sop_instance_uids_and_paths[ref_sop_uid], os.pardir))
                    break

        image, slice_info_dict, plane, voxel_spacing, rotation_matrix, input_format, _, _ = any_to_numpy(image_dir, "converting")

        structure_masks, _, structure_names, image_array = rtss_to_npy(path_in, slice_info_dict, apply_affine)

        return [image_array, structure_masks], slice_info_dict, plane, voxel_spacing, rotation_matrix, input_format, image_dir, structure_names

    elif is_dicom:
        input_format = 'dicom'
        data = pydicom.dcmread(path_in)
        if hasattr(data, 'PixelData'):
            pixel_array = data.pixel_array
            rescale_slope = data.RescaleSlope if "RescaleSlope" in data else 1.0
            rescale_intercept = data.RescaleIntercept if "RescaleIntercept" in data else 0.0
            pixel_array = pixel_array * rescale_slope + rescale_intercept
            image = np.expand_dims(pixel_array, axis=-1)
            if viewing_or_converting == 'viewing':
                image = np.rot90(image, k=1, axes=(0, 1)) # Counterclockwise
            plane = anatomical_plane_dicom(data.ImageOrientationPatient)
            print('anatomical plane dicom:', plane)

            header_in = get_header_info(path_in)[0]
            print(header_in)
            pixel_spacing = header_in["Pixel Spacing"]
            slice_spacing = header_in.get("Slice Spacing", header_in.get("Slice Thickness", 1.0))
            voxel_spacing = np.append(pixel_spacing, slice_spacing)
        else:
            print('No PixelData found in the DICOM file.')
            return None, None, None, None, None, None, None, None

    elif os.path.isdir(path_in):
        input_format = 'dicom'

        # Initialize the ImageSeriesReader
        reader = sitk.ImageSeriesReader()

        image_sitk, dicom_names = get_dicom_sitk_image(path_in, reader)

        if image_sitk == None:
            return None, None, None, None, None, None, None, None

        # Initialize slice_info_dict to store metadata
        slice_info_dict = {}

        # Read the first DICOM file to extract common metadata
        first_dicom = pydicom.dcmread(dicom_names[0])
        study_instance_uid = first_dicom.StudyInstanceUID
        series_instance_uid = first_dicom.SeriesInstanceUID
        slice_info_dict['study_instance_uid'] = study_instance_uid
        slice_info_dict['series_instance_uid'] = series_instance_uid
        slice_info_dict['image_orientation_patient'] = first_dicom.ImageOrientationPatient

        # Populate slice_info_dict with SOPInstanceUID mapping to slice index
        for index, file in enumerate(dicom_names):
            try:
                data = pydicom.dcmread(file, stop_before_pixels=True)
                sop_instance_uid = data.SOPInstanceUID
                slice_info_dict[sop_instance_uid] = index
            except Exception as e:
                print(f'Warning: Could not read SOPInstanceUID from {file}: {e}')

        # Determine the anatomical plane based on ImageOrientationPatient
        plane = anatomical_plane_dicom(first_dicom.ImageOrientationPatient)
        voxel_spacing = np.array(image_sitk.GetSpacing())
        rotation_matrix = np.array(image_sitk.GetDirection()).reshape(3, 3)

        if apply_affine:
            image_sitk = align_to_identity(image_sitk)
            
        image = sitk.GetArrayFromImage(image_sitk)
        voxel_spacing = voxel_spacing[::-1] # xyz to zyx

        return image, slice_info_dict, plane, voxel_spacing, rotation_matrix, input_format, path_in, None
    else:
        print('File type not supported.')
        return None, None, None, None, None, None, None, None
    
    return image, slice_info_dict, plane, voxel_spacing, rotation_matrix, input_format, path_in, None

def xyz_to_zyx(array):
    mask = np.flip(array, axis=0)
    mask = np.rot90(mask, k=-1, axes=(0, 1))
    mask = np.transpose(mask, (2, 1, 0))
    return mask

def zyx_to_xyz(array):
    mask = np.transpose(array, (2, 1, 0))
    mask = np.rot90(mask, k=1, axes=(0, 1))
    mask = np.flip(mask, axis=0)
    return mask

def find_rtss_from_image(image_path, slice_info_dict):

    # Find RTSS parent directory
    rtss_parent_dir = os.path.abspath(os.path.join(image_path, os.pardir))

    if slice_info_dict is None:
        raise ValueError("slice_info_dict is required.")

    series_instance_uid = slice_info_dict.get('series_instance_uid')
    study_instance_uid = slice_info_dict.get('study_instance_uid')

    if not series_instance_uid or not study_instance_uid:
        raise ValueError("slice_info_dict must contain 'series_instance_uid' and 'study_instance_uid'.")

    rtss_found = False
    rtss_path = None

    # First search in the directory of the given image_path
    for file in os.listdir(image_path):
        file_path = os.path.join(image_path, file)
        if os.path.isfile(file_path):
            try:
                dicom_data = pydicom.dcmread(file_path, stop_before_pixels=True)
                if dicom_data.Modality == 'RTSTRUCT':
                    # Match SeriesInstanceUID or StudyInstanceUID
                    if getattr(dicom_data, 'SeriesInstanceUID', None) == series_instance_uid:
                        rtss_path = file_path
                        rtss_found = True
                        break
                    elif getattr(dicom_data, 'StudyInstanceUID', None) == study_instance_uid:
                        rtss_path = file_path
                        rtss_found = True
                        break
            except Exception:
                continue

    # If no RTSTRUCT is found, search in the parent directory
    if not rtss_found:
        for root, dirs, files in os.walk(rtss_parent_dir):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    dicom_data = pydicom.dcmread(file_path, stop_before_pixels=True)
                    if dicom_data.Modality == 'RTSTRUCT':
                        # Match SeriesInstanceUID or StudyInstanceUID
                        if getattr(dicom_data, 'SeriesInstanceUID', None) == series_instance_uid:
                            rtss_path = file_path
                            rtss_found = True
                            break
                        elif getattr(dicom_data, 'StudyInstanceUID', None) == study_instance_uid:
                            rtss_path = file_path
                            rtss_found = True
                            break
                except Exception:
                    continue
            if rtss_found:
                break

    # If RTSTRUCT is found, return the path; otherwise return the image path
    if rtss_found:
        print('RTSS found:', rtss_path)
    else:
        rtss_path = image_path

    return rtss_path

def find_image_from_rtss(rtss_path, slice_info_dict):

    # Find RTSS parent directory
    rtss_parent_dir = os.path.abspath(os.path.join(rtss_path, os.pardir))

    if slice_info_dict is None:
        raise ValueError("slice_info_dict is required.")

    series_instance_uid = slice_info_dict.get('series_instance_uid')
    study_instance_uid = slice_info_dict.get('study_instance_uid')

    if not series_instance_uid or not study_instance_uid:
        raise ValueError("slice_info_dict must contain 'series_instance_uid' and 'study_instance_uid'.")

    image_found = False
    image_path = None

    # List of common image modalities and RTSTRUCT
    image_modalities = ['CT', 'MR', 'PT', 'CR', 'DX', 'XA', 'RF', 'US', 'NM']

    # First search in the RTSS parent directory
    for file in os.listdir(rtss_parent_dir):
        file_path = os.path.join(rtss_parent_dir, file)
        if os.path.isfile(file_path):
            try:
                dicom_data = pydicom.dcmread(file_path, stop_before_pixels=True)
                if dicom_data.Modality in image_modalities:
                    # Match SeriesInstanceUID or StudyInstanceUID
                    if getattr(dicom_data, 'SeriesInstanceUID', None) == series_instance_uid:
                        image_path = rtss_parent_dir
                        image_found = True
                        break
                    elif getattr(dicom_data, 'StudyInstanceUID', None) == study_instance_uid:
                        image_path = rtss_parent_dir
                        image_found = True
                        break
            except Exception:
                continue

    # If no image is found, search one layer deep in the neighboring directories of the parent directory
    if not image_found:
        parent_dir = os.path.abspath(os.path.join(rtss_parent_dir, os.pardir))
        for directory in os.listdir(parent_dir):
            dir_path = os.path.join(parent_dir, directory)
            if os.path.isdir(dir_path) and dir_path != rtss_parent_dir:
                for file in os.listdir(dir_path):
                    file_path = os.path.join(dir_path, file)
                    if os.path.isfile(file_path):
                        try:
                            dicom_data = pydicom.dcmread(file_path, stop_before_pixels=True)
                            if dicom_data.Modality in image_modalities:
                                # Match SeriesInstanceUID or StudyInstanceUID
                                if getattr(dicom_data, 'SeriesInstanceUID', None) == series_instance_uid:
                                    image_path = dir_path
                                    image_found = True
                                    break
                                elif getattr(dicom_data, 'StudyInstanceUID', None) == study_instance_uid:
                                    image_path = dir_path
                                    image_found = True
                                    break
                        except Exception:
                            continue
                if image_found:
                    break

    if image_found:
        print('Image series found:', image_path)
    else:
        image_path = rtss_path  # Default to RTSS path if no image found

    return image_path

def rtss_to_npy(
    path_in,
    slice_info_dict,
    apply_affine=True,
):
    
    if os.path.isdir(path_in):
        image_path = path_in
        rtss_path = find_rtss_from_image(path_in, slice_info_dict)
    else:
        image_path = find_image_from_rtss(path_in, slice_info_dict)
        rtss_path = path_in
    print('image_path', image_path)
    print('rtss_path', rtss_path)

    # Temporarily move RTDOSE file into child directory
    file_paths = [os.path.join(image_path, file) for file in os.listdir(image_path)]
    temp_dir = os.path.join(os.path.dirname(os.path.abspath(image_path)), 'temp')
    os.makedirs(temp_dir, exist_ok=True)  # Create the temp directory if it doesn't exist
    for file_path in file_paths:
        try:
            ds = pydicom.dcmread(file_path, stop_before_pixels=True)
            image_modalities = ['CT', 'MR', 'PT', 'CR', 'DX', 'XA', 'RF', 'US', 'NM', 'RTSTRUCT']
            if ds.Modality not in image_modalities:
                shutil.move(file_path, temp_dir)
        except Exception as e:
            print(f"An error occurred: {e}")
            continue

    # Process RTSTRUCT
    rtstruct_utils = RTStructBuilder.create_from(
        dicom_series_path=image_path,
        rt_struct_path=rtss_path
    )
    structure_names = rtstruct_utils.get_roi_names()
    print('structure_names', structure_names)

    # Put RTDOSE back
    for file in os.listdir(temp_dir):
        shutil.move(os.path.join(temp_dir, file), image_path)
    shutil.rmtree(temp_dir)

    if not structure_names:
        raise ValueError("No structures found in RTSTRUCT.")

    # Load the DICOM series with SimpleITK
    reader_sitk = sitk.ImageSeriesReader()
    dicom_img_sitk, dicom_names = get_dicom_sitk_image(image_path, reader_sitk)
    dicom_img_npy = sitk.GetArrayFromImage(dicom_img_sitk)

    structure_masks = []

    for structure_name in structure_names:
        try:
            print('here1')
            mask_3d = rtstruct_utils.get_roi_mask_by_name(structure_name)
            mask_3d = xyz_to_zyx(mask_3d)

            print('here2')
            # Copy spatial information from original scan
            mask_img_sitk = sitk.GetImageFromArray(mask_3d.astype(np.uint8))

            # Print shapes
            print(f"\nImage shape: {dicom_img_sitk.GetSize()}")
            print(f"{structure_name}: {mask_img_sitk.GetSize()}")

            # Apply affine transform
            mask_img_sitk.CopyInformation(dicom_img_sitk)

            # Apply affine if needed
            if apply_affine:
                mask_img_sitk = align_to_identity(mask_img_sitk, mask=True)

            # Convert back to NumPy
            mask_3d = sitk.GetArrayFromImage(mask_img_sitk)

            structure_masks.append(mask_3d)

        except Exception as e:
            print(f"An error occurred: {e}")
            structure_names.remove(structure_name)
            
    return structure_masks, rtss_path, structure_names, dicom_img_npy


class ImageConverter:
    def __init__(self, path_in, path_out, format_out=None, perform_resample=False, resample_shape=None, resample_voxels=None, resample_order=1, perform_crop=False, crop_entry=None, apply_affine=False):
        self.path_in = path_in
        self.path_out = path_out
        self.format_out = format_out.lower()
        self.perform_resample = perform_resample
        self.resample_order = resample_order
        self.perform_crop = perform_crop
        self.crop_entry = crop_entry
        self.apply_affine = apply_affine
        self.image, self.slice_info_dict, self.plane, self.voxel_spacing_start, self.rotation_matrix, self.format_in, self.path_in, self.structure_names = any_to_numpy(self.path_in, "converting")
        self.header_in, _ = get_header_info(self.path_in)  # Get header of image rather than of RTSS

        self.is_mask = False

        # If contains both an image and mask(s) in list, get mask(s)
        if isinstance(self.image, list):
            # self.image = [item for sublist in self.image for item in (sublist if isinstance(sublist, list) else [sublist])]
            self.image = self.image[1]
            # self.structure_names.insert(0, 'Image')       

        # File save paths
        if not isinstance(self.image, list):
            self.file_save_paths = [self.path_out]
        else:
            if np.unique(self.image[0]).shape[0] == 2:
                self.is_mask = True

            self.file_save_paths = []
            for structure_name in self.structure_names:
                par_dir_path = os.path.abspath(os.path.join(self.path_out, os.pardir))
                new_structure_name = self.replace_disallowed_chars(structure_name)
                self.file_save_paths.append(os.path.join(par_dir_path, new_structure_name))

        if self.perform_resample == 'Voxels':
            self.voxel_spacing_target = np.array([float(x) for x in resample_voxels])
            self.voxel_spacing_target = self.voxel_spacing_target[::-1]  # ZYX to XYZ

        elif self.perform_resample == 'Shape':
            self.target_shape = np.array(resample_shape)
            self.target_shape_xyz = self.target_shape[::-1]  # ZYX to XYZ

        # Read the original image with SimpleITK
        if self.format_in == 'dicom':

            is_rtss = False
            try:
                data = pydicom.dcmread(path_in, stop_before_pixels=True)
                if data.Modality == 'RTSTRUCT':
                    is_rtss = True
            except:
                pass

            if is_rtss == True:
                image_path = find_image_from_rtss(self.path_in, self.slice_info_dict)
            else:
                image_path = self.path_in

            # Temporarily move RTDOSE file into child directory
            file_paths = [os.path.join(image_path, file) for file in os.listdir(image_path)]
            temp_dir = os.path.join(os.path.dirname(os.path.abspath(image_path)), 'temp')
            os.makedirs(temp_dir, exist_ok=True)  # Create the temp directory if it doesn't exist
            for file_path in file_paths:
                try:
                    ds = pydicom.dcmread(file_path, stop_before_pixels=True)
                    image_modalities = ['CT', 'MR', 'PT', 'CR', 'DX', 'XA', 'RF', 'US', 'NM', 'RTSTRUCT']
                    if ds.Modality not in image_modalities:
                        shutil.move(file_path, temp_dir)
                except Exception as e:
                    print(f"An error occurred: {e}")
                    continue

            # Load the DICOM series with SimpleITK
            reader_sitk = sitk.ImageSeriesReader()
            dicom_series_uids = reader_sitk.GetGDCMSeriesIDs(image_path)
            if not dicom_series_uids:
                raise ValueError("No DICOM series found in the directory.")
            else:
                # For simplicity, select the first series UID
                series_uid = dicom_series_uids[0]
                dicom_names = reader_sitk.GetGDCMSeriesFileNames(image_path, series_uid)
                reader_sitk.SetFileNames(dicom_names)
                self.original_image_sitk = reader_sitk.Execute()

            # Put RTDOSE back
            for file in os.listdir(temp_dir):
                shutil.move(os.path.join(temp_dir, file), image_path)
            shutil.rmtree(temp_dir)
        elif self.format_in in ['nrrd', 'nifti']:
            # Read the image with SimpleITK
            self.original_image_sitk = sitk.ReadImage(self.path_in)
        else:
            self.original_image_sitk = None  # For formats like numpy arrays or images

        # Create SimpleITK image from numpy array and copy metadata
        if not isinstance(self.image, list):
            self.image_sitk = sitk.GetImageFromArray(self.image)
            if self.original_image_sitk:
                self.image_sitk.CopyInformation(self.original_image_sitk)
        else:
            self.image_sitk = []
            for img in self.image:
                img_sitk = sitk.GetImageFromArray(img)
                if self.original_image_sitk:
                    img_sitk.CopyInformation(self.original_image_sitk)
                self.image_sitk.append(img_sitk)

        if self.apply_affine:
            self.image_sitk = align_to_identity(self.image_sitk)

    def convert(self):
        if self.perform_resample in ['Voxels', 'Shape']:
            self.resample()

        if self.perform_crop:
            self.crop()

        self.update_header()

        format_out = self.format_out
        print('format_out:', format_out)
        if format_out == 'numpy':
            self.to_numpy()
        elif format_out == 'nifti':
            self.to_nifti()
        elif format_out == 'nrrd':
            self.to_nrrd()
        elif format_out == 'png':
            self.to_png()
        elif format_out == 'jpeg' or format_out == 'jpg':
            self.to_jpeg()
        elif format_out == 'dicom':
            self.to_dicom()
        else:
            raise ValueError(f"Unsupported output format: {self.format_out}")

    def resample(self):
        # Resample using SimpleITK
        if not isinstance(self.image_sitk, list):
            self.image_sitk = self.resample_sitk_image(self.image_sitk)
        else:
            for i in range(len(self.image_sitk)):
                self.image_sitk[i] = self.resample_sitk_image(self.image_sitk[i], is_mask=self.is_mask)

    def resample_sitk_image(self, image_sitk, is_mask=False):
        # Define the resampling parameters
        original_spacing = np.array(image_sitk.GetSpacing())  # XYZ order
        original_size = np.array(image_sitk.GetSize())  # XYZ order

        if self.perform_resample == 'Voxels':
            new_spacing = self.voxel_spacing_target  # Already in XYZ order
            new_size = (original_size * original_spacing / new_spacing).astype(int).tolist()
        elif self.perform_resample == 'Shape':
            new_size = self.target_shape_xyz.astype(int).tolist()  # Already in XYZ order
            new_spacing = (original_spacing * original_size / new_size).tolist()
        else:
            return image_sitk  # No resampling needed

        if self.resample_order == 'Linear':
            sitk_resample = sitk.sitkLinear
        elif self.resample_order == 'BSpline':
            sitk_resample = sitk.sitkBSpline
        elif self.resample_order == 'Gaussian':
            sitk_resample = sitk.sitkGaussian
        elif self.resample_order == 'Cosine Windowed Sinc':
            sitk_resample = sitk.sitkCosineWindowedSinc
        elif self.resample_order == 'Hamming Windowed Sinc':
            sitk_resample = sitk.sitkHammingWindowedSinc
        elif self.resample_order == 'Nearest Neighbor':
            sitk_resample = sitk.sitkNearestNeighbor
        else:
            print(f"Resample order {self.resample_order} not supported. Using Linear.")
            sitk_resample = sitk.sitkLinear

        # Set up the resampler
        resampler = sitk.ResampleImageFilter()
        resampler.SetInterpolator(sitk_resample if not is_mask else sitk.sitkNearestNeighbor)
        resampler.SetOutputSpacing(new_spacing)
        resampler.SetSize(new_size)
        resampler.SetOutputDirection(image_sitk.GetDirection())
        resampler.SetOutputOrigin(image_sitk.GetOrigin())

        # Perform resampling
        resampled_image_sitk = resampler.Execute(image_sitk)
        return resampled_image_sitk

    def crop(self):
        # Implement cropping logic on self.image_sitk
        if not isinstance(self.image_sitk, list):
            self.image_sitk = self.crop_sitk_image(self.image_sitk)
        else:
            for i in range(len(self.image_sitk)):
                self.image_sitk[i] = self.crop_sitk_image(self.image_sitk[i])

    def crop_sitk_image(self, image_sitk):
        # Get the desired size from crop_entry
        target_size = self.crop_entry  # Assuming crop_entry is [size_x, size_y, size_z] in ZYX order

        # Convert target_size to XYZ order
        target_size_xyz = target_size[::-1]

        # Get current size
        current_size = image_sitk.GetSize()  # XYZ order

        # Calculate start index for cropping
        start_index = [
            int((current_size[i] - target_size_xyz[i]) / 2) if current_size[i] > target_size_xyz[i] else 0
            for i in range(3)
        ]

        # Calculate end index for cropping
        end_index = [
            start_index[i] + target_size_xyz[i] if current_size[i] > target_size_xyz[i] else current_size[i]
            for i in range(3)
        ]

        # Create a region of interest filter
        roi_filter = sitk.RegionOfInterestImageFilter()
        roi_filter.SetSize([end_index[i] - start_index[i] for i in range(3)])
        roi_filter.SetIndex(start_index)

        cropped_image_sitk = roi_filter.Execute(image_sitk)

        # If padding is needed
        desired_size = target_size_xyz
        actual_size = cropped_image_sitk.GetSize()
        size_difference = [desired_size[i] - actual_size[i] for i in range(3)]

        if any(s > 0 for s in size_difference):
            # Need to pad the image
            pad_filter = sitk.ConstantPadImageFilter()
            lower_pad = [int(np.floor(s / 2)) if s > 0 else 0 for s in size_difference]
            upper_pad = [int(np.ceil(s / 2)) if s > 0 else 0 for s in size_difference]
            pad_filter.SetPadLowerBound(lower_pad)
            pad_filter.SetPadUpperBound(upper_pad)
            pad_filter.SetConstant(0)

            cropped_image_sitk = pad_filter.Execute(cropped_image_sitk)

        return cropped_image_sitk

    def update_header(self):
        # Update header information if necessary
        # This function can be used to update self.header_in based on resampling or cropping
        if self.perform_resample == 'Voxels':
            # Since voxel_spacing_target is now in XYZ order, we need to adjust accordingly
            if self.format_in == 'dicom':
                self.header_in["Pixel Spacing"] = self.voxel_spacing_target[0:2]
                self.header_in["Spacing Between Slices"] = self.voxel_spacing_target[2]
            elif self.format_in == 'nifti':
                self.header_in['pixdim'][1:4] = self.voxel_spacing_target
            elif self.format_in == 'nrrd':
                self.header_in['space directions'] = self.voxel_spacing_target

        elif self.perform_resample == 'Shape' or self.perform_crop:
            if self.format_in == 'nifti':
                if not isinstance(self.image_sitk, list):
                    self.header_in["dim"][1:4] = self.image_sitk.GetSize()
                else:
                    self.header_in["dim"][1:4] = self.image_sitk[0].GetSize()
            elif self.format_in == 'nrrd':
                if not isinstance(self.image_sitk, list):
                    self.header_in['sizes'] = self.image_sitk.GetSize()
                else:
                    self.header_in['sizes'] = self.image_sitk[0].GetSize()

    def to_numpy(self):
        # Convert self.image_sitk back to numpy arrays and save
        if not isinstance(self.image_sitk, list):
            image_array = sitk.GetArrayFromImage(self.image_sitk)
            np.save(self.path_out + '.npy', image_array)
        else:
            for i, img_sitk in enumerate(self.image_sitk):
                image_array = sitk.GetArrayFromImage(img_sitk)
                np.save(self.file_save_paths[i] + '.npy', image_array)

    def to_nifti(self):
        # Save self.image_sitk directly
        if not isinstance(self.image_sitk, list):
            sitk.WriteImage(self.image_sitk, self.path_out + '.nii')
        else:
            for i, img_sitk in enumerate(self.image_sitk):
                sitk.WriteImage(img_sitk, self.file_save_paths[i] + '.nii')

    def to_nrrd(self):
        # Save self.image_sitk directly
        if not isinstance(self.image_sitk, list):
            sitk.WriteImage(self.image_sitk, self.path_out + '.nrrd')
        else:
            for i, img_sitk in enumerate(self.image_sitk):
                sitk.WriteImage(img_sitk, self.file_save_paths[i] + '.nrrd')

    def to_png(self):
        # Convert to numpy array and save as PNG
        if not isinstance(self.image_sitk, list):
            image_array = sitk.GetArrayFromImage(self.image_sitk)
            self.save_as_image(image_array, self.path_out + '.png', 'PNG')
        else:
            for i, img_sitk in enumerate(self.image_sitk):
                image_array = sitk.GetArrayFromImage(img_sitk)
                self.save_as_image(image_array, self.file_save_paths[i] + '.png', 'PNG')

    def to_jpeg(self):
        # Convert to numpy array and save as JPEG
        if not isinstance(self.image_sitk, list):
            image_array = sitk.GetArrayFromImage(self.image_sitk)
            self.save_as_image(image_array, self.path_out + '.jpg', 'JPEG')
        else:
            for i, img_sitk in enumerate(self.image_sitk):
                image_array = sitk.GetArrayFromImage(img_sitk)
                self.save_as_image(image_array, self.file_save_paths[i] + '.jpg', 'JPEG')

    def save_as_image(self, image_array, file_path, format_out):
        # Normalize image data
        image_array = normalise_natural(image_array)

        # Correct for shapes
        if len(image_array.shape) == 3:
            if image_array.shape[0] == 1 or image_array.shape[0] == 3 or image_array.shape[0] == 4:
                image_array = image_array.transpose(1, 2, 0)
            elif image_array.shape[2] not in [3, 4]:
                image_array = image_array[:, :, 0]

        image_pil = Image.fromarray(image_array)

        # Check if the image has an alpha channel (RGBA mode)
        if image_pil.mode == 'RGBA' and format_out == 'JPEG':
            # Convert RGBA image to RGB mode
            image_pil = image_pil.convert('RGB')

        # Save the image in the specified output format
        image_pil.save(file_path, format=format_out)

    def to_dicom(self):
        os.makedirs(self.path_out, exist_ok=True)

        dicom_header = self.sitk_to_dicom_header()

        # Generate unique series and study UIDs
        series_instance_uid = dicom_header.get("Series Instance UID", pydicom.uid.generate_uid())
        study_instance_uid = dicom_header.get("Study Instance UID", pydicom.uid.generate_uid())
        frame_of_reference_uid = dicom_header.get("Frame of Reference UID", pydicom.uid.generate_uid())
        implementation_class_uid = pydicom.uid.PYDICOM_IMPLEMENTATION_UID  # Unsure whether necessary

        image_array = sitk.GetArrayFromImage(self.image_sitk)
        image_array = zyx_to_xyz(image_array)

        for i in range(image_array.shape[2]):  # Note: image_array is in ZYX order after GetArrayFromImage
            sop_instance_uid = pydicom.uid.generate_uid()  # Generate a unique SOPInstanceUID for each slice

            slice_info_dict = {
                'dicom_header': dicom_header,
                'image': image_array,
                'series_instance_uid': series_instance_uid,
                'study_instance_uid': study_instance_uid,
                'frame_of_reference_uid': frame_of_reference_uid,
                'implementation_class_uid': implementation_class_uid,
                'sop_instance_uid': sop_instance_uid,
                'iteration': i,
                'plane': anatomical_plane_dicom(dicom_header['Image Orientation (Patient)'])
            }

            data = prepare_dicom_slice(slice_info_dict)
            dicom_file_path = os.path.join(self.file_save_paths[0], f'{sop_instance_uid}.dcm')
            pydicom.dcmwrite(dicom_file_path, data, write_like_original=False)

    def sitk_to_dicom_header(self):
        image = self.image_sitk
        header = {}

        # Basic metadata from the SimpleITK image
        header['Image Position (Patient)'] = list(image.GetOrigin())
        header['Image Orientation (Patient)'] = list(image.GetDirection()[:6])  # Ensure exactly 6 values
        header['Pixel Spacing'] = list(image.GetSpacing()[:2])
        header['Slice Thickness'] = float(image.GetSpacing()[2]) if len(image.GetSpacing()) > 2 else 1.0

        # Determine pixel depth and related fields based on SimpleITK PixelID
        pixel_id = image.GetPixelID()
        if pixel_id == sitk.sitkUInt8:
            header['Bits Allocated'] = 8
            header['Bits Stored'] = 8
            header['High Bit'] = 7
            header['Samples per Pixel'] = 1
            header['Pixel Representation'] = 0  # Unsigned
        elif pixel_id == sitk.sitkUInt16:
            header['Bits Allocated'] = 16
            # Determine Bits Stored based on actual data range or predefined standard
            # Assuming 12 bits for medical images like CT
            header['Bits Stored'] = 12  
            header['High Bit'] = 11
            header['Samples per Pixel'] = 1
            header['Pixel Representation'] = 0  # Unsigned
        elif pixel_id == sitk.sitkInt16:
            header['Bits Allocated'] = 16
            header['Bits Stored'] = 16
            header['High Bit'] = 15
            header['Samples per Pixel'] = 1
            header['Pixel Representation'] = 1  # Signed
        elif pixel_id == sitk.sitkFloat32:
            header['Bits Allocated'] = 32
            header['Bits Stored'] = 32
            header['High Bit'] = 31
            header['Samples per Pixel'] = 1
            header['Pixel Representation'] = 0  # Typically, floating-point images use unsigned
        elif pixel_id == sitk.sitkFloat64:
            header['Bits Allocated'] = 64
            header['Bits Stored'] = 64
            header['High Bit'] = 63
            header['Samples per Pixel'] = 1
            header['Pixel Representation'] = 0  # Typically, floating-point images use unsigned
        else:
            # Default fallback
            header['Bits Allocated'] = 8
            header['Bits Stored'] = 8
            header['High Bit'] = 7
            header['Samples per Pixel'] = 1
            header['Pixel Representation'] = 0  # Unsigned

        # Determine Photometric Interpretation
        # Assuming 'MONOCHROME2' for single-channel images and 'RGB' for three-channel images
        if header['Samples per Pixel'] == 1:
            header['Photometric Interpretation'] = 'MONOCHROME2'
        elif header['Samples per Pixel'] == 3:
            header['Photometric Interpretation'] = 'RGB'
        else:
            # Handle other cases or raise an error
            header['Photometric Interpretation'] = 'MONOCHROME2'  # Defaulting to grayscale

        # Rescale Slope and Intercept
        # These can be adjusted based on your specific needs or image properties
        header['Rescale Slope'] = 1.0
        header['Rescale Intercept'] = 0.0

        # Image Dimensions
        header['Rows'] = int(image.GetSize()[1])    # SizeY -> Rows
        header['Columns'] = int(image.GetSize()[0]) # SizeX -> Columns

        # Image Type and Plane
        header['Image Type'] = "DERIVED\\PRIMARY"
        header['plane'] = anatomical_plane_dicom(header['Image Orientation (Patient)'])
        
        return header

    def replace_disallowed_chars(self, filename):
        replacements = {
            '*': '_asterisk_',
            '@': '_at_',
            '%': '_percent_',
            ':': '_colon_',
            '/': '_slash_',
            '\\': '_backslash_',
            '?': '_question_',
            '<': '_less_than_',
            '>': '_greater_than_',
            '|': '_pipe_',
            '"': '_quote_'
        }

        # Replace each character in the filename according to the dictionary
        for char, replacement in replacements.items():
            filename = filename.replace(char, replacement)

        return filename