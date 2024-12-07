#%%
import numpy as np
import pydicom
import re
import os
import ast

from header_map import *

#%% DICOM to NiFTI Conversion Functions

def mean_slice_spacing(dicom_folder):
    """
    Calculate the mean difference between the slice locations in a DICOM folder.
    This is needed because the slice thickness tag is not equivalent to slice separation.
    Doesn't do well with highly oblique images since rotation hasn't been applied.

    Parameters:
    dicom_folder (str): Path to the folder containing DICOM files.

    Returns:
    float: Mean difference between slice locations in millimeters (mm), or None if not applicable.
    """
    dot_products = []  

    # Determine whether axial, sagittal, or coronal slices are present
    # by checking the Image Orientation (Patient) tag
    
    # Loop over every file in the DICOM folder
    for filename in os.listdir(dicom_folder):

        # Check if filename is a DICOM file by attempting to load with pydicom
        is_dicom = False
        is_rtss_dose_plan = False
        try:
            ds = pydicom.dcmread(os.path.join(dicom_folder, filename), stop_before_pixels=True)
            is_dicom = True

            if ds.Modality in ['RTDOSE', 'RTSTRUCT', 'RTPLAN']:
                is_rtss_dose_plan = True
        except:
            pass
        if is_dicom and not is_rtss_dose_plan:
            file_path = os.path.join(dicom_folder, filename)
            ds = pydicom.dcmread(file_path, stop_before_pixels=True)

            origin = ds.ImagePositionPatient
            orientation = ds.ImageOrientationPatient
            col_i = orientation[0:3]
            col_j = orientation[3:6]
            col_k = np.cross(col_i, col_j)
            dotp = np.dot(col_k, origin)
            dot_products.append(dotp)


    # Sort the slice locations from smallest to largest
    dot_products.sort()

    # Calculate mean difference between consecutive slices
    if len(dot_products) > 1:
        differences = [dot_products[i+1] - dot_products[i] for i in range(len(dot_products) - 1)]
        mean_diff = np.mean(differences)
        return mean_diff
    else:
        return None

def dicom_to_nifti_pixdim(dicom_header_dict, path_in):

    # Get slice spacing
    try:
        z_spacing = dicom_header_dict["Spacing Between Slices"]
    except:
        z_spacing = mean_slice_spacing(path_in)

    # Extract pixel spacing and slice thickness from the DICOM header dictionary
    pixel_spacing = list(dicom_header_dict['Pixel Spacing'])  # Convert MultiValue to list

    # Construct the pixdim array starting with index 0 as per NIfTI specification
    # Start with a list of 8 ones, then overwrite the relevant first few
    pixdim = [1] * 8
    pixdim[1:len(pixel_spacing) + 1] = pixel_spacing
    pixdim[3] = z_spacing
    
    return pixdim

def dicom_to_nifti_affine(dicom_header_dict, path_in):

    image_orientation = dicom_header_dict['Image Orientation (Patient)']
    image_position = dicom_header_dict['Image Position (Patient)']
    pixel_spacing = dicom_header_dict['Pixel Spacing']
    try:
        z_spacing = dicom_header_dict["Spacing Between Slices"]
    except:
        z_spacing = mean_slice_spacing(path_in)

    # Convert the input lists to numpy arrays
    image_orientation = np.array(image_orientation)
    image_position = np.array(image_position)
    pixel_spacing = np.array(pixel_spacing)

    # Decompose the image_orientation into row (image_i) and column (image_j) direction cosines
    image_i = image_orientation[:3]
    image_j = image_orientation[3:]

    # The cross product gives the slice direction (image_k)
    image_k = np.cross(image_i, image_j)

    # Scale image_i and image_j by pixel spacing, and image_k by slice thickness
    image_i *= pixel_spacing[0]
    image_j *= pixel_spacing[1]
    image_k *= z_spacing

    # Construct the affine transformation matrix
    IJKtoLPS = np.eye(4)
    IJKtoLPS[:3, 0] = image_i
    IJKtoLPS[:3, 1] = image_j
    IJKtoLPS[:3, 2] = image_k
    IJKtoLPS[:3, 3] = image_position

    # Convert the matrix from to RAS
    LPStoRAS = np.diag([-1, -1, 1, 1])
    IJKtoRAS = np.dot(LPStoRAS, IJKtoLPS)
    affine_matrix = IJKtoRAS

    return affine_matrix

