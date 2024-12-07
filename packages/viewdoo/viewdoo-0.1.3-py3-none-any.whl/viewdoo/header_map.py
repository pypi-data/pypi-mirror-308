# Dictionary of DICOM modalities and their SOPClassUIDs
DICOM_MODALITIES = {
    "CT": "1.2.840.10008.5.1.4.1.1.2",
    "MRI": "1.2.840.10008.5.1.4.1.1.4",
    "PET": "1.2.840.10008.5.1.4.1.1.128",
    "Ultrasound": "1.2.840.10008.5.1.4.1.1.6.1",
    "Cardiac Ultrasound": "1.2.840.1  0008.5.1.4.1.1.3.1",
    "Digital Subtraction Angiography (DSA)": "1.2.840.10008.5.1.4.1.1.12.1",
    "Intravascular Optical Coherence Tomography (IVOCT)": "1.2.840.10008.5.1.4.1.1.14.1",
    "Mammography": "1.2.840.10008.5.1.4.1.1.1.2",
    "Digital Radiography (DR)": "1.2.840.10008.5.1.4.1.1.1",
    "General Nuclear Medicine": "1.2.840.10008.5.1.4.1.1.20",
    "SPECT": "1.2.840.10008.5.1.4.1.1.3",
    "Fluoroscopy": "1.2.840.10008.5.1.4.1.1.12.2",
    "Computed Radiography (CR)": "1.2.840.10008.5.1.4.1.1.1",
    "Breast Tomosynthesis": "1.2.840.10008.5.1.4.1.1.13.1.3",
    "Breast Projection X-Ray": "1.2.840.10008.5.1.4.1.1.13.1.2",
    "Enhanced CT": "1.2.840.10008.5.1.4.1.1.2.1",
    "Enhanced MRI": "1.2.840.10008.5.1.4.1.1.4.1",
    "MRI Spectroscopy": "1.2.840.10008.5.1.4.1.1.4.2",
    "X-Ray Radiofluoroscopy": "1.2.840.10008.5.1.4.1.1.12.3",
    "Dental Radiography": "1.2.840.10008.5.1.4.1.1.1.3",
    "Panoramic Dental X-Ray": "1.2.840.10008.5.1.4.1.1.1.1",
    "Ophthalmic Photography": "1.2.840.10008.5.1.4.1.1.77.1",
    "Ophthalmic Tomography": "1.2.840.10008.5.1.4.1.1.77.1.5.4",
    "Intra-oral Radiography": "1.2.840.10008.5.1.4.1.1.1.3",
    "Bone Densitometry (DEXA)": "1.2.840.10008.5.1.4.1.1.77.1.4",
    "Slide Microscopy": "1.2.840.10008.5.1.4.1.1.77.1.6",
    "Whole Slide Microscopy": "1.2.840.10008.5.1.4.1.1.77.1.6.1",
    "Radiation Therapy Image": "1.2.840.10008.5.1.4.1.1.481.1",
    "Positron Emission Mammography (PEM)": "1.2.840.10008.5.1.4.1.1.128.1",
    "Ultrasound Multi-frame": "1.2.840.10008.5.1.4.1.1.3.1"
    # ...additional modalities as needed
}

# Standardised key mappings for DICOM, NIfTI, and NRRD
DICOM_MAP = {
    'Bits Allocated': 'data_type',                          # Bits Allocated
    'Image Orientation (Patient)': 'image_orientation',     # Image Orientation (Patient)
    'Image Position (Patient)': 'image_position',           # Image Position (Patient)
    'Pixel Spacing': 'pixel_spacing',                       # Pixel Spacing
    'Slice Thickness': 'slice_thickness',                   # Slice Thickness
    'Pixel Representation': 'pixel_representation',         # Pixel Representation
    'Rescale Slope': 'scaling_slope',                       # Rescale Slope
    'Rescale Intercept': 'scaling_intercept',               # Rescale Intercept
}

NIFTI_MAP = {
    'datatype': 'data_type',
    'sform_code': 'image_orientation',
    'qform_code': 'image_orientation',
    'pixdim': 'pixel_dimensions',       # Includes pixel spacing and slice thickness as array
    'dim': 'dimensions',                # Dimensions of the data array
    'scl_slope': 'scaling_slope',       # Data scaling: slope
    'scl_inter': 'scaling_intercept',   # Data scaling: intercept
}

NRRD_MAP = {
    'type': 'data_type',
    'space directions': 'image_orientation',
    'space origin': 'image_position',
    'spacings': 'pixel_spacing',           # Pixel dimensions, including slice thickness
    'sizes': 'dimensions',                 # Dimensions of the data array
    'thicknesses': 'slice_thickness',      # List of slice thicknesses, if non-uniform
    'endian': 'endian_type',               # Endian type of the image data
    'encoding': 'data_encoding',           # Encoding of the data (raw, gzip, etc.)
}

NRRD_TO_DICOM_TYPE_MAP = {
    'signed char': (8, 'MONOCHROME2'),
    'int8': (8, 'MONOCHROME2'),
    'int8_t': (8, 'MONOCHROME2'),
    'uchar': (8, 'MONOCHROME2'),
    'unsigned char': (8, 'MONOCHROME2'),
    'uint8': (8, 'MONOCHROME2'),
    'uint8_t': (8, 'MONOCHROME2'),
    'short': (16, 'MONOCHROME2'),
    'signed short': (16, 'MONOCHROME2'),
    'int16': (16, 'MONOCHROME2'),
    'int16_t': (16, 'MONOCHROME2'),
    'ushort': (16, 'MONOCHROME2'),
    'unsigned short': (16, 'MONOCHROME2'),
    'uint16': (16, 'MONOCHROME2'),
    'uint16_t': (16, 'MONOCHROME2'),
    'int': (32, 'MONOCHROME2'),
    'signed int': (32, 'MONOCHROME2'),
    'int32': (32, 'MONOCHROME2'),
    'int32_t': (32, 'MONOCHROME2'),
    'uint': (32, 'MONOCHROME2'),
    'unsigned int': (32, 'MONOCHROME2'),
    'uint32': (32, 'MONOCHROME2'),
    'uint32_t': (32, 'MONOCHROME2'),
    'longlong': (64, 'MONOCHROME2'),
    'long long': (64, 'MONOCHROME2'),
    'signed long long': (64, 'MONOCHROME2'),
    'int64': (64, 'MONOCHROME2'),
    'int64_t': (64, 'MONOCHROME2'),
    'ulonglong': (64, 'MONOCHROME2'),
    'unsigned long long': (64, 'MONOCHROME2'),
    'uint64': (64, 'MONOCHROME2'),
    'uint64_t': (64, 'MONOCHROME2'),
    'float': (32, 'MONOCHROME2'),
    'double': (64, 'MONOCHROME2'),
    'block': (0, 'unknown')  # Handling as unknown since block type is user-defined
}

DICOM_TO_NRRD_TYPE_MAP = {
    (0, 8): 'uint8',    # Unsigned 1-byte integer
    (1, 8): 'int8',     # Signed 1-byte integer
    (0, 16): 'uint16',  # Unsigned 2-byte integer
    (1, 16): 'int16',   # Signed 2-byte integer
    (0, 32): 'uint32',  # Unsigned 4-byte integer
    (1, 32): 'int32',   # Signed 4-byte integer
    (0, 64): 'uint64',  # Unsigned 8-byte integer
    (1, 64): 'int64',   # Signed 8-byte integer
    # Adding floating point types
    (0, 32): 'float',   # 4-byte floating point (not typical in DICOM)
    (0, 64): 'double'   # 8-byte floating point (not typical in DICOM)
}

