from pydicom.dataset import FileMetaDataset, Dataset
import pydicom.uid
import pydicom
import os
import numpy as np

def calculate_slice_position( img_orientation_patient, initial_image_position, slice_thickness, i):
    """
    Calculates the ImagePositionPatient for a specific slice based on the orientation.

    Args:
    - img_orientation_patient: Array of six elements from the ImageOrientationPatient DICOM tag.
    - initial_image_position: Initial image position (x, y, z) from the ImagePositionPatient DICOM tag.
    - slice_thickness: The thickness of each slice.
    - i: Index of the slice for which to calculate the position.

    Returns:
    - new_position: Calculated position of the specified slice.
    """
    # Extract the row and column orientation vectors
    row_vector = np.array(img_orientation_patient[:3])
    column_vector = np.array(img_orientation_patient[3:])

    # Calculate the normal vector to these using the cross product
    normal_vector = np.cross(row_vector, column_vector)

    # Calculate the shift for the current slice
    shift = normal_vector * i * slice_thickness

    # Calculate the new position for the current slice
    new_position = [initial_image_position[0] + shift[0], initial_image_position[1] + shift[1], initial_image_position[2] + shift[2]]

    return new_position

def calculate_slice_location( img_orientation_patient, initial_slice_location, slice_thickness, i):
    """
    Calculates the SliceLocation for a specific slice based on the orientation and initial slice location.

    Args:
    - img_orientation_patient: Array of six elements from the ImageOrientationPatient DICOM tag.
    - initial_image_position: Initial image position (x, y, z) from the ImagePositionPatient DICOM tag.
    - initial_slice_location: The SliceLocation of the first slice in the series.
    - slice_thickness: The thickness of each slice.
    - i: Index of the slice for which to calculate the SliceLocation.

    Returns:
    - initial_slice_location: Calculated SliceLocation of the specified slice.
    """
    # Extract the row and column orientation vectors
    row_vector = np.array(img_orientation_patient[:3])
    column_vector = np.array(img_orientation_patient[3:])

    # Calculate the normal vector to these using the cross product
    normal_vector = np.cross(row_vector, column_vector)

    # Calculate the projection shift for the current slice
    projection_shift = np.dot(normal_vector, normal_vector) * i * slice_thickness

    # Calculate the new SliceLocation for the current slice
    initial_slice_location = initial_slice_location + projection_shift

    return initial_slice_location

def default_window_values(img_arr):

    min_val = np.min(img_arr)
    max_val = np.max(img_arr)
    half_range = (max_val - min_val) / 2

    # Window centre
    wc_slider = min_val + half_range / 2
    
    # Window width
    ww_slider = half_range * 3/4 

    return wc_slider, ww_slider