def anatomical_plane_dicom(image_orientation):
    # Convert the image_orientation to a 2D array for easier manipulation
    image_orientation = np.array(image_orientation).reshape(2, 3)
    
    # Calculate the row and column direction cosines
    row_cosines = image_orientation[0]
    col_cosines = image_orientation[1]
    
    # Define the standard orientation vectors for Axial, Coronal, and Sagittal
    axial = [np.array([1, 0, 0]), np.array([0, 1, 0]), np.array([0, 0, 1])]
    coronal = [np.array([1, 0, 0]), np.array([0, 0, 1]), np.array([0, 1, 0])]
    sagittal = [np.array([0, 1, 0]), np.array([0, 0, 1]), np.array([1, 0, 0])]
    
    # Compute dot products
    axial_score = abs(np.dot(row_cosines, axial[0])) + abs(np.dot(col_cosines, axial[1]))
    coronal_score = abs(np.dot(row_cosines, coronal[0])) + abs(np.dot(col_cosines, coronal[1]))
    sagittal_score = abs(np.dot(row_cosines, sagittal[0])) + abs(np.dot(col_cosines, sagittal[1]))
    
    # Determine the closest orientation
    if axial_score >= coronal_score and axial_score >= sagittal_score:
        return "axial"
    elif coronal_score >= axial_score and coronal_score >= sagittal_score:
        return "coronal"
    elif sagittal_score >= axial_score and sagittal_score >= coronal_score:
        return "sagittal"
    else:
        return "Unknown orientation"

# def anatomical_plane_dicom(image_orientation):
#     print('image_orientation', image_orientation)
#     image_orientation = np.array(image_orientation).reshape(2, 3)
#     row_cosines = image_orientation[0]
#     col_cosines = image_orientation[1]
#     normal_vector = np.cross(row_cosines, col_cosines)
#     abs_normal = np.abs(normal_vector)
#     max_index = np.argmax(abs_normal)
#     if max_index == 0:
#         return 'sagittal'
#     elif max_index == 1:
#         return 'coronal'
#     elif max_index == 2:
#         return 'axial'


def anatomical_plane_nifti(nifti_img_sitk):
    # Get the affine transformation matrix
    affine = np.array(nifti_img_sitk.GetDirection()).reshape(3, 3)
    
    # Extract the rotation part of the affine matrix
    rotation_matrix = affine[:3, :3]
    
    # Calculate the direction cosines for each axis
    x_cosine = rotation_matrix[:, 0]
    y_cosine = rotation_matrix[:, 1]
    z_cosine = rotation_matrix[:, 2]
    
    # Define the standard orientation vectors for Axial, Coronal, and Sagittal
    axial = [np.array([1, 0, 0]), np.array([0, 1, 0]), np.array([0, 0, 1])]
    coronal = [np.array([1, 0, 0]), np.array([0, 0, 1]), np.array([0, 1, 0])]
    sagittal = [np.array([0, 1, 0]), np.array([0, 0, 1]), np.array([1, 0, 0])]
    
    # Compute dot products
    axial_score = abs(np.dot(x_cosine, axial[0])) + abs(np.dot(y_cosine, axial[1])) + abs(np.dot(z_cosine, axial[2]))
    coronal_score = abs(np.dot(x_cosine, coronal[0])) + abs(np.dot(y_cosine, coronal[1])) + abs(np.dot(z_cosine, coronal[2]))
    sagittal_score = abs(np.dot(x_cosine, sagittal[0])) + abs(np.dot(y_cosine, sagittal[1])) + abs(np.dot(z_cosine, sagittal[2]))
    
    # Determine the closest orientation
    if axial_score >= coronal_score and axial_score >= sagittal_score:
        return "axial"
    elif coronal_score >= axial_score and coronal_score >= sagittal_score:
        return "coronal"
    elif sagittal_score >= axial_score and sagittal_score >= coronal_score:
        return "sagittal"
    else:
        return "Unknown orientation"


