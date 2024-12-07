#%%
import os
import pydicom
from pydicom.errors import InvalidDicomError
import nibabel as nib
import nrrd
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkinter import ttk
import csv
from PIL import Image
from screeninfo import get_monitors
import numpy as np 
from customtkinter import *
import SimpleITK as sitk

from header_tag_conversions import *

def view_header(master, image_path):
    """ Display the header information of an image in a structured Treeview. """

    original_header_info, _ = get_header_info(image_path)
    if not original_header_info:
        return  # Exit if there's nothing to show, as expected.

    header_info = original_header_info.copy()  # Make a copy for filtering purposes

    # Create a new Toplevel window
    popup = CTkToplevel(master)
    popup.title("Image Information")

    popup.withdraw()

    # Set the initial size of the window (width x height)
    window_size = (600, 450)
    popup.geometry(f"{window_size[0]}x{window_size[1]}")
    centre_window(popup, window_size)

    popup.deiconify()

    # Create search bar
    search_frame = CTkFrame(popup)
    search_frame.pack(side='top', fill='x', padx=10, pady=5)

    search_label = CTkLabel(search_frame, text="Search:")
    search_label.pack(side='left')

    search_var = tk.StringVar()

    search_entry = CTkEntry(search_frame, textvariable=search_var)
    search_entry.pack(side='left', fill='x', expand=True, padx=10)

    # Treeview setup
    tree = ttk.Treeview(popup, columns=('Key', 'Value'), show='headings', height=10)
    tree.heading('Key', text='Key')
    tree.heading('Value', text='Value')
    tree.column('Key', anchor='w', width=250, stretch=tk.NO)  # Fixed width for the 'Key' column
    tree.column('Value', anchor='w', stretch=tk.YES)  # 'Value' column will expand

    def update_treeview(filtered_info):
        tree.delete(*tree.get_children())  # Clear current Treeview contents
        for key, value in sorted(filtered_info.items()):
            tree.insert('', 'end', values=(key, value))

    # Initial population of the Treeview
    update_treeview(header_info)

    # Scrollbar for the Treeview
    scrollbar = CTkScrollbar(popup, orientation="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)

    # Buttons frame
    buttons_frame = CTkFrame(popup)
    buttons_frame.pack(side='bottom', fill='x', pady=0)  # Pack frame first

    export_button = CTkButton(buttons_frame, text="Export as CSV", command=lambda: export_as_csv(header_info, image_path))
    close_button = CTkButton(buttons_frame, text="Close", command=popup.destroy)

    # Use grid inside the frame to center the buttons
    buttons_frame.grid_columnconfigure(0, weight=1)  # Empty column to the left for centering
    buttons_frame.grid_columnconfigure(3, weight=1)  # Empty column to the right for centering

    export_button.grid(row=0, column=1, padx=0, pady=2)
    close_button.grid(row=0, column=2, padx=0, pady=2)

    # Layout
    scrollbar.pack(side='right', fill='y')
    tree.pack(side='top', fill='both', expand=True)

    # Window configuration for dynamic resizing
    popup.grid_columnconfigure(0, weight=1)
    popup.grid_rowconfigure(1, weight=1)

    # Event to open a popup for copying text
    def show_details(event):
        selected_item = tree.selection()[0]
        item_values = tree.item(selected_item, 'values')
        detail_popup = CTkToplevel(popup)
        centre_window(detail_popup, (300, 100))
        detail_popup.title("Detail View")
        text = CTkTextbox(detail_popup, height=10, width=50)
        text.insert('end', f"Key: {item_values[0]}\nValue: {item_values[1]}")
        text.pack(fill='both', expand=True)
        text.config(state='disabled')
        button = CTkButton(detail_popup, text='Close', command=detail_popup.destroy)
        button.pack()

    tree.bind('<Double-1>', show_details)  # Bind double-click event to show details

    # Filter function
    def filter_header_info(*args):
        search_text = search_var.get().lower()
        filtered_info = {k: v for k, v in original_header_info.items() if search_text in k.lower() or search_text in str(v).lower()}
        update_treeview(filtered_info)

    # Bind the filter function to the search bar text changes
    search_var.trace_add('write', filter_header_info)

def get_header_info(image_path):
    """ Get the header information of an image. """

    print("get_header_info", image_path)
    
    header_info = None 
    format_in = ''
    try:
        # Check if single file and DICOM
        if os.path.isfile(image_path) and is_dicom(image_path):
            header_info = header_dicom(image_path)
            format_in = 'dicom'
        # Check if directory contains DICOM files
        elif os.path.isdir(image_path) and any(is_dicom(os.path.join(image_path, f)) for f in os.listdir(image_path) if os.path.isfile(os.path.join(image_path, f))):
            header_info = header_dicom(image_path)
            format_in = 'dicom'
        # NifTI
        elif image_path.endswith('.nii') or image_path.endswith('.nii.gz'):
            header_info = header_nifti(image_path)
            format_in = 'nifti'
        # NRRD
        elif image_path.endswith('.nrrd'):
            header_info = header_nrrd(image_path)
            format_in = 'nrrd'
        # PNG or JPEG
        elif image_path.lower().endswith(('.png', '.jpg', '.jpeg')):
            header_info = header_png_jpeg(image_path)
            format_in = 'png_jpeg'

    except Exception as e:
        print(e)
        return None, None

    # If any keys are lists, convert them to strings
    # header_info = rename_keys_with_list_to_string(header_info)

    return header_info, format_in

def rename_keys_with_list_to_string(original_dict):
    new_dict = {}
    for key, value in original_dict.items():
        if isinstance(key, str) and key.startswith('[') and key.endswith(']'):
            # Remove the brackets and extra spaces
            cleaned_key = key[1:-1].replace(' ', '')
            new_dict[cleaned_key] = value
        else:
            new_dict[key] = value
    return new_dict


def header_dicom(image_path):
    """
    Get the header information of a DICOM file or the first valid DICOM image found in a directory.
    - image_path: Path to a DICOM file or a directory containing DICOM files.
    """
    if os.path.isfile(image_path):
        return dicom_single_header(image_path)
    elif os.path.isdir(image_path):
        return dicom_dir_header(image_path)
    else:
        messagebox.showerror("Path Error", "The specified path does not exist.")
        return None

def dicom_single_header(file_path):
    """ Reads and returns the DICOM header information from a single file. """
    try:
        ds = pydicom.dcmread(file_path, stop_before_pixels=True)
        header_dicom = {}
        for elem in ds:
            # if elem.tag.group < 0x6000:  # Filtering out pixel data
            header_dicom[elem.name] = elem.value
        return header_dicom
    except InvalidDicomError as e:
        messagebox.showerror("DICOM Error", f"Invalid DICOM file: {str(e)}")
        return None

def dicom_dir_header(directory_path):
    """ Finds the first valid DICOM file in a directory and returns its header information. """
    all_files = os.listdir(directory_path)
    all_files_ds = []
    for file in list(all_files): # Use list to make a copy (avoids skipping indices when removing items)
        try:
            ds = pydicom.dcmread(os.path.join(directory_path, file), stop_before_pixels=True)
            modalities = ['RTDOSE', 'RTSTRUCT', 'RTPLAN']
            if ds.Modality not in modalities:
                all_files_ds.append(ds)
            else:
                all_files.remove(file)
        except:
            pass
    sorted_files = zip(all_files_ds, all_files)
    sorted_files = sorted(sorted_files, key=lambda x: sort_key(x[0]))
    return dicom_single_header(os.path.join(directory_path, sorted_files[0][1]))

def sort_key(ds):
    if hasattr(ds, 'ImagePositionPatient'):
        origin = ds.ImagePositionPatient
        orientation = ds.ImageOrientationPatient
        
        col_i = orientation[:3]
        col_j = orientation[3:]
        col_k = np.cross(col_i, col_j)

        dot = np.dot(col_k, origin)

        return dot
    
    elif hasattr(ds, 'InstanceNumber'):
        return ds.InstanceNumber
    elif hasattr(ds, 'SliceLocation'):
        return ds.SliceLocation
    
def header_nifti(image_path):
    """ Get the header information of a NifTI image. """
    nii = nib.load(image_path)
    header_nifti = {key: str(val) for key, val in nii.header.items()}
    return header_nifti

def header_nrrd(image_path):
    """ Get the header information of a NRRD image. """
    # Read the NRRD file header
    try:
        data, header = nrrd.read(image_path, index_order='C')
        header_nrrd = {key: str(val) for key, val in header.items()}
        return header_nrrd
    except nrrd.NrrdError as e:
        messagebox.showerror("NRRD Error", f"Invalid NRRD file: {str(e)}")
        return None

def header_png_jpeg(image_path):
    """ Get the header information of a PNG or JPEG image. """
    with Image.open(image_path) as img:
        header_natural = {key: img.info[key] for key in img.info}
    return header_natural

def is_dicom(image_path):
    """ Check if the file at 'image_path' is a valid DICOM file. """
    if not os.path.isfile(image_path):
        return False
    try:
        # Attempt to dicom_dir_header the file with pydicom and check for specific DICOM tags
        ds = pydicom.dcmread(image_path, stop_before_pixels=True)
        return True
    except InvalidDicomError:
        return False
    except Exception:
        return False
    return False

def contains_dicom(path_in):      
    """ Check if a directory contains DICOM files. """
    contains_dicom = False  
    contains_image = False
    rtss_file_names = []
    if os.path.isdir(path_in):
        for item in os.listdir(path_in):
            item_path = os.path.join(path_in, item)
            
            # Skip directories
            if os.path.isdir(item_path):
                continue
            
            try:
                # Attempt to read the file as a DICOM file
                ds = pydicom.dcmread(item_path, stop_before_pixels=True)
                contains_dicom = True

                # Check if the file is a RTSS file
                if ds.Modality == 'RTSTRUCT':
                    rtss_file_names.append(item_path)
                
                # Check if ct, mr etc image file
                if 'ImageType' in ds:
                    contains_image = True
            except InvalidDicomError: # If an InvalidDicomError was raised, it's not a DICOM file
                continue
    
    # If no DICOM files were found, return False
    return contains_dicom, rtss_file_names, contains_image

def centre_window(window, window_size):
    """ Centre the window on the monitor where the mouse cursor is currently located. """
    
    window.update_idletasks()  # Ensures that the window's geometry is up to date

    # Fetch the mouse cursor's current screen position
    x_mouse, y_mouse = window.winfo_pointerxy()

    # Retrieve all connected monitors
    monitors = get_monitors()

    # Determine which monitor the cursor is on
    current_monitor = None
    for monitor in monitors:
        if monitor.x <= x_mouse <= monitor.x + monitor.width and monitor.y <= y_mouse <= monitor.y + monitor.height:
            current_monitor = monitor
            break

    # Fallback to the primary monitor if no monitor contains the cursor
    if not current_monitor:
        current_monitor = monitors[0] if monitors else None

    if current_monitor:
        
        width = window_size[0]
        height = window_size[1]

        # Calculate the position to center the window on the found monitor
        x = int(current_monitor.x) + (int(current_monitor.width) - width) // 2
        y = int(current_monitor.y) + (int(current_monitor.height) - height) // 2

        # Set the new window geometry
        window.geometry(f"{width}x{height}+{x}+{y}")

def export_as_csv(header, image_path):
    """ Export information as a CSV file with user-defined location and filename. """
    # Open a file save dialog
    file_path = filedialog.asksaveasfilename(
        initialdir=os.path.dirname(image_path),
        title="Select file",
        filetypes=(("CSV files", "*.csv"), ("All files", "*.*")),
        defaultextension=".csv"
    )

    # Check if a file path was provided (i.e., the user didn't cancel the dialog)
    if file_path:
        try:
            with open(file_path, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                if isinstance(header, dict):
                    for key, value in header.items():  # Use .items() for dictionaries
                        writer.writerow([key, value])
                elif isinstance(header, (list, tuple)):
                    for item in header:
                        writer.writerow(item)  # Assuming each item is already a tuple (key, value)
            messagebox.showinfo("Export Successful", f"The data was exported successfully to '{file_path}'.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export the data: {str(e)}")


#%% Image Conversion Controller Functions

def dicom_to_dicom(header_in):
    dicom_header = header_in
    dicom_header['plane'] = anatomical_plane_dicom(dicom_header['Image Orientation (Patient)'])
    return dicom_header

def dicom_to_nifti(image, header_in, path_in):

    # Load the DICOM series with SimpleITK
    reader_sitk = sitk.ImageSeriesReader()
    dicom_filenames = reader_sitk.GetGDCMSeriesFileNames(path_in)
    reader_sitk.SetFileNames(dicom_filenames)
    dicom_img_sitk = reader_sitk.Execute()
    print('Original image shape:', dicom_img_sitk.GetSize())

    # [Optional] Perform any image processing or transformations here
    # For example, resampling, filtering, etc.

    # Define output directories
    output_dir = r"C:\Users\physics\Desktop\processed_images"
    os.makedirs(output_dir, exist_ok=True)

    # Save as NIfTI (.nii)
    nifti_path = os.path.join(output_dir, 'image.nii')
    sitk.WriteImage(dicom_img_sitk, nifti_path)
    print(f"Image saved as NIfTI at: {nifti_path}")

    # Save as compressed NIfTI (.nii.gz)
    nifti_gz_path = os.path.join(output_dir, 'image.nii.gz')
    sitk.WriteImage(dicom_img_sitk, nifti_gz_path)
    print(f"Image saved as compressed NIfTI at: {nifti_gz_path}")

    # Save as NRRD (.nrrd)
    nrrd_path = os.path.join(output_dir, 'image.nrrd')
    sitk.WriteImage(dicom_img_sitk, nrrd_path)
    print(f"Image saved as NRRD at: {nrrd_path}")
    
    # Transform header values from DICOM
    affine_matrix = dicom_to_nifti_affine(header_in, path_in) 
    pix_dim = np.array(dicom_to_nifti_pixdim(header_in, path_in), dtype=float) 
    data_type, bitpix = dicom_to_nifti_datatype(header_in)
    scl_slope, scl_inter = dicom_to_nifti_scl_slope(header_in)

    # Set values less than 1e-6 to 0
    affine_matrix[np.abs(affine_matrix) < 1e-6] = 0

    # Access and modify the image's header directly
    nifti_img = nib.Nifti1Image(image, affine_matrix)
    header = nifti_img.header
    header['datatype'] = data_type
    header['bitpix'] = bitpix
    header.set_sform(affine_matrix, code=1) # Set automatically with affine matrix, but need to set code manually
    header.set_qform(affine_matrix, code=1)  # Set automatically with affine matrix, but need to set code manually
    header['scl_slope'] = scl_slope # Applies to image matrix upon saving, then is set to nan in saved header
    header['scl_inter'] = scl_inter
    header['pixdim'] = pix_dim
    header['slice_code'] = 0 # Arbitrary value for slice code

    return nifti_img

def dicom_to_nrrd(header_in, path_in):
    # https://teem.sourceforge.net/nrrd/format.html#space
    print(header_in)

    sizes = dicom_to_nrrd_sizes(header_in)
    thicknesses = dicom_to_nrrd_thicknesses(header_in, path_in)
    data_type = dicom_to_nrrd_type(header_in)
    endian = dicom_to_nrrd_endian(header_in)
    space_origin = dicom_to_nrrd_origin(header_in) 
    space_directions = dicom_to_nrrd_space_directions(header_in, path_in) # Similar to image orientation (patient) but with pixel spacing integrated (not unit vector)

    encoding = "raw"
    dimension = len(space_directions)
    space = "left-posterior-superior"
    kinds = ['domain', 'domain', 'domain']

    nrrd_header = {
        'sizes': sizes, # necessary
        'type': data_type, # necessary
        'kinds': kinds, # optional
        'encoding': encoding, # necessary
        'endian': endian, # necessary
        'dimension': dimension, # necessary
        'space': space, # optional, replaces space dimension
        'space origin': space_origin, # optional
        'space directions': space_directions, # optional
        'thicknesses': thicknesses, # optional
    }

    return nrrd_header

def nifti_to_nifti(image, header_in):
    # Changing sign from unsigned short to float
    # Swapping quatern signs

    # Transform header values from NRRD
    pixdim = nifti_to_nifti_pixdim(header_in)
    affine_matrix = nifti_to_nifti_affine(header_in)
    datatype, bitpix = nifti_to_nifti_datatype_bitpix(header_in)
    
    # Clean up very small values in the affine matrix to maintain numerical stability
    affine_matrix[np.abs(affine_matrix) < 1e-6] = 0

    # Access and modify the NIfTI image's header directly
    nifti_img = nib.Nifti1Image(image, affine_matrix)
    header = nifti_img.header
    header['datatype'] = datatype
    header['bitpix'] = bitpix
    header.set_sform(affine_matrix, code=1)  # Set sform and qform codes to 1 (aligned with scanner)
    header.set_qform(affine_matrix, code=1)
    header['pixdim'] = pixdim

    return nifti_img

def nifti_to_dicom(image, header_in):
    # Transform header values from NIfTI
    pixel_spacing = nifti_to_dicom_pixel_spacing(header_in)[:-1]
    slice_thickness = nifti_to_dicom_pixel_spacing(header_in)[-1]
    bits_allocated, photometric_interpretation = nifti_to_dicom_datatype(header_in)

    # Create dictionary to hold DICOM header fields
    dicom_header = {
        'Image Position (Patient)': nifti_to_dicom_image_pos_patient(header_in),
        'Image Orientation (Patient)': nifti_to_dicom_image_orient(header_in),
        'Pixel Spacing': pixel_spacing,
        'Slice Thickness': slice_thickness,
        'Bits Allocated': bits_allocated,
        'Photometric Interpretation': photometric_interpretation,
        'Rescale Slope': 1.0,  # Always nan in NIfTI headers
        'Rescale Intercept': 0.0,  # Always nan in NIfTI headers
        'Rows': nifti_to_dicom_dim(image)[0],
        'Columns': nifti_to_dicom_dim(image)[1],
        'Image Type': plane_to_image_type(anatomical_plane_dicom(nifti_to_dicom_image_orient(header_in))),
        'plane': anatomical_plane_dicom(nifti_to_dicom_image_orient(header_in))
    }

    return dicom_header

def nifti_to_nrrd(header_in):    
    # https://teem.sourceforge.net/nrrd/format.html#space

    sizes = nifti_to_nrrd_sizes(header_in)
    thicknesses = nifti_to_nrrd_thicknesses(header_in)
    data_type = nifti_to_nrrd_type(header_in)
    endian = nifti_to_nrrd_endian(header_in)
    space_origin = nifti_to_nrrd_origin(header_in) 
    space_directions = nifti_to_nrrd_space_directions(header_in) # Similar to image orientation (patient) but with pixel spacing integrated (not unit vector)

    encoding = "raw"
    dimension = len(space_directions)
    space = "left-posterior-superior"
    kinds = ['domain', 'domain', 'domain']

    nrrd_header = {
        'sizes': sizes, # necessary
        'type': data_type, # necessary
        'kinds': kinds, # optional
        'encoding': encoding, # necessary
        'endian': endian, # necessary
        'dimension': dimension, # necessary
        'space': space, # optional, replaces space dimension
        'space origin': space_origin, # optional
        'space directions': space_directions, # optional
        'thicknesses': thicknesses, # optional
    }

    return nrrd_header

def nrrd_to_nrrd(header_in):
    sizes = nrrd_to_nrrd_sizes(header_in)
    space_directions = nrrd_to_nrrd_space_directions(header_in)
    space_origin = nrrd_to_nrrd_space_origin(header_in)
    kinds = nrrd_to_nrrd_kinds(header_in)
    header_in['sizes'] = sizes
    header_in['space directions'] = space_directions
    header_in['space origin'] = space_origin
    header_in['kinds'] = kinds
    return header_in

def nrrd_to_dicom(image, header_in):

    image_position_patient = nrrd_to_dicom_image_pos_patient(header_in)
    pixel_spacing_full = nrrd_to_dicom_pixel_spacing(header_in)
    pixel_spacing = pixel_spacing_full[:-1]
    spacing_between_slices = pixel_spacing_full[-1]
    slice_thickness = spacing_between_slices # This may not always be true   
    bits_allocated, photometric_interpretation = nrrd_to_dicom_datatype(header_in)
    image_orientation_patient = nrrd_to_dicom_image_orient(header_in, pixel_spacing_full)
    rows, columns = nrrd_to_dicom_dim(image)
    image_type = plane_to_image_type(anatomical_plane_dicom(image_orientation_patient))
    plane = anatomical_plane_dicom(image_orientation_patient)

    dicom_header = {
        'Image Position (Patient)': image_position_patient,
        'Image Orientation (Patient)': image_orientation_patient,
        'Pixel Spacing': pixel_spacing,
        'Slice Thickness': slice_thickness,
        'Spacing Between Slices': spacing_between_slices,
        'Bits Allocated': bits_allocated,
        'Photometric Interpretation': photometric_interpretation,
        'Rescale Slope': 1.0,
        'Rescale Intercept': 0.0,
        'Rows': rows,
        'Columns': columns,
        'Image Type': image_type,
        'Plane': plane
    }

    return dicom_header

def nrrd_to_nifti(image, header_in):    

    # Transform header values from NRRD
    pix_dim = np.array(nrrd_to_nifti_pixdim(header_in), dtype=float)
    affine_matrix = nrrd_to_nifti_orientation(header_in)
    data_type, bitpix = nrrd_to_nifti_datatype(header_in)
    scl_slope, scl_inter = nrrd_to_nifti_scl_slope(header_in)
    
    # Clean up very small values in the affine matrix to maintain numerical stability
    affine_matrix[np.abs(affine_matrix) < 1e-6] = 0

    # Access and modify the NIfTI image's header directly
    nifti_img = nib.Nifti1Image(image, affine_matrix)
    header = nifti_img.header
    header['datatype'] = data_type
    header['bitpix'] = bitpix
    header.set_sform(affine_matrix, code=1)  # Set sform and qform codes to 1 (aligned with scanner)
    header.set_qform(affine_matrix, code=1)
    header['scl_slope'] = scl_slope
    header['scl_inter'] = scl_inter
    header['pixdim'] = pix_dim

    return nifti_img

def npy_to_dicom(image):

    image_position_patient = [0, 0, 0]
    image_orientation_patient = [1, 0, 0, 0, 1, 0]
    pixel_spacing = [1, 1]
    slice_thickness = 1
    spacing_between_slices = 1
    bits_allocated, photometric_interpretation = 16, 'MONOCHROME1'
    rows, columns = image.shape[0], image.shape[1]
    plane = 'axial'
    image_type = plane_to_image_type(plane)
    

    dicom_header = {
        'Image Position (Patient)': image_position_patient,
        'Image Orientation (Patient)': image_orientation_patient,
        'Pixel Spacing': pixel_spacing,
        'Slice Thickness': slice_thickness,
        'Spacing Between Slices': spacing_between_slices,
        'Bits Allocated': bits_allocated,
        'Photometric Interpretation': photometric_interpretation,
        'Rescale Slope': 1.0,
        'Rescale Intercept': 0.0,
        'Rows': rows,
        'Columns': columns,
        'Image Type': image_type,
        'Plane': plane
    }

    return dicom_header


# %%