def prepare_dicom_slice(slice_info):

    dicom_header = slice_info['dicom_header']
    img_arr = slice_info['image']
    series_instance_uid = slice_info['series_instance_uid']
    study_instance_uid = slice_info['study_instance_uid']
    frame_of_reference_uid = slice_info['frame_of_reference_uid']
    implementation_class_uid = slice_info['implementation_class_uid']
    sop_instance_uid = slice_info['sop_instance_uid']
    i = slice_info['iteration']
    plane = slice_info['plane']

    # 1 = Required
    # 1C = Conditionally Required
    # 2 = Required, empty if unknown
    # 3 = Optional

    meta = FileMetaDataset()
    # File Preamble. Typically, you don't have to manually set this unless you have a specific use case
    # DICOM Prefix. This is automatically handled by pydicom when saving a file
    # File Meta Information Group Length. This is calculated and added by pydicom, so you don't manually set it
    meta.FileMetaInformationVersion = b'\x00\x01'  # Two byte field.
    meta.MediaStorageSOPClassUID = dicom_header.get('Media Storage SOP Class UID', dicom_header.get('SOP Class UID', '1.2.840.10008.5.1.4.1.1.4')) # MR as backup
    meta.MediaStorageSOPInstanceUID = sop_instance_uid  # Unique identifier for the instance
    meta.TransferSyntaxUID = pydicom.uid.ExplicitVRLittleEndian  # Explicit VR Little Endian
    meta.ImplementationClassUID = implementation_class_uid  # Implementation Class UID

    # Main data elements EMPTY IF UNKNOWN
    # data = Dataset()
    # data.preamble = b'\0' * 128  # 128-byte preamble
    # data.SpecificCharacterSet = dicom_header.get('Specific Character Set', 'ISO_IR 100') # 1C
    # data.SOPClassUID = dicom_header.get('SOP Class UID', '1.2.840.10008.5.1.4.1.1.4') # 1
    # data.SOPInstanceUID = sop_instance_uid # 1
    # data.StudyInstanceUID = dicom_header.get('Study Instance UID', study_instance_uid) # 1C
    # data.SeriesInstanceUID = dicom_header.get('Series Instance UID', series_instance_uid) # 1C
    # if plane == 'axial':
    #     data.ImageType = dicom_header.get('Image Type', ['ORIGINAL', 'PRIMARY', 'AXIAL']) # 1
    # elif plane == 'sagittal':
    #     data.ImageType = dicom_header.get('Image Type', ['ORIGINAL', 'PRIMARY', 'SAGITTAL']) # 1
    # elif plane == 'coronal':
    #     data.ImageType = dicom_header.get('Image Type', ['ORIGINAL', 'PRIMARY', 'CORONAL']) # 1
    # data.StudyID = dicom_header.get('Study ID', '') # 2
    # data.StudyDate = dicom_header.get('Study Date', '') # 2
    # data.SeriesNumber = dicom_header.get('Series Number', '') # 2
    # data.ReferringPhysicianName = dicom_header.get('Referring Physician\'s Name', '') # 2
    # data.AccessionNumber = dicom_header.get('Accession Number', '') # 2
    # data.PatientName = dicom_header.get('Patient\'s Name', '') # 2
    # data.PatientSex = dicom_header.get('Patient\'s Sex', '') # 2
    # data.PatientID = dicom_header.get('Patient ID', '') # 2
    # data.ContentDate = dicom_header.get('Content Date', '') # 2C
    # data.StudyTime = dicom_header.get('Study Time', '') # 2C
    # data.ContentTime = dicom_header.get('Content Time', '') # 2C
    # data.Modality = dicom_header.get('Modality', 'MR') # 1
    # data.SpacingBetweenSlices = dicom_header.get('Spacing Between Slices', '') # 3

    # data.SliceThickness = dicom_header.get('Slice Thickness', '1.0') # 2
    # data.InstanceNumber = dicom_header.get('Instance Number', str(i + 1)) # 2
    # data.ImageOrientationPatient = dicom_header.get('Image Orientation (Patient)', [1, 0, 0, 0, 1, 0]) # 1
    # initial_image_position = dicom_header.get('Image Position (Patient)', [0, 0, 0])
    # data.ImagePositionPatient = calculate_slice_position(data.ImageOrientationPatient, initial_image_position, data.SliceThickness, i) # 1
    # data.FrameOfReferenceUID = dicom_header.get('Frame of Reference UID', frame_of_reference_uid) # 1
    # data.SamplesPerPixel = dicom_header.get('Samples Per Pixel', 1) # 1
    # data.PhotometricInterpretation = dicom_header.get('Photometric Interpretation', 'MONOCHROME2') # 1
    # data.Rows = dicom_header.get('Rows', img_arr.shape[0]) # 1
    # data.Columns = dicom_header.get('Columns', img_arr.shape[1]) # 1
    # data.PixelSpacing = dicom_header.get('Pixel Spacing', str([1.0, 1.0])) # 1
    # data.BitsAllocated = dicom_header.get('Bits Allocated', 16) # 1
    # data.BitsStored = dicom_header.get('Bits Stored', 12) # 1
    # data.HighBit = dicom_header.get('High Bit', 11) # 1
    # data.PixelRepresentation = dicom_header.get('Pixel Representation', 1) # 1
    # if data.SOPClassUID in ['1.2.840.10008.5.1.4.1.1.2', '1.2.840.10008.5.1.4.1.1.2.1', '1.2.840.10008.5.1.4.1.1.2.2']:
    #     data.RescaleIntercept = dicom_header.get('Rescale Intercept', 0.0) # 1C
    #     data.RescaleSlope = dicom_header.get('Rescale Slope', 1.0) # 1C
    # data.Manufacturer = dicom_header.get('Manufacturer', '') # 2
    # data.ScanningSequence = dicom_header.get('Scanning Sequence', ['GR', 'IR']) # 1
    # data.SequenceVariant = dicom_header.get('Sequence Variant', ['SK','SP','MP']) # 1
    # data.ScanOptions = dicom_header.get('Scan Options', []) # 2
    # data.MRAcquisitionType = dicom_header.get('MR Acquisition Type', '') # 2
    # data.EchoTime = dicom_header.get('Echo Time', '') # 2
    # data.EchoTrainLength = dicom_header.get("Echo Train Length", '') # 2
    # data.ContrastBolusAgent = dicom_header.get('Contrast/Bolus Agent', '') # 2
    # data.RepetitionTime = dicom_header.get('Repetition Time', '') # 2C
    # data.InversionTime = dicom_header.get('Inversion Time', '') # 2C
    # data.PositionReferenceIndicator = dicom_header.get('Position Reference Indicator', '') # 2
    # wc, ww = default_window_values(img_arr)
    # data.WindowCenter = dicom_header.get('Window Center', str(round(wc))) # 1C
    # data.WindowWidth = dicom_header.get('Window Width', str(round(ww))) # 1C
    # if data.Modality == 'CT':
    #     px_array = np.ascontiguousarray(img_arr[:, :, i]).astype(np.int16)
    # else:
    #     px_array = np.ascontiguousarray(img_arr[:, :, i]).astype(np.uint16)
    # data.PixelData = px_array.tobytes()

    # Main data elements DUMMY IF UNKNOWN
    data = Dataset()
    data.preamble = b'\0' * 128  # 128-byte preamble
    data.SpecificCharacterSet = dicom_header.get('Specific Character Set', 'ISO_IR 100')  # 1C
    data.SOPClassUID = dicom_header.get('SOP Class UID', '1.2.840.10008.5.1.4.1.1.4')  # 1
    data.SOPInstanceUID = sop_instance_uid  # 1
    data.StudyInstanceUID = dicom_header.get('Study Instance UID', study_instance_uid)  # 1C
    data.SeriesInstanceUID = dicom_header.get('Series Instance UID', series_instance_uid)  # 1C

    if plane == 'axial':
        data.ImageType = dicom_header.get('Image Type', ['ORIGINAL', 'PRIMARY', 'AXIAL'])  # 1
    elif plane == 'sagittal':
        data.ImageType = dicom_header.get('Image Type', ['ORIGINAL', 'PRIMARY', 'SAGITTAL'])  # 1
    elif plane == 'coronal':
        data.ImageType = dicom_header.get('Image Type', ['ORIGINAL', 'PRIMARY', 'CORONAL'])  # 1

    data.StudyID = dicom_header.get('Study ID', '000000')  # 2
    data.StudyDate = dicom_header.get('Study Date', '20010101')  # 2
    data.SeriesNumber = dicom_header.get('Series Number', '1')  # 2
    data.ReferringPhysicianName = dicom_header.get("Referring Physician's Name", 'PHYSICIAN^DUMMY')  # 2
    data.AccessionNumber = dicom_header.get('Accession Number', '000000')  # 2
    data.PatientName = dicom_header.get("Patient's Name", 'PATIENT^DUMMY')  # 2
    data.PatientSex = dicom_header.get("Patient's Sex", 'O')  # 2
    data.PatientID = dicom_header.get('Patient ID', '000000')  # 2
    data.ContentDate = dicom_header.get('Content Date', '20010101')  # 2C
    data.StudyTime = dicom_header.get('Study Time', '000000.000000')  # 2C
    data.ContentTime = dicom_header.get('Content Time', '000000.000000')  # 2C
    data.Modality = dicom_header.get('Modality', 'MR')  # 1
    # data.SpacingBetweenSlices = dicom_header.get('Spacing Between Slices', '1.0')  # 3

    data.SliceThickness = dicom_header.get('Slice Thickness', '1.0')  # 2
    data.InstanceNumber = dicom_header.get('Instance Number', str(i + 1))  # 2
    data.ImageOrientationPatient = dicom_header.get('Image Orientation (Patient)', [1, 0, 0, 0, 1, 0])  # 1
    initial_image_position = dicom_header.get('Image Position (Patient)', [0, 0, 0])
    data.ImagePositionPatient = calculate_slice_position(data.ImageOrientationPatient, initial_image_position, data.SliceThickness, i)  # 1
    data.FrameOfReferenceUID = dicom_header.get('Frame of Reference UID', frame_of_reference_uid)  # 1
    data.SamplesPerPixel = dicom_header.get('Samples Per Pixel', 1)  # 1
    data.PhotometricInterpretation = dicom_header.get('Photometric Interpretation', 'MONOCHROME2')  # 1
    data.Rows = dicom_header.get('Rows', img_arr.shape[0])  # 1
    data.Columns = dicom_header.get('Columns', img_arr.shape[1])  # 1
    data.PixelSpacing = dicom_header.get('Pixel Spacing', '[1.0, 1.0]')  # 1
    data.BitsAllocated = dicom_header.get('Bits Allocated', 16)  # 1
    data.BitsStored = dicom_header.get('Bits Stored', 12)  # 1
    data.HighBit = dicom_header.get('High Bit', 11)  # 1
    data.PixelRepresentation = dicom_header.get('Pixel Representation', 1)  # 1

    if data.SOPClassUID in ['1.2.840.10008.5.1.4.1.1.2', '1.2.840.10008.5.1.4.1.1.2.1', '1.2.840.10008.5.1.4.1.1.2.2']:
        data.RescaleIntercept = dicom_header.get('Rescale Intercept', 0.0)  # 1C
        data.RescaleSlope = dicom_header.get('Rescale Slope', 1.0)  # 1C

    data.Manufacturer = dicom_header.get('Manufacturer', 'MANUFACTURER^DUMMY')  # 2
    data.ScanningSequence = dicom_header.get('Scanning Sequence', ['GR', 'IR'])  # 1
    data.SequenceVariant = dicom_header.get('Sequence Variant', ['SK','SP','MP'])  # 1
    data.ScanOptions = dicom_header.get('Scan Options', ['NONE'])  # 2
    data.MRAcquisitionType = dicom_header.get('MR Acquisition Type', 'DUMMY ACQUISITION')  # 2
    data.EchoTime = dicom_header.get('Echo Time', '0.00')  # 2
    data.EchoTrainLength = dicom_header.get("Echo Train Length", '0')  # 2
    data.ContrastBolusAgent = dicom_header.get('Contrast/Bolus Agent', 'NONE')  # 2
    data.RepetitionTime = dicom_header.get('Repetition Time', '0000')  # 2C
    data.InversionTime = dicom_header.get('Inversion Time', '000')  # 2C
    data.PositionReferenceIndicator = dicom_header.get('Position Reference Indicator', 'DUMMY INDICATOR')  # 2
    wc, ww = default_window_values(img_arr)
    data.WindowCenter = dicom_header.get('Window Center', str(round(wc)))  # 1C
    data.WindowWidth = dicom_header.get('Window Width', str(round(ww)))  # 1C

    if data.Modality == 'CT':
        px_array = np.ascontiguousarray(img_arr[:, :, i]).astype(np.int16)
    else:
        px_array = np.ascontiguousarray(img_arr[:, :, i]).astype(np.uint16)

    data.PixelData = px_array.tobytes()        
    
    # data.save_as(dicom_file_path)

    # data.PatientBirthDate = dicom_header.get('Patient\'s Birth Date', '') # 3
    # data.PatientBirthTime = dicom_header.get('Patient\'s Birth Time', '') # 3
    # data.PregnancyStatus = dicom_header.get('Pregnancy Status', '') # 3
    # data.SeriesDate = dicom_header.get('Series Date', '20220101') # 3
    # data.SeriesTime = dicom_header.get('Series Time', '093000') # 3
    # data.AcquisitionDate = dicom_header.get('Acquisition Date', '20220101') # 3
    # data.AcquisitionTime = dicom_header.get('Acquisition Time', '093000') # 3
    # data.IssuerOfPatientID = dicom_header.get("Issuer of Patient ID", '') # 3
    # data.PatientAge = dicom_header.get('Patient\'s Age', '060Y') # 3
    # data.AcquisitionNumber = dicom_header.get('Acquisition Number', '1') # 3
    # initial_slice_location = dicom_header.get('Slice Location', '0.0')
    # data.SliceLocation = self.calculate_slice_location(data.ImageOrientationPatient, initial_slice_location, data.SliceThickness, i) # 3
    # data.SequenceName = dicom_header.get('Sequence Name', '') # 3
    # data.AngioFlag = dicom_header.get("Angio Flag", "") # 3
    # data.SmallestImagePixelValue = dicom_header.get('Smallest Image Pixel Value', int(np.min(img_arr))) # 3
    # data.LargestImagePixelValue = dicom_header.get('Largest Image Pixel Value', int(np.max(img_arr))) # 3
    # data.InstanceCreationDate = dicom_header.get('Instance Creation Date', '20220101') # 3
    # data.InstanceCreationTime = dicom_header.get('Instance Creation Time', '093000') # 3
    # data.InstitutionalDepartmentName = dicom_header.get('Institutional Department Name', 'Department') # 3
    # data.PhysiciansOfRecord = dicom_header.get('Physician(s) of Record', '') # 3
    # data.PerformingPhysicianName = dicom_header.get("Performing Physician's Name", "") # 3
    # data.NameOfPhysiciansReadingStudy = dicom_header.get("Name of Physician(s) Reading Study", "") # 3
    # data.OperatorsName = dicom_header.get("Operators' Name", "") # 3
    # data.InstitutionName = dicom_header.get('Institution Name', '') # 3
    # data.InstitutionAddress = dicom_header.get('Institution Address', '') # 3
    # data.StationName = dicom_header.get('Station Name', '') # 3
    # data.StudyDescription = dicom_header.get('Study Description', '') # 3
    # data.SeriesDescription = dicom_header.get('Series Description', '') # 3
    # data.ManufacturerModelName = dicom_header.get('Manufacturer\'s Model Name', '') # 3
    # data.BodyPartExamined = dicom_header.get('Body Part Examined', '') # 3
    # data.MagneticFieldStrength = dicom_header.get('Magnetic Field Strength', 1.5) # 3
    # data.SpacingBetweenSlices = dicom_header.get('Spacing Between Slices', '')
    # data.NumberOfPhaseEncodingSteps = dicom_header.get('Number of Phase Encoding Steps', str(128)) # 3
    # data.PixelBandwidth = dicom_header.get('Pixel Bandwidth', 200) # 3
    # data.SoftwareVersions = dicom_header.get('Software Versions', '') # 3
    # data.ProtocolName = dicom_header.get('Protocol Name', '') # 3
    # data.PatientBirthTime = dicom_header.get('Patient\'s Birth Time', '') # 3
    # data.OtherPatientIDs = dicom_header.get('Other Patient IDs', '') # 3
    # data.OtherPatientNames = dicom_header.get('Other Patient Names', '') # 3
    # data.PatientSize = dicom_header.get('Patient\'s Size', '') # 3
    # data.PatientWeight = dicom_header.get('Patient\'s Weight', '') # 3
    # data.EthnicGroup = dicom_header.get("Ethnic Group", "") # 3
    # data.BranchOfService = dicom_header.get('Branch of Service', '')  
    # data.PatientTelephoneNumbers = dicom_header.get('Patient\'s Telephone Numbers', '') # 3
    # data.AdditionalPatientHistory = dicom_header.get('Additional Patient History', '') # 3
    # data.PatientReligiousPreference = dicom_header.get('Patient\'s Religious Preference', '')
    # data.NumberOfAverages = dicom_header.get('Number of Averages', 1) # 3
    # data.ImagingFrequency = dicom_header.get('Imaging Frequency', 123) # 3
    # data.ImagedNucleus = dicom_header.get('Imaged Nucleus', '1H') # 3
    # data.EchoNumbers = dicom_header.get('Echo Number(s)', 1) # 3
    # data.PercentSampling = dicom_header.get('Percent Sampling', 100) # 3
    # data.PercentPhaseFieldOfView = dicom_header.get('Percent Phase Field of View', 100) # 3
    # data.DeviceSerialNumber = dicom_header.get('Device Serial Number', '000000') # 3
    # data.ContrastBolusVolume = dicom_header.get('Contrast/Bolus Volume', 10) # 3
    # data.ContrastBolusTotalDose = dicom_header.get('Contrast/Bolus Total Dose', 0) # 3
    # data.ContrastBolusIngredient = dicom_header.get('Contrast/Bolus Ingredient', '') # 3
    # data.ContrastBolusIngredientConcentration = dicom_header.get('Contrast/Bolus Ingredient Concentration', 0) # 3
    # data.TransmitCoilName = dicom_header.get('Transmit Coil Name', 'Body') # 3
    # data.AcquisitionMatrix = dicom_header.get('Acquisition Matrix', [0, 256, 256, 0]) # 3
    # data.InPlanePhaseEncodingDirection = dicom_header.get('In-plane Phase Encoding Direction', '')
    # data.FlipAngle = dicom_header.get('Flip Angle', 0) # 
    # data.VariableFlipAngleFlag = dicom_header.get('Variable Flip Angle Flag', 'N') # 3
    # data.SAR = dicom_header.get('SAR', 0) # 3
    # data.dBdt = dicom_header.get('dB/dt', 0) # 3
    # data.PatientPosition = dicom_header.get('Patient Position', 'HFS') # 3
    # data.PrivateCreator = dicom_header.get('Private Creator', '') # 1 BUT I THINK IT DEPENDS ON OTHER THINGS EXISTING, like inventory?
    # data.SliceMeasurementDuration = dicom_header.get('SliceMeasurementDuration', '')
    # data.GradientMode = dicom_header.get('GradientMode', 'Normal')
    # data.FlowCompensation = dicom_header.get('FlowCompensation', 'No')
    # data.TablePositionOrigin = dicom_header.get('TablePositionOrigin', [0, 0, -1000])
    # data.ImaAbsTablePosition = dicom_header.get('ImaAbsTablePosition', [0, 0, -1000])
    # data.ImaRelTablePosition = dicom_header.get('Ima Rel Table Position', '')
    # data.SlicePositionPCS = dicom_header.get('Slice Position PCS', '')
    # data.SliceResolution = dicom_header.get('Slice Resolution', '')
    # data.RealDwellTime = dicom_header.get('Real Dwell Time', '') 
    # data.WindowCenterWidthExplanation = dicom_header.get('Window Center & Width Explanation', 'Algo1') # 3
    # data.ReferencedStudySequence = dicom_header.get('Referenced Study Sequence', '') # 3
    # data.ReferencedPatientSequence = dicom_header.get('Referenced Patient Sequence', '') # 3
    # data.ReferencedImageSequence = dicom_header.get('Referenced Image Sequence', '') # 3
    # data.RequestAttributesSequence = dicom_header.get('Request Attributes Sequence', []) # 3

    # data.file_meta = file_meta
    data.file_meta = meta
    data.is_little_endian = True
    data.is_implicit_VR = False

    return data