def anatomical_plane_nrrd(nrrd_header):
    # Extract the space directions from the header
    space_directions = nrrd_header['space directions']
    
    # Convert the space directions to a numpy array for easier manipulation
    space_directions = np.array(space_directions)
    
    print('space directions for plane', space_directions)
    
    # Calculate the direction cosines for each axis
    x_cosine = space_directions[0]
    y_cosine = space_directions[1]
    z_cosine = space_directions[2]
    
    # Define the standard orientation vectors for Axial, Coronal, and Sagittal
    axial = [np.array([1, 0, 0]), np.array([0, 1, 0]), np.array([0, 0, 1])]
    coronal = [np.array([1, 0, 0]), np.array([0, 0, 1]), np.array([0, 1, 0])]
    sagittal = [np.array([0, 1, 0]), np.array([0, 0, 1]), np.array([1, 0, 0])]
    
    # Compute dot products
    axial_score = abs(np.dot(x_cosine, axial[0])) + abs(np.dot(y_cosine, axial[1])) + abs(np.dot(z_cosine, axial[2]))
    coronal_score = abs(np.dot(x_cosine, coronal[0])) + abs(np.dot(y_cosine, coronal[1])) + abs(np.dot(z_cosine, coronal[2]))
    sagittal_score = abs(np.dot(x_cosine, sagittal[0])) + abs(np.dot(y_cosine, sagittal[1])) + abs(np.dot(z_cosine, sagittal[2]))
    
    # Determine the closest orientation
    if axial_score >= coronal_score and axial_score >= sagittal_score:
        return "axial"
    elif coronal_score >= axial_score and coronal_score >= sagittal_score:
        return "coronal"
    elif sagittal_score >= axial_score and sagittal_score >= coronal_score:
        return "sagittal"
    else:
        return "Unknown orientation"

def plane_to_image_type(plane):
    if plane == 'axial':
        image_type = ['ORIGINAL', 'PRIMARY', 'AXIAL']
    elif plane == 'sagittal':
        image_type = ['ORIGINAL', 'PRIMARY', 'SAGITTAL']
    elif plane == 'coronal':
        image_type = ['ORIGINAL', 'PRIMARY', 'CORONAL']
    return image_type

def dicom_to_nifti_datatype(dicom_header_dict):
    pixel_representation, bits_allocated = dicom_header_dict['Pixel Representation'], dicom_header_dict['Bits Allocated']

    # NIfTI datatype codes based on combination of Pixel Representation and Bits Allocated
    datatype_map = {
        (0, 8): (2, 8),     # UINT8 (8-bit unsigned integer)
        (1, 8): (256, 8),   # INT8 (8-bit signed integer)
        (0, 16): (512, 16), # UINT16 (16-bit unsigned integer)
        (1, 16): (4, 16),   # INT16 (16-bit signed integer)
        (0, 32): (768, 32), # UINT32 (32-bit unsigned integer)
        (1, 32): (8, 32),   # INT32 (32-bit signed integer)
        # Add more mappings if necessary for different bit depths like 64-bit
        (0, 64): (1280, 64), # UINT64 (64-bit unsigned integer)
        (1, 64): (1024, 64)  # INT64 (64-bit signed integer)
    }

    # Get the NIfTI datatype code and bitpix value from the map
    # based on the given pixel representation and bits allocated
    data_type_and_bitpix = datatype_map.get((pixel_representation, bits_allocated))

    # Handle the case where no matching datatype is found
    if data_type_and_bitpix is None:
        raise ValueError("Unsupported combination of pixel representation and bits allocated")

    # Unpack the datatype and bitpix values
    data_type, bitpix = data_type_and_bitpix

    return data_type, bitpix

def numpy_to_nifti_dim(output_nifti):
    numpy_array = output_nifti.get_fdata()

    # numpy_array is a numpy array with DICOM image data
    shape = list(numpy_array.shape)
    
    # Initialize the dim array with up to 8 elements, defaulting to 0
    dim = [0] * 8
    
    # Set the first element to the number of dimensions that contain data
    dim[0] = len(shape)
    
    # Fill the next elements with the dimensions from the numpy array shape
    for i in range(1, len(shape) + 1):
        dim[i] = shape[i - 1]

    return dim

def dicom_to_nifti_scl_slope(dicom_header_dict):
    """Not yet tested"""
    # Default slope and intercept
    scl_slope = 1.0
    scl_inter = 0.0
    
    # Extract Rescale Slope if present
    if 'Rescale Slope' in dicom_header_dict:
        scl_slope = dicom_header_dict['Rescale Slope']
    else:
        scl_slope = 1.0  # Default to 1 if not present
    # Extract Rescale Intercept if present
    if 'Rescale Intercept' in dicom_header_dict:
        scl_inter = dicom_header_dict['Rescale Intercept']
    else:
        scl_inter = 0.0
    
    return scl_slope, scl_inter

#%% DICOM to NRRD Conversion Functions

import numpy as np

def dicom_to_nrrd_sizes(dicom_header_dict):
    rows = dicom_header_dict['Rows']
    columns = dicom_header_dict['Columns']
    return [columns, rows]

def dicom_to_nrrd_thicknesses(dicom_header_dict, path_in):
    pixel_spacing = list(map(float, dicom_header_dict.get('Pixel Spacing', (1.0, 1.0))))
    slice_spacing = dicom_header_dict.get('Spacing Between Slices', mean_slice_spacing(path_in))
    if pixel_spacing == None:
        pixel_spacing = [1.0, 1.0]
    if slice_spacing == None:
        slice_spacing = 1.0
    slice_spacing = float(slice_spacing)
    print(pixel_spacing, slice_spacing)
    return pixel_spacing + [slice_spacing]

def dicom_to_nrrd_type(dicom_header_dict):
    pixel_representation = dicom_header_dict['Pixel Representation']
    bits_allocated = dicom_header_dict['Bits Allocated']

    return DICOM_TO_NRRD_TYPE_MAP.get((pixel_representation, bits_allocated), 'unknown')

def dicom_to_nrrd_endian(dicom_header_dict):
    return 'little' if dicom_header_dict.get('High Bit', 0) < 8 else 'big'

def dicom_to_nrrd_origin(dicom_header_dict):
    image_position = list(map(float, dicom_header_dict['Image Position (Patient)']))
    return image_position

def dicom_to_nrrd_space_directions(dicom_header_dict, path_in):

    image_orientation_patient = list(map(float, dicom_header_dict.get('Image Orientation (Patient)', (1.0, 0.0, 0.0, 0.0, 1.0, 0.0))))
    col_i = np.array(image_orientation_patient[:3])
    col_j = np.array(image_orientation_patient[3:])
    col_k = np.cross(col_i, col_j)

    pixel_spacing = list(map(float, dicom_header_dict.get('Pixel Spacing', (1.0, 1.0))))
    slice_spacing = dicom_header_dict.get('Spacing Between Slices', mean_slice_spacing(path_in))
    slice_spacing = float(slice_spacing)

    col_i *= pixel_spacing[0]
    col_j *= pixel_spacing[1]
    col_k *= slice_spacing

    combined = np.array([col_i, col_j, col_k])

    return combined


#%% Nifti to Nifti Conversion Functions

def nifti_to_nifti_pixdim(header_in):

    pixdim = header_in["pixdim"]
    pixdim = parse_srow(pixdim)
    
    return pixdim

def nifti_to_nifti_affine(header_in):

    srow_x = parse_srow(header_in["srow_x"])
    srow_y = parse_srow(header_in["srow_y"])
    srow_z = parse_srow(header_in["srow_z"])

    # Add dummy row
    dummy_row = np.array([0, 0, 0, 1])

    affine = np.array([srow_x, srow_y, srow_z, dummy_row])

    return affine    

def nifti_to_nifti_datatype_bitpix(header_in):

    datatype = header_in["datatype"]

    bitpix = header_in["bitpix"]

    return datatype, bitpix


#%% NiFTI to DICOM Conversion Functions

import numpy as np

def parse_srow(srow_str):
    # Replace newline characters with nothing, then strip square brackets, and finally split by spaces
    numbers = srow_str.replace('\n', '').strip('[]').split()
    return np.array([float(num) for num in numbers])

def nifti_to_dicom_image_pos_patient(header_in):
    return [-float(header_in['qoffset_x']), -float(header_in['qoffset_y']), float(header_in['qoffset_z'])]

def nifti_to_dicom_image_orient(header_in):
    srow_x = parse_srow(header_in['srow_x'])
    srow_y = parse_srow(header_in['srow_y'])
    srow_z = parse_srow(header_in['srow_z'])

    IJKtoRAS = np.array([srow_x, srow_y, srow_z]) # Combine into a 3x4 matrix

    pixel_spacing_i, pixel_spacing_j, pixel_spacing_k = nifti_to_dicom_pixel_spacing(header_in) # Get the pixel spacing
    
    # Divide each column by the corresponding pixel spacing directly
    IJKtoRAS[:, 0] /= pixel_spacing_i
    IJKtoRAS[:, 1] /= pixel_spacing_j
    IJKtoRAS[:, 2] /= pixel_spacing_k

    RAStoLPS = np.array([
        [-1,  0,  0],
        [ 0, -1,  0],
        [ 0,  0,  1],
    ])

    IJKtoLPS = np.dot(RAStoLPS, IJKtoRAS)

    # Get first two Columns
    i = IJKtoLPS[:, 0]
    j = IJKtoLPS[:, 1]

    # Return as a list of 6 values
    return i.tolist() + j.tolist()

def nifti_to_dicom_pixel_spacing(header_in):
    # This actually the slice spacing rather than slice thickness, which are not always the same.
    pixdim = parse_srow(header_in['pixdim'])
    return [pixdim[1], pixdim[2], pixdim[3]]

def nifti_to_dicom_datatype(header_in):
    """
    Convert NIfTI data type to equivalent DICOM data type and bit depth.
    
    Args:
    header_in (dict): A dictionary containing NIfTI header information.
    
    Returns:
    tuple: A tuple containing the bit depth and the DICOM Photometric Interpretation.
           If the datatype is not recognized, it returns the bit depth from the 'bitpix'
           field of the header with 'UNKNOWN' as the Photometric Interpretation.
    """
    # NIfTI numeric datatype codes to human-readable format
    nifti_dtype_map = {
        2: 'uint8',     # DT_UINT8, unsigned char
        4: 'int16',     # DT_INT16, signed short
        8: 'int32',     # DT_INT32, signed int
        16: 'float32',  # DT_FLOAT32, 32 bit float
        64: 'float64',  # DT_FLOAT64, 64 bit float
        256: 'int8',    # DT_INT8, signed char
        512: 'uint16',  # DT_UINT16, unsigned short (for example)
        # Add additional NIfTI types as necessary
    }
    
    # Mapping of human-readable NIfTI data types to DICOM (bits allocated, Photometric Interpretation)
    dtype_dicom_map = {
        'uint8': (8, 'MONOCHROME2'),   # Using MONOCHROME2 for unsigned data
        'int16': (16, 'MONOCHROME2'),
        'int8': (8, 'MONOCHROME2'),
        'uint16': (16, 'MONOCHROME2'),
        'int32': (32, 'MONOCHROME2'),
        'float32': (32, 'MONOCHROME2'),
        'float64': (64, 'MONOCHROME2'),
    }
    
    # Retrieve the numeric data type from the header, default to 2 (uint8) if not specified
    nifti_datatype_code = int(header_in.get('datatype', 2))  # Defaulting to 2 as an example
    
    # Convert numeric NIfTI datatype code to human-readable format
    human_readable_type = nifti_dtype_map.get(nifti_datatype_code, 'unknown')

    # Get the mapping from dtype_dicom_map; if datatype is not in the map, use 'bitpix' and 'UNKNOWN'
    bits_allocated, photometric_interpretation = dtype_dicom_map.get(human_readable_type, (header_in.get('bitpix', 8), 'UNKNOWN'))
    
    return int(bits_allocated), photometric_interpretation

def nifti_to_dicom_scl_slope(header_in):
    return float(header_in['scl_slope']), float(header_in['scl_inter'])

def nifti_to_dicom_dim(image):
    return [image.shape[1], image.shape[0]]


#%% NiFTI to NRRD Conversion Functions

def parse_srow(srow_str):
    # Replace newline characters with nothing, then strip square brackets, and finally split by spaces
    numbers = srow_str.replace('\n', '').strip('[]').split()
    return np.array([float(num) for num in numbers])

def nifti_to_nrrd_sizes(header_in):
    dim = header_in['dim']
    dim = parse_srow(dim)
    dim = [int(x) for x in dim]
    sizes = [dim[1], dim[2], dim[3]]
    return sizes

def nifti_to_nrrd_thicknesses(header_in):
    thicknesses = header_in['pixdim']
    thicknesses = parse_srow(thicknesses)
    thicknesses = [float(x) for x in thicknesses]
    thicknesses = [thicknesses[1], thicknesses[2], thicknesses[3]]
    return thicknesses

def nifti_to_nrrd_type(header_in):
    nifti_to_nrrd_type_map = {
        2: 'uint8',
        4: 'int16',
        8: 'int32',
        16: 'float',
        64: 'double',
        256: 'int8',
        512: 'uint16',
        768: 'uint32',
        1024: 'int64',
        1280: 'uint64'
    }
    nifti_datatype = int(header_in['datatype'])
    nrrd_datatype = nifti_to_nrrd_type_map.get(nifti_datatype, 'unknown')
    return nrrd_datatype

def nifti_to_nrrd_endian(header_in):
    # Check the sizeof_hdr field to determine the endian type
    sizeof_hdr = header_in.get('sizeof_hdr', None)
    
    if sizeof_hdr is None:
        raise ValueError("Invalid NIfTI header: 'sizeof_hdr' field is missing.")

    if int(sizeof_hdr) == 348:
        return "little"
    elif int(sizeof_hdr) == 1543569408:
        return "big"
    else:
        raise ValueError("Unrecognized 'sizeof_hdr' value. Cannot determine endian type.")


def nifti_to_nrrd_origin(header_in):
    origin = [header_in['qoffset_x'], header_in['qoffset_y'], header_in['qoffset_z']]
    origin = [float(x) for x in origin]
    return origin

def nifti_to_nrrd_space_directions(header_in):
    srow_x = parse_srow(header_in['srow_x'])[:-1]
    srow_y = parse_srow(header_in['srow_y'])[:-1]
    srow_z = parse_srow(header_in['srow_z'])[:-1]
    space_directions = np.array([srow_x, srow_y, srow_z])
    space_directions = np.dot(np.diag([-1,-1,1]), space_directions).T
    return space_directions


#%% NRRD to NRRD Conversion Functions

def nrrd_to_nrrd_sizes(header_in):
    sizes = parse_space_directions_or_origin(header_in['sizes'])
    return sizes

def nrrd_to_nrrd_space_directions(header_in):
    space_directions = parse_space_directions_or_origin(header_in['space directions'])
    return space_directions

def nrrd_to_nrrd_space_origin(header_in):
    space_origin = parse_space_directions_or_origin(header_in['space origin'])
    return space_origin

def nrrd_to_nrrd_kinds(header_in):
    kinds = header_in['kinds']
    result = ast.literal_eval(kinds)
    if isinstance(result, list):
        return result
    else:
        return "The provided string does not represent a list."


#%% NRRD to DICOM Conversion Functions

import numpy as np

def nrrd_to_dicom_pixel_spacing(header):
    """Extract pixel spacing and slice thickness from NRRD header using spacings or space directions."""
    if 'spacings' in header:
        spacing = header['spacings']
        spacing = parse_space_directions_or_origin(spacing)
        return [float(spacing[0]), float(spacing[1]), float(spacing[2])]
    elif 'space directions' in header:
        # Extract the space directions and compute the norms of the vectors for pixel and slice spacing
        
        directions = header['space directions']
        directions = parse_space_directions_or_origin(directions)
        pixel_spacing_i = np.linalg.norm(directions[0])
        pixel_spacing_j = np.linalg.norm(directions[1])
        slice_thickness = np.linalg.norm(directions[2]) if len(directions) > 2 else 1.0
        return [pixel_spacing_i, pixel_spacing_j, slice_thickness]
    else:
        return [1.0, 1.0, 1.0]  # Default spacing if neither key is present

def nrrd_to_dicom_image_orient(header, pixel_spacing):
    """Convert directions from NRRD to DICOM orientation format."""
    if 'space directions' in header:
        directions = header['space directions']
        directions = parse_space_directions_or_origin(directions)
        col_i, col_j = np.array(directions[0]), np.array(directions[1])
        col_i /= pixel_spacing[0]
        col_j /= pixel_spacing[1]
        return list(col_i[:3]) + list(col_j[:3])
    else:
        return [1.0, 0.0, 0.0, 0.0, 1.0, 0.0]  # Default orientation if not present

def nrrd_to_dicom_image_pos_patient(header):
    """Convert origin from NRRD to DICOM."""
    origin = header['space origin']
    origin = parse_space_directions_or_origin(origin)
    return origin

def nrrd_to_dicom_dim(image):
    """Extract image dimensions from NRRD."""
    return [image.shape[1], image.shape[0]]

def nrrd_to_dicom_datatype(header):
    """Determine data type and photometric interpretation from NRRD header."""
    datatype = header.get('type', 'unknown')
    return NRRD_TO_DICOM_TYPE_MAP.get(datatype, (0, 'unknown'))

#%% NRRD to NiFTI Conversion Functions

def nrrd_to_nifti_orientation(nrrd_header):
    """
    Extracts and converts the NRRD 'space directions' and 'space origin' 
    to an orientation matrix for NIfTI.
    """
    try:
        # Extract the space directions
        space_directions_str = nrrd_header['space directions']
        if isinstance(space_directions_str, str):
            space_directions = parse_space_directions_or_origin(space_directions_str)
        else:
            space_directions = np.array(space_directions_str)

        # Extract the space origin
        space_origin_str = nrrd_header['space origin']
        space_origin = parse_space_directions_or_origin(space_origin_str)

        # Convert from LPS to RAS if necessary
        convert_lps_to_ras = np.diag([-1, -1, 1])
        space_directions_ras = np.dot(convert_lps_to_ras, space_directions.T).T

        # Create the 4x4 affine transformation matrix
        affine_4x4 = np.eye(4)
        affine_4x4[:3, :3] = space_directions_ras
        affine_4x4[:3, 3] = np.dot(convert_lps_to_ras, space_origin)  # Set the translation part

        return affine_4x4
    except KeyError as e:
        raise KeyError(f"Key error in the header: {e}")
    except ValueError as e:
        raise ValueError(f"Failed to process space directions or origin: {e}")

def parse_space_directions_or_origin(space_directions_str):
    """
    Parses a string representation of space directions into a NumPy array,
    ensuring uniform dimensionality and correctly handling scientific notation.
    """
    # Properly handle scientific notation by keeping 'e+' and 'e-' intact
    cleaned_str = re.sub(r'(?<!e)[^\d\.\-e\+]', ' ', space_directions_str)

    # Remove any extra white spaces
    elements = re.sub(r'\s+', ' ', cleaned_str).strip()

    # Assuming 'elements' is a space-separated string of numbers in scientific notation
    rows = elements.split(' ')
    # Group every three elements into a sublist to form rows
    rows = [rows[i:i+3] for i in range(0, len(rows), 3)]

    matrix = []
    for row in rows:
        try:
            float_nums = [float(num) for num in row]
            matrix.append(float_nums)
        except ValueError as e:
            raise ValueError(f"Error converting to float in row '{row}': {e}")

    # Ensure uniform dimensions across all rows
    if not all(len(row) == len(matrix[0]) for row in matrix):
        raise ValueError("Inconsistent dimensions found in space directions.")

    matrix = np.array(matrix)

    # If there is only one row it is an origin and should be a 1D array
    if len(matrix) == 1:
        matrix = matrix[0]

    return matrix

def nrrd_to_nifti_pixdim(nrrd_header):
    """
    Extracts pixel dimensions from the NRRD 'space directions' header.
    Handles space directions provided as a string and ensures consistency.
    """
    space_directions_str = nrrd_header.get('space directions', None)
    if space_directions_str:
        if isinstance(space_directions_str, str):
            space_directions = parse_space_directions_or_origin(space_directions_str)
        else:
            space_directions = np.array(space_directions_str)
    else:
        raise ValueError("Space directions are missing or in an unrecognized format.")

    pixdim_final = [1] * 8
    # pixdim[1:len(pixel_spacing) + 1] = pixel_spacing
    # pixdim[3] = z_spacing

    # Calculate pixel dimensions
    pix_dim = np.sqrt(np.sum(np.square(space_directions), axis=1))
    pixdim_final[1:len(pix_dim) + 1] = pix_dim
    

    return pixdim_final

def nrrd_to_nifti_datatype(nrrd_header):
    """
    Determines the NIfTI datatype and bits per pixel from the NRRD header's 'type' field.
    Maps common NRRD data types to NIfTI data types.
    """
    nrrd_type_to_nifti = {
        'uint8': (2, 8),
        'int16': (4, 16),
        'int32': (8, 32),
        'float': (16, 32),
        'double': (64, 64),
        'int8': (256, 8),
        'uint16': (512, 16),
        'uint32': (768, 32),
        'int64': (1024, 64),
        'uint64': (1280, 64),
        'short': (4, 16)  # assuming 'short' is a synonym for 'int16'
    }
    nrrd_type = nrrd_header.get('type')  # Safer access using get
    if nrrd_type not in nrrd_type_to_nifti:
        raise ValueError(f"Unsupported NRRD data type: {nrrd_type}")
    return nrrd_type_to_nifti[nrrd_type]

def nrrd_to_nifti_scl_slope(nrrd_header):
    """
    Calculates scale slope and intercept for NIfTI from the NRRD header.
    Default slope and intercept are returned if not specified in the header.
    """
    # Default values
    scl_slope = 1.0
    scl_inter = 0.0

    # If the NRRD header specifies scaling, use those values
    if 'scl_slope' in nrrd_header and 'scl_inter' in nrrd_header:
        scl_slope = float(nrrd_header['scl_slope'])
        scl_inter = float(nrrd_header['scl_inter'])

    return scl_slope, scl_inter
