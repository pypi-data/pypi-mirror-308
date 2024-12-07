#%%

import os
import tkinter as ttk
from tkinter import ttk
from tkinter import messagebox
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import shutil
import math
import threading
import warnings
import pydicom
import traceback
import cv2
from rt_utils import RTStructBuilder
from scipy import ndimage
import random
from customtkinter import *

warnings.filterwarnings("ignore")

# change working directory
script_dir = os.path.dirname(os.path.abspath(__file__))

os.chdir(script_dir)
from conversion import any_to_numpy, rtss_to_npy, ImageConverter

from header_controls import *

class App:
    def __init__(self, master):
        print("init")  

        self.original_master = master # For some weird bug
        self.master = master

        self.mac_platforms = ['darwin', 'macos', 'macosx', 'mac']
        self.linux_platforms = ['linux', 'linux2', 'freebsd']
        self.windows_platforms = ['win32', 'win64']

        # Button padding
        self.button_padx = 0
        self.button_pady = 0

        # Treeview Fonts
        if sys.platform in self.mac_platforms:
            treeview_font = ('SF Display', 10)
            self.treeview_font_heading = ('SF Display', 9, 'bold')
        elif sys.platform in self.windows_platforms:
            treeview_font = ('Roboto', 10)
            self.treeview_font_heading = ('Roboto', 9, 'bold')
        elif sys.platform in self.linux_platforms:
            treeview_font = ('Roboto', 10)
            self.treeview_font_heading = ('Roboto', 10, 'bold')
        else:
            treeview_font = ('Helvetica', 10)
            self.treeview_font_heading = ('Helvetica', 9, 'bold')

        style = ttk.Style()
        style.theme_use("clam")
        # Configure Treeview item appearance
        style.configure("Treeview", 
                        foreground="black", 
                        font=treeview_font)

        # Configure the Treeview header appearance
        style.configure("Treeview.Heading", 
                        background="#2C3F4F",   # Set the background color for the header
                        foreground="white",     # Set the text color for the header
                        relief="raised",          # Remove the border
                        borderwidth=4,
                        bordercolor="white",
                        font=self.treeview_font_heading)     # Set the font for the header
        
        # Configure the Treeview header selected item appearance
        style.map("Treeview.Heading", 
                  foreground=[('selected', 'white')], 
                  background=[('selected', '#2C3F4F')])
        
        # Configure the Treeview selected item appearance
        style.map("Treeview", 
                  foreground=[('selected', 'white')], 
                  background=[('selected', '#4A6984')])
        
        # Allow main content area to expand horizontally and vertically
        self.master.grid_rowconfigure(1, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

        # For tracking last selection for each path
        self.last_selection_dict = {}

        # Initialise the last_update variable
        self.is_updating = False

        # For contours  
        self.colours_list = ['red', 'cyan', 'magenta', 'yellow', 'lime', 'fuchsia', 'aqua', 'orange', 'chartreuse']

        # Initalise the current_path variable
        self.current_path = tk.StringVar(master)
        self.last_valid_path = tk.StringVar(master)
        # path = r"C:\Users\physics\Desktop\BOURNE, James [2203936]"
        path = os.getcwd()
        self.current_path.set(path)  
        self.last_valid_path.set(path) 

        # Initialise the lock variables
        self.lock_slice = tk.IntVar(value=0)
        self.lock_wc = tk.IntVar(value=0)
        self.lock_ww = tk.IntVar(value=0)
        self.view_lock = tk.IntVar(value=0)

        # Initialise resampling lock
        self.enable_resample_shape = tk.IntVar(value=0)
        self.enable_resample_voxel = tk.IntVar(value=0)
        self.enable_crop = tk.IntVar(value=0)
        self.apply_rotations = tk.IntVar(value=0)

        # Initialise image arrays
        self.display_img_array = None
        self.structure_masks = []
        self.hidden_structure_indices = []
        self.structure_names = []
        self.color_boxes = []
        self.structure_checkbuttons = []
        self.slice_info_dict = None

        self.keyboard_or_mouse = 0 # 0 for keyboard, 1 for mouse selection

        self.master.bind('<Left>', self.adjust_slice_slider)
        self.master.bind('<Right>', self.adjust_slice_slider)
        self.master.bind('<Delete>', self.delete_file_or_folder)

        # To prevent delete button being enabled when editing text
        self.last_interaction = None

        # For error handling
        self.errors = []
        self.show_traceback = False

        self.initUI()    
        self.master.bind("<MouseWheel>", self.adjust_slice_slider)

        # For when reloading image with apply affine switch
        self.current_plane = None
        self.current_slice_index = None
        self.current_wc = None
        self.current_ww = None
        self.last_structure_file_paths = None

    def initUI(self):
        print("initUI")

        # Create the path entry at the top of the app
        path_entry_frame = CTkFrame(self.master)
        path_entry_frame.grid_rowconfigure(0, weight=0)  # Ensure does not reshape vertically
        path_entry_frame.grid_columnconfigure(1, weight=1)  # Allow reshape horizontally
        path_entry_frame.grid(row=0, column=0, sticky="ew")
        self.path_entry = CTkEntry(path_entry_frame, textvariable=self.current_path)
        self.path_entry.grid(row=0, column=1, sticky="ew")
        self.go_button = CTkButton(path_entry_frame, text="Go", command=lambda: self.load_files(self.current_path.get()))
        self.go_button.grid(row=0, column=0, sticky="w", padx=self.button_padx, pady=self.button_pady)
        self.path_entry.bind("<Return>", lambda event: self.load_files(self.current_path.get()))
        self.path_entry.bind("<KP_Enter>", lambda event: self.load_files(self.current_path.get()))
        self.current_image_path = None

        # Reset Program Button
        self.reset_button = CTkButton(path_entry_frame, text="Reset App", command=self.restart)
        self.reset_button.grid(row=0, column=2, sticky="w", padx=self.button_padx, pady=self.button_pady)

        # Path controls
        self.path_entry.bind("<Control-a>", self.select_all)
        self.path_entry.bind("<Control-c>", self.copy_to_clipboard)
        self.path_entry.bind("<Control-v>", self.paste_from_clipboard)

        # Paned window
        self.paned_window = ttk.PanedWindow(self.master, orient=tk.HORIZONTAL)
        self.paned_window.grid(row=1, column=0, sticky="nsew") 
        self.paned_window.grid_rowconfigure(0, weight=1)
        self.paned_window.grid_columnconfigure(1, weight=1)
        self.master.grid_rowconfigure(1, weight=1) # Expands rather than path entry


        # Paned Window > Left Frame
        self.left_frame = CTkFrame(self.master)
        self.left_frame.grid_rowconfigure(0, weight=1)
        self.left_frame.grid_columnconfigure(0, weight=1)

        # Left Frame > Browser frame
        self.file_ex_treeview_frame = CTkFrame(self.left_frame)
        self.file_ex_treeview_frame.grid_rowconfigure(0, weight=1)
        self.file_ex_treeview_frame.grid_rowconfigure(1, weight=0)
        self.file_ex_treeview_frame.grid_columnconfigure(0, weight=1) 
        self.init_explorer_treeview()
        self.file_ex_treeview_frame.grid(row=0, column=0, sticky="nsew")

        # Left Frame > Canvas frame
        self.init_canvas_settings()

        # Paned Window > Right Frame
        self.centre_frame = CTkFrame(self.master)
        self.centre_frame.grid_rowconfigure(0, weight=1)
        self.centre_frame.grid_rowconfigure(1, weight=0)
        self.centre_frame.grid_columnconfigure(0, weight=1)

        # Right Frame > Viewer controls frame
        self.viewer_controls_frame = CTkFrame(self.centre_frame)
        self.viewer_controls_frame.grid_columnconfigure(0, weight=0)
        self.viewer_controls_frame.grid_columnconfigure(1, weight=1)
        self.viewer_controls_frame.grid_columnconfigure(2, weight=0)
        self.viewer_controls_frame.grid_columnconfigure(3, weight=0)
        self.viewer_controls_frame.grid(row=1, column=0, sticky="ew")

        axsagcor_row = 0
        slice_slider_row= 1
        wc_slider_row = 2
        ww_slider_row = 3

        # Slice slider (Viewer controls frame)
        self.slice_slider_label = CTkLabel(self.viewer_controls_frame, text="Slice")
        self.slice_slider_label.grid(row=slice_slider_row, column=0, sticky="e")
        self.slice_slider = CTkSlider(self.viewer_controls_frame, from_=1, to=1, orientation=tk.HORIZONTAL)
        self.slice_slider.grid(row=slice_slider_row, column=1, sticky="ew")
        self.slice_value_label = CTkLabel(self.viewer_controls_frame, text="1", width=60)
        self.slice_value_label.grid(row=slice_slider_row, column=2, sticky="ew")
        self.slice_slider.bind("<B1-Motion>", self.apply_slice_change_label)
        self.slice_slider.bind("<ButtonRelease-1>", self.apply_slice_change_label)

        # Window Centre slider (Viewer controls frame)
        self.wc_slider_label = CTkLabel(self.viewer_controls_frame, text="Window Centre")
        self.wc_slider_label.grid(row=wc_slider_row, column=0, sticky="e")
        self.wc_slider = CTkSlider(self.viewer_controls_frame, from_=0, to=0, orientation=tk.HORIZONTAL)
        self.wc_slider.grid(row=wc_slider_row, column=1, sticky="ew")
        self.wc_value_label = CTkLabel(self.viewer_controls_frame, text="0.00", width=60)
        self.wc_value_label.grid(row=wc_slider_row, column=2, sticky="ew")
        self.wc_slider.bind("<B1-Motion>", self.update_wc_label)
        self.wc_slider.bind("<ButtonRelease-1>", self.update_wc_label)

        # Window Width slider (Viewer controls frame)
        self.ww_slider_label = CTkLabel(self.viewer_controls_frame, text="Window Width")
        self.ww_slider_label.grid(row=ww_slider_row, column=0, sticky="e")
        self.ww_slider = CTkSlider(self.viewer_controls_frame, from_=0, to=0, orientation=tk.HORIZONTAL)
        self.ww_slider.grid(row=ww_slider_row, column=1, sticky="ew")
        self.ww_value_label = CTkLabel(self.viewer_controls_frame, text="0.00", width=60)
        self.ww_value_label.grid(row=ww_slider_row, column=2, sticky="ew")
        self.ww_slider.bind("<B1-Motion>", self.update_ww_label)
        self.ww_slider.bind("<ButtonRelease-1>", self.update_ww_label)

        # Disable sliders
        self.slice_slider.configure(state='disabled')
        self.wc_slider.configure(state='disabled')
        self.ww_slider.configure(state='disabled')

        # Slider lock buttons (Viewer controls frame)
        self.slice_lock_button = CTkSwitch(self.viewer_controls_frame, text="🔒", variable=self.lock_slice, width=50)
        self.wc_lock_button = CTkSwitch(self.viewer_controls_frame, text="🔒", variable=self.lock_wc, width=50)
        self.ww_lock_button = CTkSwitch(self.viewer_controls_frame, text="🔒", variable=self.lock_ww, width=50)
        self.slice_lock_button.grid(row=slice_slider_row, column=3, sticky="e")
        self.wc_lock_button.grid(row=wc_slider_row, column=3, sticky="e")
        self.ww_lock_button.grid(row=ww_slider_row, column=3, sticky="e")

        # Ax, Sag, Cor (Viewer controls frame)
        self.ax_sag_cor_frame = CTkFrame(self.viewer_controls_frame)
        self.init_ax_sag_cor(self.ax_sag_cor_frame)
        self.ax_sag_cor_frame.grid(row=axsagcor_row, column=0, sticky="ew", columnspan=3)

        # Lock button
        self.view_lock_button = CTkSwitch(self.viewer_controls_frame, text="🔒", width=50, variable=self.view_lock)
        self.view_lock_button.grid(row=axsagcor_row, column=3, sticky="e")

        # Right Frame
        self.right_frame = CTkFrame(self.master)
        self.right_frame.grid_rowconfigure(0, weight=1)
        self.right_frame.grid_columnconfigure(0, weight=1)

        # Structure TreeView
        self.init_structure_explorer()

        # Options Frame
        self.options_frame = CTkFrame(self.right_frame)
        self.options_frame.grid_columnconfigure(0, weight=1)
        self.options_frame.grid_columnconfigure(1, weight=1)
        self.init_options_frame()
        self.options_frame.grid(row=1, column=0, sticky="nsew")

        # Add the Left/Right frames to the PanedWindow
        self.paned_window.add(self.left_frame)
        self.paned_window.add(self.centre_frame, weight=1)
        self.paned_window.add(self.right_frame)

        # Updating contents in the explorer
        self.load_files(self.current_path.get())

        self.init_canvas()

        # After all widgets are created, define the lists of buttons and switches
        self.all_buttons = [
            self.go_button,
            self.view_image_button,
            self.view_contours_button,
            self.remove_overlays_button,
            self.view_header_button,
            self.select_input_button,
            self.select_output_button,
            self.convert_button,
            self.axial_button,
            self.sagittal_button,
            self.coronal_button
        ]
        # self.apply_button_hover_effects(self.all_buttons)

        self.all_switches = [
            self.slice_lock_button,
            self.wc_lock_button,
            self.ww_lock_button,
            self.scale_image_to_voxels_switch,
            self.apply_affine_switch,
            self.resample_shape_switch,
            self.resample_voxel_switch,
            self.crop_switch
        ]
        # self.apply_switch_effects(self.all_switches)

        # Bind the events
        self.structure_tree.bind("<Motion>", self.on_treeview_hover)
        self.structure_tree.bind("<Leave>", self.on_treeview_leave)

    def restart(self):
        print("restart_program")

        # Close the current window
        self.master.destroy()
        
        # Reinitialize the program
        main()  # Call the main function to restart the program

    def on_treeview_hover(self, event):
        """Change the hover color of the Treeview item."""
        self.last_interaction = "treeview"
        file_explorer_treeview = event.widget
        item = file_explorer_treeview.identify_row(event.y)
        file_explorer_treeview.item(item, tags=('hover',))

    def on_treeview_leave(self, event):
        """Reset the item color when the mouse leaves."""
        self.last_interaction = None
        file_explorer_treeview = event.widget
        item = file_explorer_treeview.identify_row(event.y)
        file_explorer_treeview.item(item, tags=())

    def apply_button_hover_effects(self, buttons):
        for button in buttons:
            button.bind("<Enter>", lambda event, btn=button: btn.configure(text_color="white", fg_color="#0250BB"))
            button.bind("<Leave>", lambda event, btn=button: btn.configure(text_color="white", fg_color="#4A6984"))

    def apply_switch_effects(self, switches):

        for switch in switches:
            switch.configure(height=23, width=40, switch_height=18, switch_width=36)

    def init_structure_explorer(self):
        print("init_structure_explorer")

        # Create a frame specifically for the Treeview and its scrollbar
        self.structure_frame = CTkFrame(self.right_frame)
        self.structure_frame.grid_rowconfigure(0, weight=1)
        self.structure_frame.grid_columnconfigure(0, weight=1)
        self.structure_frame.grid(row=0, column=0, sticky="nsew")

        # Create the Treeview for structures
        self.structure_tree = ttk.Treeview(self.structure_frame, columns=('Visibility', 'Color', 'Structures'), show='headings', height=15)
        self.structure_tree.heading('Visibility', text='👁')
        self.structure_tree.heading('Color', text='🖌️')
        self.structure_tree.heading('Structures', text='Structures')
        self.structure_tree.column('Visibility', anchor='center', width=30, stretch=False)
        self.structure_tree.column('Color', anchor='center', width=30, stretch=False)
        self.structure_tree.column('Structures', anchor='w')
        self.structure_tree.grid(row=0, column=0, sticky="nsew")

        # Add a scrollbar to the structure_frame, attached only to the Treeview
        self.structure_scrollbar = CTkScrollbar(self.structure_frame, orientation="vertical", command=self.structure_tree.yview)
        self.structure_tree.configure(yscrollcommand=self.structure_scrollbar.set)
        self.structure_scrollbar.grid(row=0, column=1, sticky='ns')

        # Bind click event to the "Visibility" heading
        self.structure_tree.heading('Visibility', command=self.toggle_all_structures)

        # Bind the focus event
        self.structure_tree.bind("<FocusIn>", self.on_tree_focus)

        # Bind hover events
        self.structure_tree.bind("<Enter>", self.on_treeview_hover)
        self.structure_tree.bind("<Leave>", self.on_treeview_leave)

        self.structure_tree.bind("<<TreeviewSelect>>", self.on_structure_select)

    def on_structure_select(self, event):
        # Get selected item
        selected_item = self.structure_tree.selection()
        if not selected_item:
            return
        selected_index = self.structure_tree.index(selected_item[0])
        self.find_max_pixel_slice_and_display(selected_index)

    def find_max_pixel_slice_and_display(self, structure_index):
        """Finds the slice with the highest sum of pixel values in the given structure's mask 
        and displays that slice in the current view (axial, sagittal, or coronal), with orientation adjustments."""
        if not self.structure_masks or structure_index >= len(self.structure_masks):
            return

        structure_mask = self.structure_masks[structure_index]

        # Sum pixel values for each slice based on the current view
        if self.plane == 'axial':
            slice_sums = [np.sum(structure_mask[i, :, :]) for i in range(structure_mask.shape[0])]
            max_slice_index = int(np.argmax(slice_sums))
        elif self.plane == 'sagittal':
            # Reverse index for sagittal view
            slice_sums = [np.sum(structure_mask[:, :, structure_mask.shape[2] - i - 1]) for i in range(structure_mask.shape[2])]
            max_slice_index = int(np.argmax(slice_sums))
        elif self.plane == 'coronal':
            # Reverse index for coronal view
            slice_sums = [np.sum(structure_mask[:, structure_mask.shape[1] - i - 1, :]) for i in range(structure_mask.shape[1])]
            max_slice_index = int(np.argmax(slice_sums))

        # Set the slice slider to the identified slice
        self.slice_slider.set(max_slice_index)
        self.apply_slice_change_label(None)  # Update the view to the new slice

    def update_structure_treeview(self, structure_names):
        # Clear the current items in the Treeview
        for item in self.structure_tree.get_children():
            self.structure_tree.delete(item)

        # Add the structure names and corresponding colors to the Treeview
        self.colours_list = ['red', 'cyan', 'magenta', 'yellow', 'lime', 'fuchsia', 'aqua', 'orange', 'chartreuse']

        for i, name in enumerate(structure_names):
            color = self.colours_list[i % len(self.colours_list)]  # Cycle through colors
            item_id = self.structure_tree.insert('', 'end', values=('', '', name))
            self.create_color_box(item_id, color)
            self.add_checkbutton(item_id)

        # Force the Treeview to update the display
        self.structure_tree.update_idletasks()

        # Now, create the color boxes
        for i, name in enumerate(structure_names):
            color = self.colours_list[i % len(self.colours_list)]  # Cycle through colors
            item_id = self.structure_tree.get_children()[i]  # Get item id after insertion
            self.create_color_box(item_id, color)

    def add_checkbutton(self, item_id):
        bbox = self.structure_tree.bbox(item_id, column=0)  # Update to column=0 for the first column
        if bbox:
            x, y, width, height = bbox
            check_var = tk.BooleanVar(value=True)
            checkbutton = CTkCheckBox(self.structure_tree, variable=check_var, command=lambda: self.toggle_structure(item_id, check_var), text='', width=width, height=height, border_width=0, corner_radius=0, fg_color='#ffffff', hover_color='#697b88', checkmark_color="black")
            checkbutton.place(x=x, y=y)
            self.structure_checkbuttons.append((checkbutton, check_var))  # Store the reference to the checkbutton and its variable

        self.structure_tree.update_idletasks()

    def create_color_box(self, item_id, color):
        # Get the bounding box of the cell in column 1 (which is now for colors)
        bbox = self.structure_tree.bbox(item_id, column=1)
        if bbox:
            x, y, width, height = bbox
            # Create a Canvas to show the color box
            canvas = tk.Canvas(self.structure_tree, width=width, height=height, highlightthickness=0)
            canvas.create_rectangle(0, 0, width, height, fill=color, outline=color)
            canvas.place(x=x, y=y)
            self.color_boxes.append(canvas)

    def toggle_structure(self, item_id, check_var):
        is_visible = check_var.get()
        structure_index = self.structure_tree.index(item_id)

        if is_visible:
            # Code to show the structure
            self.show_structure(structure_index)
        else:
            # Code to hide the structure
            self.hide_structure(structure_index)

        # Refresh the image
        self.render_image()

    def show_structure(self, index):
        self.hidden_structure_indices.remove(index)
        self.render_image()

    def hide_structure(self, index):
        self.hidden_structure_indices.append(index)
        self.render_image()

    def toggle_all_structures(self):
        all_hidden = len(self.hidden_structure_indices) == len(self.structure_names)
        
        if all_hidden:
            # Show all structures and check all checkboxes
            self.hidden_structure_indices.clear()  # Clear the list to show all structures
            for i in range(len(self.structure_names)):
                self.structure_checkbuttons[i][1].set(True)  # Set the BooleanVar to True
        else:
            # Hide all structures and uncheck all checkboxes
            self.hidden_structure_indices = list(range(len(self.structure_names)))  # Hide all structures
            for i in range(len(self.structure_names)):
                self.structure_checkbuttons[i][1].set(False)  # Set the BooleanVar to False

        # Refresh the image to apply changes
        self.render_image()

    def init_canvas_settings(self):
        print("init_canvas_settings")

        # Contour settings are now placed in the left_frame, below the Treeview frame
        self.contour_settings = CTkFrame(self.left_frame)
        self.contour_settings.grid(row=1, column=0, sticky="nsew")

        # Configure all 4 columns in contour_settings to expand
        for col in range(4):
            self.contour_settings.grid_columnconfigure(col, weight=1)

        # Directly create the label with padding to simulate the white border
        font = self.treeview_font_heading
        font = (font[0], font[1] + 3, font[2])

        # The main label with a simulated white border using padding
        title_label = CTkLabel(
            self.contour_settings,
            text="Canvas",
            font=font,
            anchor="center",
            fg_color="#2C3F4F",
            text_color="white",
            height=25
        )
        title_label.grid(row=0, column=0, columnspan=4, sticky="ew", padx=3, pady=(3, 1))  # Placed below the buttons

        # Add the new frame for view and convert buttons below the header label
        frame_view_buttons = CTkFrame(self.contour_settings)
        frame_view_buttons.grid(row=1, column=0, sticky="nsew", columnspan=4)

        # Configure all 4 columns in frame_view_buttons to expand
        for col in range(4):
            frame_view_buttons.grid_columnconfigure(col, weight=1)

        # View Image and View Contours buttons each span 2 columns
        self.view_image_button = CTkButton(
            frame_view_buttons,
            text="View Image",
            command=self.view_image,
            width=150
        )
        self.view_image_button.grid(row=0, column=0, sticky="ew", padx=self.button_padx, pady=self.button_pady, columnspan=2)

        self.view_contours_button = CTkButton(
            frame_view_buttons,
            text="View Contours",
            width=150,
            command=self.view_structures
        )

    

        self.view_contours_button.grid(row=0, column=2, sticky="ew", padx=self.button_padx, pady=self.button_pady, columnspan=2)

        # Clear Contours and View Header buttons each span 2 columns
        self.remove_overlays_button = CTkButton(
            frame_view_buttons,
            text="Clear Contours",
            width=150,
            command=self.clear_contours
        )

        self.remove_overlays_button.grid(row=1, column=2, sticky="ew", padx=self.button_padx, pady=self.button_pady, columnspan=2)

        self.view_header_button = CTkButton(
            frame_view_buttons,
            text="View Header",
            width=150,
            command=lambda: view_header(
                self.master,
                os.path.join(self.last_valid_path.get(), self.get_selection()[0])
            )
        )
        self.view_header_button.grid(row=1, column=0, sticky="ew", padx=self.button_padx, pady=self.button_pady, columnspan=2)

        # Scale aspect ratio to voxel spacing switch
        self.scale_image_view_to_voxels = tk.BooleanVar(self.master)
        self.scale_image_view_to_voxels.set(True)
        self.scale_image_to_voxels_switch = CTkSwitch(
            self.contour_settings,
            text="Scale to Physical Space",
            variable=self.scale_image_view_to_voxels
        )
        self.scale_image_to_voxels_switch.grid(row=4, column=0, sticky="w", padx=2, columnspan=4)
        self.scale_image_view_to_voxels.trace_add('write', lambda *args: self.on_voxel_spacing_toggle())

        # Apply affine to image view switch
        self.apply_affine = tk.BooleanVar(self.master)
        self.apply_affine.set(False)
        self.apply_affine_switch = CTkSwitch(
            self.contour_settings,
            text="LPS Orientation (Resample)",
            variable=self.apply_affine,
            command=self.on_apply_affine_toggle
        )
        self.apply_affine_switch.grid(row=5, column=0, sticky="w", padx=2, columnspan=4)

        # Colormap Frame
        self.contour_colormap_frame = CTkFrame(self.contour_settings)
        self.contour_colormap_frame.grid(row=2, column=0, sticky="ew", padx=0, columnspan=4)

        # Configure the grid for contour_colormap_frame
        self.contour_colormap_frame.grid_columnconfigure(0, weight=0)  # Combobox column
        self.contour_colormap_frame.grid_columnconfigure(1, weight=1)  # Label column

        # Image color map combobox
        self.color_map = tk.StringVar(value="grey")
        self.color_map_combobox = CTkComboBox(
            self.contour_colormap_frame,
            values=["gray", "bone", "cividis", "jet", "hot", "magma", "plasma"],
            command=self.set_color_map,
            variable=self.color_map,
            width=110,
            state="readonly",
            dropdown_fg_color="white",
            dropdown_hover_color="gray90"
        )
        self.color_map_combobox.grid(row=0, column=0, sticky="ew", padx=2, pady=1)

        # Image color map label
        self.color_map_label = CTkLabel(
            self.contour_colormap_frame,
            text="Colormap",
            anchor="w"  # Ensure text is left-aligned within the label
        )
        self.color_map_label.grid(row=0, column=1, sticky="w", padx=2, pady=1)

        # Starting View Frame
        self.contour_view_frame = CTkFrame(self.contour_settings)
        self.contour_view_frame.grid(row=3, column=0, sticky="ew", padx=0, columnspan=4)

        # Configure the grid for contour_view_frame
        self.contour_view_frame.grid_columnconfigure(0, weight=0)  # Combobox column
        self.contour_view_frame.grid_columnconfigure(1, weight=1)  # Label column

        # Starting View combobox
        self.starting_view = tk.StringVar(value="auto")
        self.starting_view_combobox = CTkComboBox(
            self.contour_view_frame,
            values=["auto", "axial", "sagittal", "coronal"],
            variable=self.starting_view,
            width=110,
            state="readonly",
            dropdown_fg_color="white",
            dropdown_hover_color="gray90"
        )
        self.starting_view_combobox.grid(row=0, column=0, sticky="ew", padx=2, pady=1)

        # Starting View label
        self.starting_view_label = CTkLabel(
            self.contour_view_frame,
            text="Starting View",
            anchor="w"  # Ensure text is left-aligned within the label
        )
        self.starting_view_label.grid(row=0, column=1, sticky="w", padx=2, pady=1)

        # Outline switch
        self.contour_outline_switch_val = tk.BooleanVar(value=True)
        self.contour_outline_switch = CTkSwitch(
            self.contour_settings,
            variable=self.contour_outline_switch_val,
            text="Contour Linewidth",
            command=self.set_contour_outline,
            width=50
        )
        self.contour_outline_switch.grid(row=6, column=0, sticky="w", padx=2, columnspan=1)

        # Linewidth slider
        slider_width = 125  # Controls starting width of right frame
        self.linewidth_slider = CTkSlider(
            self.contour_settings,
            from_=1,
            to=10,
            command=self.set_contour_linewidth,
            state="normal",
            number_of_steps=10,
            width=slider_width
        )
        self.linewidth_slider.set(1)
        self.linewidth_value = CTkLabel(self.contour_settings, text="1px", width=40, anchor="w")
        self.linewidth_slider.grid(row=6, column=2, sticky="ew")
        # self.linewidth_value.grid(row=6, column=3, sticky="w")

        # Fill switch
        self.contour_fill_switch_val = tk.BooleanVar(value=False)
        self.contour_fill_switch = CTkSwitch(
            self.contour_settings,
            variable=self.contour_fill_switch_val,
            text="Contour Opacity",
            command=self.set_contour_fill,
            width=50
        )
        self.contour_fill_switch.grid(row=7, column=0, sticky="w", padx=2, columnspan=2)

        # Opacity slider
        self.opacity_slider = CTkSlider(
            self.contour_settings,
            from_=1,
            to=100,
            command=self.set_contour_opacity,
            number_of_steps=100,
            state="normal",
            width=slider_width
        )
        self.opacity_slider.set(25)
        self.opacity_value = CTkLabel(self.contour_settings, text="25%", width=40, anchor="w")
        self.opacity_slider.grid(row=7, column=2, sticky="ew")
        # self.opacity_value.grid(row=7, column=3, sticky="w")

        # Export current canvas as image
        self.export_button = CTkButton(
            self.contour_settings,
            text="Export Canvas as PNG",
            command=self.export_image
        )
        self.export_button.grid(row=8, column=0, columnspan=4, sticky="ew", padx=self.button_padx, pady=self.button_pady)




    def set_color_map(self, value):
        print("set_color_map")

        if self.display_img_array is not None:
            self.render_image()

    def set_contour_outline(self):
        print("set_contour_outline")

        if self.contour_outline_switch_val.get():
            self.linewidth_slider.configure(state="normal")
        else:
            self.linewidth_slider.configure(state="disabled")

        if self.display_img_array is not None:
            self.render_image()

    def set_contour_linewidth(self, value):
        print("set_contour_linewidth")

        self.linewidth_value.configure(text=f"{value:.0f}px")

        self.render_image()

    def set_contour_fill(self):
        print("set_contour_fill")

        if self.contour_fill_switch_val.get():
            self.opacity_slider.configure(state="normal")
        else:
            self.opacity_slider.configure(state="disabled")

        if self.display_img_array is not None:
            self.render_image()

    def set_contour_opacity(self, value):
        print("set_contour_opacity")

        self.opacity_value.configure(text=f"{value:.0f}%")

        self.render_image()

    def export_image(self):
        print("export_image")

        if self.display_img_array is not None:
            # Get the path where the image will be saved
            current_slice = self.slice_slider.get()
            file_name = f"exported_image_slice_{int(current_slice)}.png"
            export_path = os.path.join(self.current_path.get(), file_name)
            
            # Save the current view of the canvas to a file
            self.fig.savefig(export_path, bbox_inches='tight', pad_inches=0)
            print(f"Image exported successfully to: {export_path}")            

    def init_explorer_treeview(self):
        print("init_explorer_treeview")

        self.file_explorer_treeview = ttk.Treeview(self.file_ex_treeview_frame, columns=('Browser',), show='headings', height=15)
        self.file_explorer_treeview.heading('Browser', text='Browser')
        self.file_explorer_treeview.column('Browser', anchor='w', width=280)
        self.file_explorer_treeview.pack(side='left', fill='both', expand=True)

        scrollbar = CTkScrollbar(self.file_ex_treeview_frame, orientation="vertical", command=self.file_explorer_treeview.yview)
        self.file_explorer_treeview.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')

        # Bind single click event to update last_selection_dict
        self.file_explorer_treeview.bind('<<TreeviewSelect>>', self.single_click)

        self.file_explorer_treeview.bind('<Double-1>', self.double_click)
        self.file_explorer_treeview.bind("<FocusIn>", self.on_tree_focus)  # Bind the focus event

        # Bind hover events
        self.file_explorer_treeview.bind("<Enter>", self.on_treeview_hover)
        self.file_explorer_treeview.bind("<Leave>", self.on_treeview_leave)

    def single_click(self, event):
        self.last_interaction = 'treeview'

        selected_items = self.file_explorer_treeview.selection()

        # Check if any item is selected
        if selected_items:
            selected_item = self.file_explorer_treeview.item(selected_items[0], 'values')[0]

            # Ignore the ".." entry
            if selected_item != "..":
                normalized_current_path = os.path.normpath(self.current_path.get())
                # Update the dictionary with the normalized path and selected file/folder name
                self.last_selection_dict[normalized_current_path] = selected_item

    def double_click(self, event):
        print("double_click")

        selected_item = self.file_explorer_treeview.item(self.file_explorer_treeview.selection()[0], 'values')[0]

        # Normalize the current path to ensure consistent formatting
        normalized_current_path = os.path.normpath(self.current_path.get())

        # Ignore the ".." entry
        if selected_item == "..":
            new_path = os.path.dirname(normalized_current_path)  # Go up one directory
        else:
            # Update the dictionary with the normalized path and selected file/folder name
            self.last_selection_dict[normalized_current_path] = selected_item

            new_path = os.path.join(normalized_current_path, selected_item.replace("📁 ", ""))  # Remove folder emoji if present

        # Load the new path or view the image
        if os.path.isdir(new_path):
            self.load_files(new_path)
            self.current_path.set(new_path)
        else:
            self.view_image()

    def load_files(self, path):
            print("load_files")

            # Normalize the path to ensure consistent formatting
            normalized_path = os.path.normpath(path)

            # Clear the Treeview
            for item in self.file_explorer_treeview.get_children():
                self.file_explorer_treeview.delete(item)

            # Add ".." to allow navigation to the parent directory
            self.file_explorer_treeview.insert('', 'end', values=("..", "Navigate Up"), tags=('dir',))

            folders = []
            contents = []

            # Allowed image extensions
            allowed_extensions = ['.gz', '.dcm', '.jpg', '.jpeg', '.png', '.nrrd', '.bmp', '.gif', '.npy', '.nii', '.npz']

            # Update last_files_list
            try:
                entries = os.listdir(normalized_path)
            except PermissionError:
                messagebox.showerror("Error", "No permission to access this directory")
                return

            self.last_files_list = entries

            for entry in entries:
                full_path = os.path.join(normalized_path, entry)
                
                if os.path.isdir(full_path):
                    folders.append((entry, 'Directory'))
                else:
                    file_name, file_extension = os.path.splitext(entry)
                    if file_extension.lower() in allowed_extensions:
                        contents.append((entry, 'File'))
                    else:
                        try:
                            file_path = os.path.join(normalized_path, entry)
                            pydicom.dcmread(file_path, stop_before_pixels=True)
                            contents.append((entry, 'DICOM File'))
                        except Exception as e:
                            pass

            # Sort folders and contents
            folders.sort()
            contents.sort()

            # Insert folders first, then contents
            for folder_name, folder_type in folders:
                self.file_explorer_treeview.insert('', 'end', values=(f"📁 {folder_name}", folder_type), tags=('dir',))
            for file_name, file_type in contents:
                self.file_explorer_treeview.insert('', 'end', values=(file_name, file_type), tags=('file',))

            # Restore last selection if the normalized path is in the dictionary and it’s not ".."
            if normalized_path in self.last_selection_dict and self.last_selection_dict[normalized_path] != "..":
                last_selected_name = self.last_selection_dict[normalized_path]

                # Loop through all TreeView items and find the one matching the stored file/folder name
                for item in self.file_explorer_treeview.get_children():
                    item_name = self.file_explorer_treeview.item(item, 'values')[0]
                    if item_name == last_selected_name:
                        self.file_explorer_treeview.selection_set(item)
                        self.file_explorer_treeview.see(item)  # Scroll to the item

            self.last_valid_path.set(normalized_path)

    def init_options_frame(self):
        print("init_options_frame")

        font = self.treeview_font_heading
        font = (font[0], font[1] + 3, font[2])

        # The main label with a simulated white border using padding
        title_label = CTkLabel(
            self.options_frame,
            text="Conversion",
            font=font,
            anchor="center",
            fg_color="#2C3F4F",
            text_color="white",
            height=25
        )
        title_label.grid(row=2, column=0, columnspan=2, sticky="ew", padx=3, pady=(3, 1))  # Placed below the buttons

        # Select buttons and paths self.options_frame
        frame_paths = CTkFrame(self.options_frame)
        frame_paths.grid(row=4, column=0, sticky="nsew", columnspan=2)
        frame_paths.grid_columnconfigure(0, weight=0)
        frame_paths.grid_columnconfigure(1, weight=1)

        # Select buttons
        self.select_input_button = CTkButton(frame_paths, text="Select Input", command=self.set_input_path, width=115)
        self.select_output_button = CTkButton(frame_paths, text="Select Output", command=self.set_output_path, width=115)
        self.select_input_button.grid(row=1, column=0, sticky="w", padx=self.button_padx, pady=self.button_pady)
        self.select_output_button.grid(row=2, column=0, sticky="w", padx=self.button_padx, pady=self.button_pady)

        # Paths
        self.path_in = tk.StringVar(self.master)
        self.out_dir = tk.StringVar(self.master)
        self.input_path_entry = CTkEntry(frame_paths, textvariable=self.path_in)
        self.output_path_entry = CTkEntry(frame_paths, textvariable=self.out_dir)
        self.input_path_entry.grid(row=1, column=1, sticky="nsew", pady=(0, 1))
        self.output_path_entry.grid(row=2, column=1, sticky="nsew", pady=(0, 0))

        # Comboboxes
        self.comboboxes_frame = CTkFrame(self.options_frame)
        self.comboboxes_frame.grid(row=5, column=0, sticky="w", columnspan=2)
        self.comboboxes_frame.grid_columnconfigure(0, weight=0)
        self.comboboxes_frame.grid_columnconfigure(1, weight=0)

        self.output_format_combobox = CTkComboBox(self.comboboxes_frame, values=["DICOM", "NifTI", "NRRD", "NumPy"], state="readonly", width=110, justify="left", dropdown_fg_color="white", dropdown_hover_color="gray90")
        self.output_format_combobox.grid(row=0, column=0, sticky="w", padx=1, pady=1)
        self.output_format_label = CTkLabel(self.comboboxes_frame, text="Output Format", anchor="w", justify="left", width=110, padx=5, pady=1)
        self.output_format_label.grid(row=0, column=1, sticky="w")

        self.interpolation_type_combobox = CTkComboBox(
            self.comboboxes_frame, 
            values=["Nearest Neighbor", "Linear", "BSpline", 
                    "Gaussian", "Cosine Windowed Sinc", "Hamming Windowed Sinc"], 
            state="readonly", 
            width=110, 
            justify="left", 
            dropdown_fg_color="white", 
            dropdown_hover_color="gray90"
        )
        self.interpolation_type_combobox.grid(row=1, column=0, sticky="w", padx=1, pady=1)
        interpolation_type_combobox_label = CTkLabel(self.comboboxes_frame, text="Interpolation Type", anchor="w", justify="left", width=110, padx=5, pady=1)
        interpolation_type_combobox_label.grid(row=1, column=1, sticky="w")

        # Resampling frame
        self.resample_frame = CTkFrame(self.options_frame)
        self.resample_frame.grid(row=6, column=0, sticky="w")
        self.resample_frame.grid_columnconfigure(0, weight=0)
        self.resample_frame.grid_columnconfigure(1, weight=1)

        # Resample to shape
        self.resample_shape_entry = CTkEntry(self.resample_frame, width=110)
        self.resample_shape_entry.grid(row=0, column=0, sticky="w", padx=1, pady=1)
        self.resample_shape_switch = CTkSwitch(self.resample_frame, variable=self.enable_resample_shape, text="Resample to Shape")
        self.resample_shape_switch.grid(row=0, column=1, sticky="w", padx=1)

        # Resample to voxel sizes
        self.resample_voxel_entry = CTkEntry(self.resample_frame, width=110)
        self.resample_voxel_entry.grid(row=1, column=0, sticky="w", padx=1, pady=1)
        self.resample_voxel_switch = CTkSwitch(self.resample_frame, variable=self.enable_resample_voxel, text="Resample to Voxel Sizes")
        self.resample_voxel_switch.grid(row=1, column=1, sticky="w", padx=1)

        # Crop
        self.crop_entry = CTkEntry(self.resample_frame, width=110)
        self.crop_entry.grid(row=2, column=0, sticky="w", padx=1, pady=1)
        self.crop_switch = CTkSwitch(self.resample_frame, variable=self.enable_crop, text="Crop to Shape")
        self.crop_switch.grid(row=2, column=1, sticky="w", padx=1)

        # Apply rotations
        self.lps_convert_switch = CTkSwitch(self.resample_frame, variable=self.apply_rotations, text="LPS Image Matrix Orientation (Resample)")
        self.lps_convert_switch.grid(row=3, column=0, sticky="w", padx=2, pady=self.button_pady, columnspan=2)

        # Make font smaller
        entries = [self.resample_shape_entry, self.resample_voxel_entry, self.crop_entry]
        for entry in entries:
            if sys.platform in self.mac_platforms:
                entry.configure(font=("SF Display", 11))
            elif sys.platform in self.linux_platforms or sys.platform in self.windows_platforms:
                entry.configure(font=("Roboto", 11))

        self.setup_entry_state_triggers()
        self.update_resample_shape_state()  # Ensure initial state is correct
        self.update_resample_voxel_state()
        self.update_crop_state()

        # Convert button
        self.convert_button = CTkButton(self.options_frame, text="Convert", command=self.start_image_conversion, width=300)
        self.convert_button.grid(row=7, column=0, sticky="sew", columnspan=2, padx=self.button_padx, pady=self.button_pady)

        # Bind focus-in event for paths to prevent delete button affect Browser
        self.path_entry.bind("<FocusIn>", self.on_path_field_focus)
        self.input_path_entry.bind("<FocusIn>", self.on_path_field_focus)
        self.output_path_entry.bind("<FocusIn>", self.on_path_field_focus)
        self.resample_shape_entry.bind("<FocusIn>", self.on_path_field_focus)
        self.resample_voxel_entry.bind("<FocusIn>", self.on_path_field_focus)

    def init_ax_sag_cor(self, frame):
        print("init_ax_sag_cor")

        # Axial, Sagittal, Coronal buttons
        self.axial_button = CTkButton(frame, text="Axial", command=lambda: self.swap_view('axial'))
        self.axial_button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=self.button_padx, pady=self.button_pady)

        self.sagittal_button = CTkButton(frame, text="Sagittal", command=lambda: self.swap_view('sagittal'))
        self.sagittal_button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=self.button_padx, pady=self.button_pady)

        self.coronal_button = CTkButton(frame, text="Coronal", command=lambda: self.swap_view('coronal'))
        self.coronal_button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=self.button_padx, pady=self.button_pady)

        self.view_buttons = [self.axial_button, self.sagittal_button, self.coronal_button]

    def init_canvas(self):
        print("init_canvas")

        self.fig = plt.Figure(facecolor="grey")
        self.ax = self.fig.add_subplot(111)
        self.ax.axis('off')  # Hide axes

        # Embed the figure in a Tkinter canvas
        self.canvas_image = FigureCanvasTkAgg(self.fig, master=self.centre_frame)
        self.canvas_widget = self.canvas_image.get_tk_widget()
        self.canvas_widget.grid(row=0, column=0, sticky="nsew")

        self.canvas_widget.bind("<Enter>", self.on_canvas_hover)
        self.canvas_widget.bind("<Leave>", self.on_canvas_leave)  # Ensure this is bound

        # Bind mouse wheel events
        if sys.platform in self.windows_platforms or sys.platform in self.mac_platforms:
            self.canvas_widget.bind("<MouseWheel>", self.adjust_slice_slider)
        elif sys.platform in self.linux_platforms:
            self.canvas_widget.bind("<Button-4>", self.adjust_slice_slider)
            self.canvas_widget.bind("<Button-5>", self.adjust_slice_slider)

        # Bind mouse motion event to display pixel value
        self.canvas_image.mpl_connect('motion_notify_event', self.on_mouse_move)

        self.canvas_image.draw()  # Redraw the canvas to update colors

    def on_canvas_hover(self, event):
        self.last_interaction = 'canvas'

    def on_canvas_leave(self, event):
        self.hide_annotation()
        self.last_interaction = None
        self.canvas_image.draw_idle()

    def setup_entry_state_triggers(self):
        print("setup_entry_state_triggers")

        # Trigger function setup for checkbox state changes
        self.enable_resample_shape.trace_add('write', self.update_resample_shape_state)
        self.enable_resample_voxel.trace_add('write', self.update_resample_voxel_state)
        self.enable_crop.trace_add('write', self.update_crop_state)

    def update_resample_shape_state(self, *args):
        print("update_resample_shape_state")

        if self.enable_resample_shape.get() == 1:
            self.resample_shape_entry.configure(state='normal')

            # Disable resample voxel if resample shape is enabled
            self.enable_resample_voxel.set(0)
            self.update_resample_voxel_state()

            # Disable crop if resample shape is enabled
            self.enable_crop.set(0)
            self.update_crop_state()
            
            self.interpolation_type_combobox.configure(state='readonly')
            self.interpolation_type_combobox.set('Linear')
        else:
            self.resample_shape_entry.configure(state='readonly')
            self.interpolation_type_combobox.configure(state='disabled')
        
        if self.enable_resample_shape.get() == 0 and self.enable_resample_voxel.get() == 0:
            self.interpolation_type_combobox.configure(state='normal')
            self.interpolation_type_combobox.set('')
            self.interpolation_type_combobox.configure(state='disabled')

    def update_resample_voxel_state(self, *args):
        print("update_resample_voxel_state")

        if self.enable_resample_voxel.get() == 1:
            self.resample_voxel_entry.configure(state='normal')

            # Disable resample shape if resample voxel is enabled
            self.enable_resample_shape.set(0)
            self.update_resample_shape_state()

            self.interpolation_type_combobox.configure(state='normal')
            self.interpolation_type_combobox.set('Linear')
        else:
            self.resample_voxel_entry.configure(state='readonly')
            self.interpolation_type_combobox.configure(state='disabled')
        
        if self.enable_resample_shape.get() == 0 and self.enable_resample_voxel.get() == 0:
            self.interpolation_type_combobox.configure(state='normal')
            self.interpolation_type_combobox.set('')
            self.interpolation_type_combobox.configure(state='disabled')

    def update_crop_state(self, *args):
        print("update_crop_state")

        if self.enable_crop.get() == 1:
            self.crop_entry.configure(state='normal')

            # Disable resample to shape if crop is enabled
            self.enable_resample_shape.set(0)
            self.update_resample_shape_state()
            self.update_resample_voxel_state()

        else:
            self.crop_entry.configure(state='readonly')

    def on_apply_affine_toggle(self):
        print("on_apply_affine_toggle")
        # Save current view settings
        self.current_plane = self.plane
        self.current_slice_index = int(self.slice_slider.get()) if self.slice_slider.cget('state') == 'normal' else 0
        self.current_wc = self.wc_slider.get()
        self.current_ww = self.ww_slider.get()
        self.reload_image_and_structures()

    def reload_image_and_structures(self):
        print("reload_image_and_structures")
        if self.current_image_path:
            had_structures = False if len(self.structure_names) == 0 else True
            self.clear_contours()  # Remove prior contours
            self.prepare_for_image(self.current_image_path, reload=True)  # Re-prepare the image

            # Restore the view buttons' state
            for button in self.view_buttons:
                button.configure(state="normal")
            if self.plane == 'axial':
                self.axial_button.configure(state="disabled")
            elif self.plane == 'sagittal':
                self.sagittal_button.configure(state="disabled")
            elif self.plane == 'coronal':
                self.coronal_button.configure(state="disabled")
            self.update_button_state_appearance()

            print('self.structure_names', self.structure_names)

            # Reload structures
            if self.last_structure_file_paths is not None:
                # Non-RTSS structures
                new_structure_masks = []
                new_structure_names = []
                for file_path in self.last_structure_file_paths:
                    mask = any_to_numpy(file_path, "viewing", self.apply_affine.get())[0]
                    new_structure_masks.append(mask)
                    name = os.path.basename(file_path)
                    new_structure_names.append(name)
                self.structure_masks = new_structure_masks
                self.structure_names = new_structure_names
                # Binarize structure masks
                self.structure_masks = [(mask >= 0.5).astype(int) for mask in self.structure_masks]
                # Update the structure treeview and render the image
                self.update_structure_treeview(self.structure_names)
                self.render_image()
            elif self.slice_info_dict is not None and had_structures:
                # RTSS structures
                rtss_path = self.find_rtss(self.current_image_path, self.slice_info_dict)
                new_structure_masks, file_path, new_structure_names = rtss_to_npy(
                    rtss_path, self.slice_info_dict, self.apply_affine.get())
                self.structure_masks = new_structure_masks
                self.structure_names = new_structure_names
                # Binarize structure masks
                self.structure_masks = [(mask >= 0.5).astype(int) for mask in self.structure_masks]
                # Update the structure treeview and render the image
                self.update_structure_treeview(self.structure_names)
                self.render_image()
            else:
                # No structures to reload
                self.render_image()



    def on_path_field_focus(self, event):
        print("on_path_field_focus")
        self.last_interaction = 'path_field'

    def on_tree_focus(self, event):
        print("on_tree_focus")
        self.last_interaction = 'treeview'

    def prepare_for_image(self, file_path=None, reload=False):
        """Prepare the image for display, adjusting sliders and restoring previous settings."""
        print("prepare_for_image")

        self.structure_masks = []  # Remove prior structures

        if file_path is None:
            file_path = os.path.join(self.current_path.get(), self.get_selection()[0])
            self.current_image_path = file_path

        # Load header
        self.header_info, _ = get_header_info(file_path)
        if self.header_info is None:
            self.log_error(f"Incompatible file: {file_path}.")
            self.show_errors_and_traceback()
            return
        
        # Load image
        self.display_img_array, self.slice_info_dict, self.plane, self.voxel_spacing, self.rotation_matrix, self.input_format, _, self.structure_names = any_to_numpy(file_path, "viewing", self.apply_affine.get())

        # Split image and masks if loading image from RTSS file
        if isinstance(self.display_img_array, list):
            self.display_img_array, self.structure_masks = self.display_img_array[0], self.display_img_array[1]

        # Handle None values in voxel spacing
        if None in self.voxel_spacing:
            for i, el in enumerate(self.voxel_spacing):
                if el is None:
                    self.voxel_spacing[i] = 1

        self.interpolation_order = 2
        self.original_shape = self.display_img_array.shape
        self.display_img_array = self.display_img_array.astype(np.float32)

        if reload and self.current_plane is not None:
            # Restore previous plane if reloading
            self.plane = self.current_plane
        else:
            # Reset current_plane when loading a new image
            self.current_plane = None

        # Initialize sliders
        self.init_sliders()

        # Restore previous window center (wc) and window width (ww) if reloading
        if reload and self.current_wc is not None and self.current_ww is not None:
            self.wc_slider.set(self.current_wc)
            self.ww_slider.set(self.current_ww)
        else:
            # Reset wc and ww
            self.current_wc = None
            self.current_ww = None

        # Get the maximum slice index from the slider
        max_slice = int(self.slice_slider.cget("to"))

        # Reapply the stored slice index if the slice lock is on
        if reload and self.current_slice_index is not None and self.lock_slice.get() == 1:
            if 0 <= self.current_slice_index <= max_slice:
                self.slice_slider.set(self.current_slice_index)
            else:
                self.current_slice_index = None  # Reset if out of range
        else:
            # Reset current_slice_index
            self.current_slice_index = None
            # Set to middle slice if lock is off
            middle_slice = max_slice // 2
            self.slice_slider.set(middle_slice)

        # Reset view buttons
        for button in self.view_buttons:
            button.configure(state="normal")

        # Get the view from the combobox or fallback to plane if set to 'auto'
        view = self.starting_view_combobox.get() if self.starting_view_combobox.get() != 'auto' else self.plane

        # Swap the view and disable the corresponding button
        if view == 'axial':
            self.swap_view('axial')
            self.axial_button.configure(state="disabled")
        elif view == 'sagittal':
            self.swap_view('sagittal')
            self.sagittal_button.configure(state="disabled")
        elif view == 'coronal':
            self.swap_view('coronal')
            self.coronal_button.configure(state="disabled")

        # Update resample entries
        self.update_resample_shape_entry()
        self.update_resample_voxel_entry()
        self.update_crop_entry()
        self.update_button_state_appearance()
        if not (self.structure_names is None or self.structure_names == []):
            self.update_structure_treeview(self.structure_names)

    def update_button_state_appearance(self):
        for button in self.all_buttons:
            if button.cget("state") == 'disabled':
                button.configure(fg_color='#2C3F4F')
            else:
                button.configure(fg_color='#4A6984')

    def on_voxel_spacing_toggle(self):
        print('on_voxel_spacing_toggle')

        if self.display_img_array is not None:
            self.render_image()

    def init_sliders(self):
        print("init_sliders")

        # Setup wc and ww sliders
        self.init_slice_slider()
        self.init_window_sliders()

        # Update slider labels (current values)
        self.apply_slice_change_label(None)
        self.wc_slider.configure(state='normal')
        self.ww_slider.configure(state='normal')
        self.update_wc_label(None)
        self.update_ww_label(None)

    def init_slice_slider(self):
        print("init_slice_slider")

        min_val = 0
        if self.plane == 'axial':
            max_val = self.display_img_array.shape[0] - 1
        elif self.plane == 'sagittal':
            max_val = self.display_img_array.shape[2] - 1
        elif self.plane == 'coronal':
            max_val = self.display_img_array.shape[1] - 1

        if min_val == max_val:
            # Handle the single-slice case without calling set()
            self.slice_value_label.configure(text=str(min_val + 1))  # Update the label to the only available slice
            self.slice_slider.configure(from_=min_val, to=max_val)
            self.slice_slider.configure(state='disabled')  # Disable the slider
        else:
            # Normal case (multiple slices are available)
            previous_slice = self.slice_slider.get()
            self.slice_slider.configure(from_=min_val, to=max_val)
            middle_slice = max_val // 2
            self.slice_slider.configure(state='normal')  # Ensure the slider is enabled
            if self.lock_slice.get() == 0:
                self.slice_slider.set(middle_slice)  # Set to the middle slice
            else:
                if previous_slice > max_val:
                    self.slice_slider.set(max_val)
                elif previous_slice < min_val:
                    self.slice_slider.set(min_val)
                else:
                    self.slice_slider.set(previous_slice)
                
            self.slice_value_label.configure(text=str(middle_slice + 1))  # Update the label

    def init_window_sliders(self):
        print("init_window_sliders")

        std_range = 4

        min_val = np.mean(self.display_img_array) - std_range*np.std(self.display_img_array)
        min_val = max(min_val, np.min(self.display_img_array))

        max_val = np.mean(self.display_img_array) + std_range*np.std(self.display_img_array)
        max_val = min(max_val, np.max(self.display_img_array))

        half_range = (max_val - min_val) / 2
        half_range = max(half_range, 2)

        # Window centre
        self.wc_slider.configure(from_= math.floor(min_val), to=math.ceil(max_val))
        if self.lock_wc.get() == 1:
            if self.wc_slider.get() < min_val:
                self.wc_slider.set(min_val)
            if self.wc_slider.get() > max_val:
                self.wc_slider.set(max_val)
        else:
            self.wc_slider.set(min_val + half_range)
        
        # Window width
        self.ww_slider.configure(from_=1, to=math.ceil(half_range))
        if self.lock_ww.get() == 1:
            if self.ww_slider.get() > half_range:
                self.ww_slider.set(half_range)
        else:
            self.ww_slider.set(half_range)

    def get_selection(self):
        print("get_selection")

        selected_items = self.file_explorer_treeview.selection()  # Get all selected items
        selected_paths = []  # List to store paths of selected items

        for item in selected_items:
            selected = self.file_explorer_treeview.item(item, 'values')[0]  # Assuming the first column has the file name
            new_path = ''
            if selected == "..":
                # Navigate up one directory level
                new_path = os.path.dirname(self.current_path.get())
            else:
                file_type = self.file_explorer_treeview.item(item, 'values')[1]  # Assuming the second column has the file type
                if file_type == 'Directory':
                    # Navigate into selected directory, remove emoji if present
                    new_path = os.path.join(self.current_path.get(), selected.replace("📁 ", ""))  # Remove the folder emoji
                else:
                    new_path = os.path.join(self.current_path.get(), selected)
            
            selected_paths.append(new_path)

        return selected_paths
                
    def view_image(self):
        print("view_image")

        self.view_image_button.configure(text="Loading Image")
        self.view_image_button.configure(state="disabled")  # Disable prevents multi-clicks
        self.update_button_state_appearance()
        self.master.update_idletasks()  # Update the GUI
        self.errors = []

        try:
            self.clear_contours()  # Remove prior contours
            # Reset current view settings
            self.current_plane = None
            self.current_slice_index = None
            self.current_wc = None
            self.current_ww = None
            self.prepare_for_image(reload=False)  # Load new image
        except Exception as e:
            # Store error
            selected = self.get_selection()[0]
            self.store_errors_and_traceback(os.path.join(self.last_valid_path.get(), selected), e)
            self.show_errors_and_traceback()

        self.reset_view_image_button_state()
        self.update_button_state_appearance()

    def render_image(self):
        print("render_image")

        if self.display_img_array is not None:
            if not self.is_updating:
                if self.master != self.original_master:
                    self.master = self.original_master
                self.master.after(0, self.update_canvas) # Move this code to run in the main thread

    def update_canvas(self):
        print("update_canvas")

        self.is_updating = True

        # Determine the slice index based on whether the slider is enabled or disabled
        if self.slice_slider.cget('state') == 'disabled':
            slice_index = 0  # When the slider is disabled, there's only one slice, so index is 0
        else:
            print('self.slice_slider', self.slice_slider.get())
            slice_index = int(self.slice_slider.get())        

        self.ax.clear()
        # Dicom convention
        # L -> x, P -> y, S -> z | Numpy is zyx | Therefore we have, SPL
        if self.plane == 'axial':
            self.original_slice = self.display_img_array[slice_index, :, :]
            aspect_ratio = self.voxel_spacing[1] / self.voxel_spacing[2]
        elif self.plane == 'sagittal':
            slice_idx_reversed = self.display_img_array.shape[2] - slice_index - 1
            self.original_slice = self.display_img_array[:, :, slice_idx_reversed]
            aspect_ratio = self.voxel_spacing[0] / self.voxel_spacing[1]
            self.original_slice = np.flipud(self.original_slice)
        elif self.plane == 'coronal':
            slice_idx_reversed = self.display_img_array.shape[1] - slice_index - 1
            self.original_slice = self.display_img_array[:, slice_idx_reversed, :]
            aspect_ratio = self.voxel_spacing[0] / self.voxel_spacing[2]
            self.original_slice = np.flipud(self.original_slice)
        wc = self.wc_slider.get()
        ww = self.ww_slider.get()
        self.scan_slice = self.normalise_natural(self.original_slice, wc, ww)

        # Set colormap
        if self.input_format.lower() == 'png_or_jpeg':
            path_in = os.path.join(self.current_path.get(), self.get_selection()[0])
            img_bgr = cv2.imread(path_in)
            img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB
            self.ax.imshow(img_rgb)

            # Disable sliders
            self.slice_slider.configure(state='disabled')
            self.wc_slider.configure(state='disabled')
            self.ww_slider.configure(state='disabled')
        else:
            self.ax.imshow(self.scan_slice, cmap=self.color_map.get())  # Display in grayscale

        # Create an annotation object for displaying the pixel value
        self.annot = self.ax.annotate("", xy=(0,0), xytext=(15,-20), textcoords="offset points",
                                    bbox=dict(boxstyle="round", fc="yellow", ec="black", lw=1))
        self.annot.set_visible(False)

        self.ax.axis('off')
        if self.structure_masks != []:
            self.render_structures()  # Pass the aspect ratio to render_structures

        if self.scale_image_view_to_voxels.get() == 1:
            self.ax.set_aspect(aspect_ratio)
            
        self.fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
        self.canvas_image.draw()

        self.is_updating = False

    def on_mouse_move(self, event):
        if event.inaxes == self.ax and self.display_img_array is not None:
            x = event.xdata
            y = event.ydata
            if x is not None and y is not None:
                x = int(x)
                y = int(y)
                # Ensure indices are within bounds
                if 0 <= x < self.original_slice.shape[1] and 0 <= y < self.original_slice.shape[0]:
                    pixel_value = self.original_slice[y, x]
                    self.update_annotation(event, pixel_value)
                else:
                    self.hide_annotation()
            else:
                self.hide_annotation()
        else:
            self.hide_annotation()
        self.canvas_image.draw_idle()

    def update_annotation(self, event, pixel_value):
        # Update the position and text of the annotation
        self.annot.xy = (event.xdata, event.ydata)
        text = f"{pixel_value:.2f}"
        self.annot.set_text(text)
        self.annot.get_bbox_patch().set_alpha(0.8)
        self.annot.set_visible(True)

    def hide_annotation(self):
        if hasattr(self, 'annot'):
            self.annot.set_visible(False)
            
    def render_structures(self):
        print("render_structures")

        # Get current slice index
        if self.slice_slider.cget('state') == 'disabled':
            slice_index = 0
        else:
            slice_index = int(self.slice_slider.get())        

        for i, structure_mask in enumerate(self.structure_masks):
            if i in self.hidden_structure_indices:
                continue

            colour = self.colours_list[i % len(self.colours_list)]
            
            # Extract the appropriate slice based on view orientation
            if self.plane == 'axial':
                structure_mask_slice = structure_mask[slice_index, :, :]
            elif self.plane == 'sagittal':
                slice_idx_reversed = self.display_img_array.shape[2] - slice_index - 1
                structure_mask_slice = structure_mask[:, :, slice_idx_reversed]
                structure_mask_slice = np.flipud(structure_mask_slice)
            elif self.plane == 'coronal':
                slice_idx_reversed = self.display_img_array.shape[1] - slice_index - 1
                structure_mask_slice = structure_mask[:, slice_idx_reversed, :]
                structure_mask_slice = np.flipud(structure_mask_slice)

            # Ensure mask is binary and the right type for contour operations
            structure_mask_slice = (structure_mask_slice > 0.5).astype(np.uint8)
            
            # Skip empty slices
            if not np.any(structure_mask_slice):
                continue

            try:
                if self.contour_outline_switch_val.get():
                    # Use matplotlib's contour with explicit levels
                    self.ax.contour(
                        structure_mask_slice,
                        levels=[0.5],
                        colors=colour,
                        linewidths=self.linewidth_slider.get()
                    )
                if self.contour_fill_switch_val.get():
                    # Use matplotlib's contourf with explicit levels
                    self.ax.contourf(
                        structure_mask_slice,
                        levels=[-0.5, 0.5, 1.5],  # Ensure we capture the full range
                        colors=[None, colour],  # None for below threshold, colour for above
                        alpha=self.opacity_slider.get() / 100
                    )
            except Exception as e:
                print(f"Error rendering structure {i}: {str(e)}")
                continue

    def view_structures(self):
        print("view_structures")

        try:
            self.view_contours_button.configure(text="Loading Contours")
            self.view_contours_button.configure(state="disabled")
            self.update_button_state_appearance()
            self.master.update_idletasks()  # Update the GUI

            new_structure_masks = []
            new_structure_names = []

            # Check if rtss_file
            is_rtss = False
            try:
                ds = pydicom.dcmread(self.get_selection()[0])
                if ds.Modality == 'RTSTRUCT':
                    is_rtss = True
            except:
                pass

            # Load structures from file
            if not os.path.isdir(self.get_selection()[0]) and not is_rtss:
                file_paths = self.get_selection()
                self.last_structure_file_paths = file_paths  # Store for reloading
                for file_path in file_paths:
                    mask = any_to_numpy(file_path, "viewing", self.apply_affine.get())[0]
                    new_structure_masks.append(mask)
                    name = os.path.basename(file_path)
                    new_structure_names.append(name)
            # Load structures from RTSS
            else: 
                new_structure_masks, file_path, new_structure_names, image_array = rtss_to_npy(
                    self.current_image_path, self.slice_info_dict, self.apply_affine.get())
                self.last_structure_file_paths = None  # Indicate RTSS structures

            # Combine existing structures with new ones
            if self.structure_masks:
                self.structure_masks.extend(new_structure_masks)
                self.structure_names.extend(new_structure_names)
            else:
                self.structure_masks = new_structure_masks
                self.structure_names = new_structure_names

            # Binarize structure masks
            self.structure_masks = [(mask >= 0.5).astype(int) for mask in self.structure_masks]

            # Update the structure treeview and render the image
            self.update_structure_treeview(self.structure_names)
            self.render_image()

        except Exception as e:
            print(f"An error occurred: {e}")
            self.view_contours_button.configure(text="View Contours")
            self.view_contours_button.configure(state="normal")
            self.update_button_state_appearance()

        finally:
            self.reset_view_structures_button_state()

    def clear_contours(self):
        print("clear_contours")

        self.structure_masks = []
        self.structure_names = []
        self.hidden_structure_indices = []  # Clear hidden indices

        # Clear the Treeview, including the color boxes
        for item in self.structure_tree.get_children():
            self.structure_tree.delete(item)

        # Destroy all checkbuttons
        for checkbutton, _ in self.structure_checkbuttons:
            checkbutton.destroy()

        # Clear the list of checkbuttons and color boxes
        self.structure_checkbuttons.clear()
        for canvas in self.color_boxes:
            canvas.destroy()

        self.color_boxes.clear()

        self.render_image()

    def normalise_natural(self, image, wc, ww):
        """Normalize image intensities for display."""
        print("normalise_natural")

        # Handle any NaN or infinite values in the original image.
        finite_mask = np.isfinite(image)
        max_finite = np.max(image[finite_mask])
        min_finite = np.min(image[finite_mask])
        image = np.nan_to_num(image, nan=0.0, posinf=max_finite, neginf=min_finite)

        # Check if the image is binary.
        unique_values = np.unique(image)
        if np.array_equal(unique_values, [0, 1]):
            return (image * 255).astype(np.uint8)  # When binary, map 0s to black and 1s to white.

        # Calculate the min and max intensity values based on wc and ww.
        min_intensity = wc - (ww / 2)
        max_intensity = wc + (ww / 2)

        # Clip the image to the specified window and normalize.
        windowed_img = np.clip(image, min_intensity, max_intensity)
        range_intensity = max_intensity - min_intensity
        if range_intensity == 0:
            range_intensity = 1  # Prevent division by zero

        image_normalised = 255 * (windowed_img - min_intensity) / range_intensity

        # Ensure no NaN or infinite values remain after normalization
        return np.nan_to_num(image_normalised, nan=0.0, posinf=255.0, neginf=0.0).astype(np.uint8)
        
    def show_pixel_value(self, event):
        if self.display_img_array is None:
            return

        # Convert display coordinates to data coordinates considering transformations
        image_x, image_y = (event.x, event.y)
        data_coords = self.ax.transData.inverted().transform((image_x, image_y))
        image_x = int(round(data_coords[0]))
        image_y = int(self.scan_slice.shape[1] - round(data_coords[1]))

        # Ensure coordinates are within image boundaries
        try:
            pixel_value = self.scan_slice[image_y, image_x]
            formatted_value = "{:.2f}".format(pixel_value)
            self.update_pixel_display(event.x, event.y, formatted_value)
        except:
            self.hide_pixel_value_label(event)

    def swap_view(self, new_view):
        print("swap_view")
        # Store current window center and width values
        current_wc = self.wc_slider.get()
        current_ww = self.ww_slider.get()

        # Reset all buttons to normal state
        for button in self.view_buttons:
            button.configure(state="normal")

        # Set the selected button to the pressed state and update the view
        if new_view == "axial":
            self.plane = 'axial'
            self.current_plane = 'axial'
            self.axial_button.configure(state="disabled")
        elif new_view == "sagittal":
            self.plane = 'sagittal'
            self.current_plane = 'sagittal'
            self.sagittal_button.configure(state="disabled")
        elif new_view == "coronal":
            self.plane = 'coronal'
            self.current_plane = 'coronal'
            self.coronal_button.configure(state="disabled")

        self.update_button_state_appearance()

        # Re-initialize the sliders
        self.init_sliders()

        # Reapply the stored window center and width values
        self.wc_slider.set(current_wc)
        self.ww_slider.set(current_ww)
        self.update_wc_label(None)
        self.update_ww_label(None)

        # Reapply the stored slice index if the slice lock is on
        if self.lock_slice.get() == 1 and self.current_slice_index is not None:
            max_slice = int(self.slice_slider.cget("to"))
            if 0 <= self.current_slice_index <= max_slice:
                self.slice_slider.set(self.current_slice_index)
            else:
                self.current_slice_index = None  # Reset if out of range
        else:
            # Set to middle slice if lock is off
            max_slice = int(self.slice_slider.cget("to"))
            middle_slice = max_slice // 2
            self.slice_slider.set(middle_slice)

        # Render the image with the new view and applied values
        self.render_image()


    def apply_slice_change_label(self, event):
        # Determine the slice index based on whether the slider is enabled or disabled
        if self.slice_slider.cget('state') == 'disabled':
            slice_index = 0  # When the slider is disabled, there's only one slice, so index is 0
        else:
            slice_index = int(self.slice_slider.get())    

        self.slice_value_label.configure(text=str(slice_index + 1))
        if event is not None or self.display_img_array is not None:
            self.render_image()

    def update_wc_label(self, event):
        self.wc_value_label.configure(text=f"{self.wc_slider.get():.2f}")
        if event is not None:
            self.render_image()

    def update_ww_label(self, event):
        self.ww_value_label.configure(text=f"{self.ww_slider.get():.2f}")
        if event is not None:
            self.render_image()

    def adjust_slice_slider(self, event):
        
        if self.slice_slider.cget('state') == 'normal' and self.last_interaction != 'treeview':
            current_value = int(self.slice_slider.get())
            max_value = int(self.slice_slider.cget("to"))
            min_value = int(self.slice_slider.cget("from_"))

            # Keyboard events
            if event.keysym == 'Right':
                new_value = min(current_value + 1, max_value)
            elif event.keysym == 'Left':
                new_value = max(current_value - 1, min_value)
            # Mouse wheel events for Windows and macOS
            elif sys.platform in self.windows_platforms or sys.platform in self.mac_platforms:
                if event.delta > 0:  # Scrolling up
                    new_value = max(current_value + 1, min_value)
                elif event.delta < 0:  # Scrolling down
                    new_value = min(current_value - 1, max_value)
            # Mouse wheel events for Linux
            elif sys.platform in self.linux_platforms:
                if event.num == 4:  # Scroll up
                    new_value = max(current_value + 1, min_value)
                elif event.num == 5:  # Scroll down
                    new_value = min(current_value - 1, max_value)
            else:
                return

            self.slice_slider.set(int(new_value))
            self.apply_slice_change_label(None)

    def set_input_path(self):
        print("set_input_path")

        selected = self.get_selection()[0]
        path = os.path.join(self.last_valid_path.get(), selected)
        self.path_in.set(path)

    def set_output_path(self):
        print("set_output_path")

        try:
            selected_path = self.last_valid_path.get() # Current path

            # Check if selected is a directory or file
            if os.path.isdir(selected_path):
                path = selected_path    
            else:
                path = os.path.dirname(selected_path)

        except:
            path = self.last_valid_path.get()

        self.out_dir.set(path)

    def enter_key(self, event):  
        """Not currently in use"""
        selected_items = self.file_explorer_treeview.selection()
        if selected_items:
            item = selected_items[0]  # Get the first selected item
            selected = self.get_selection()[0]
            new_path = os.path.join(self.current_path.get(), selected)
            
            if os.path.isdir(new_path):
                self.current_path.set(new_path)
                self.load_files(self.current_path.get())
            else:
                self.prepare_for_image()  # Assuming this handles file opening
        else:
            print("No item selected")

    def delete_file_or_folder(self, event):
        print("delete_file_or_folder")

        if self.last_interaction != 'treeview':  
            return
        else:
            self.last_interaction = 'treeview'

        selected_items = self.file_explorer_treeview.selection()
        if selected_items:
            selected = self.get_selection()[0]
            path_to_delete = os.path.join(self.current_path.get(), selected)
            
            # Ask for confirmation before deleting
            confirm = self.custom_askyesno("Confirm Delete", f"Are you sure you want to delete '{selected}'?")
            if confirm:
                if os.path.isdir(path_to_delete):
                    shutil.rmtree(path_to_delete)  # Remove the directory and all its contents
                else:
                    os.remove(path_to_delete)  # Remove the file
                
                # After deletion, refresh the displayed files
                self.load_files(self.current_path.get())
        else:
            # Optionally handle no selection case
            print("No item selected to delete")

    def custom_askyesno(self, title, message):
        # Create a new Toplevel window
        confirm_window = CTkToplevel(self.master)
        confirm_window.title(title)
        
        # Set the size and center the window
        confirm_window.geometry("400x120")
        confirm_window.grab_set()  # Make the window modal

        centre_window(confirm_window, (400, 140))

        # Create and place the message label
        label = CTkLabel(confirm_window, text=message, wraplength=250)
        label.pack(pady=15)

        # Create a frame to hold the buttons
        button_frame = CTkFrame(confirm_window)
        button_frame.pack(pady=0)

        # Variable to store the user's response
        response = StringVar()

        # Define button callbacks
        def on_yes():
            response.set("yes")
            confirm_window.destroy()

        def on_no():
            response.set("no")
            confirm_window.destroy()

        # Create Yes and No buttons
        yes_button = CTkButton(button_frame, text="Yes", command=on_yes)
        yes_button.grid(row=0, column=0, padx=self.button_padx, pady=self.button_pady)

        no_button = CTkButton(button_frame, text="No", command=on_no)
        no_button.grid(row=0, column=1, padx=self.button_padx, pady=self.button_pady)

        # Wait for the window to close
        confirm_window.wait_window()

        # Return True if the user clicked Yes, otherwise False
        return response.get() == "yes"

    def backspace_key(self, event):
        """Not currently in use"""
        print("Backspace key pressed")
        if self.last_interaction == 'treeview':  # Ensure this is contextually correct
            new_path = os.path.dirname(self.current_path.get())
            if new_path != self.current_path.get():  # Prevent navigating up from root
                self.current_path.set(new_path)
                self.load_files(new_path)

    def select_all(self, event):
        self.path_entry.select_range(0, tk.END)
        return "break"

    def copy_to_clipboard(self, event):
        self.master.clipboard_clear()
        self.master.clipboard_append(self.path_entry.get())
        self.master.update()
        return "break"

    def paste_from_clipboard(self, event):
        clipboard_content = self.master.clipboard_get()
        self.path_entry.delete(0, tk.END)
        self.path_entry.insert(0, clipboard_content)
        return "break"

    def check_ready_to_convert(self):

        # Paths
        path_in = self.input_path_entry.get()
        out_dir = self.output_path_entry.get()
        out_dir = os.path.join(out_dir, 'Conversions')
        output_format = self.output_format_combobox.get()

        # Check input path is non empty
        if path_in == '':
            messagebox.showerror("Error", "Input path is empty")
            return False

        # Check output path is non empty
        if out_dir == '':
            messagebox.showerror("Error", "Output path is empty")
            return False

        # Check an output format is selected
        if output_format == '':
            messagebox.showerror("Error", "Output format is not selected")
            return False

        return True

    def start_image_conversion(self):
        print("start_image_conversion")
        self.convert_button.configure(text="Initialising")
        self.convert_button.configure(state="disabled") # Disable prevents multi-clicks
        self.update_button_state_appearance()

        ready = self.check_ready_to_convert()
        if not ready:
            self.convert_button.configure(text="Convert")
            self.convert_button.configure(state="normal")
            self.update_button_state_appearance()
            return

        # Paths
        out_dir = self.output_path_entry.get()
        out_dir = os.path.join(out_dir, 'Conversions')
        path_in = self.input_path_entry.get()

        # Delete output (Conversions) folder if it exists
        try:
            # If the output directory exists, clear its contents
            if os.path.exists(out_dir):
                # Get list of items in the directory
                for item in os.listdir(out_dir):
                    item_path = os.path.join(out_dir, item)
                    try:
                        if os.path.isfile(item_path):
                            os.unlink(item_path)
                        elif os.path.isdir(item_path):
                            shutil.rmtree(item_path)
                    except Exception as e:
                        print(f"Error removing {item_path}: {e}")
            else:
                # Create new output directory if it doesn't exist
                os.makedirs(out_dir)

        except Exception as e:
            self.convert_button.configure(text="Convert")
            self.convert_button.configure(state="normal")
            self.update_button_state_appearance()
            return

        # Start the conversion in a new thread
        conversion_thread = threading.Thread(target=self.image_conversion_thread)
        conversion_thread.start()

    def image_conversion_thread(self):
        print("image_conversion_thread")
        self.errors = []
        convert_num = self.count_items_to_convert()
        self.update_progress(0, convert_num)

        # Paths and format settings
        path_in, out_dir, output_format, interpolation_type = self.initialize_conversion_settings()
        
        # Handle single file or directory
        has_dicom, rtss_file_names, contains_image = contains_dicom(path_in)
        if not os.path.isdir(path_in) or has_dicom:
            self.convert_single_image(path_in, out_dir, output_format, interpolation_type, rtss_file_names)
            self.update_progress(1, 1)
        else:
            # Batch convert all files in directory
            self.convert_multiple_images(path_in, out_dir, output_format, interpolation_type, convert_num)
        
        # Finalize and reset UI elements
        self.finalize_conversion()

    def count_items_to_convert(self):
        # Paths
        path_in = self.input_path_entry.get()

        count = 0

        # Check if the input path is a file
        if not os.path.isdir(path_in):
            count = 1  # Only one item to convert
        else:
            for dirpath, dirnames, filenames in os.walk(path_in):

                has_dicom, rtss_file_names, contains_image = contains_dicom(dirpath)

                # Count current path if contains DICOM images
                if contains_image:
                    count += 1
                
                # Count RTSS files in dirpath
                num_rtss_files = len(rtss_file_names)
                if num_rtss_files > 0:
                    count += num_rtss_files

                # Count files in dirpath when not DICOMs
                for file in filenames:
                    file_path = os.path.join(dirpath, file)

                    try:
                        ds = pydicom.dcmread(file_path, stop_before_pixels=True)
                    except:
                        count += 1                    

        return count

    def initialize_conversion_settings(self):
        path_in = self.input_path_entry.get()
        out_dir = os.path.join(self.output_path_entry.get(), 'Conversions')
        interpolation_type = self.interpolation_type_combobox.get() if self.enable_resample_shape.get() == 1 or self.enable_resample_voxel.get() == 1 else 'Linear'
        output_format = self.output_format_combobox.get()
        return path_in, out_dir, output_format, interpolation_type

    def convert_single_image(self, path_in, out_dir, output_format, interpolation_type, rtss_file_names):
        print('convert_single_image')

        # Convert single file or dicom image directory
        try:
            self.to_imageconverter(path_in, out_dir, output_format, interpolation_type)
        except Exception as e:
            self.log_error(f"Error converting {path_in}: {e}")

        # Convert any rtss files in the directory
        for rtss_file_name in rtss_file_names:
            try:
                rtss_file_path = os.path.join(path_in, rtss_file_name)
                self.to_imageconverter(rtss_file_path, out_dir, output_format, interpolation_type)
            except Exception as e:
                self.log_error(f"Error converting {rtss_file_path}: {e}")
        
        self.load_files(self.current_path.get())

    def convert_multiple_images(self, path_in, out_dir, output_format, interpolation_type, convert_num):
        print('convert_multiple_images')
        converted_num = 0

        for current_dir, dirs, files in os.walk(path_in):
            if 'Conversions' in dirs:
                dirs.remove('Conversions')

            # First, convert dicom folders in current_dir
            converted_num = self.convert_dicom_folders(
                current_dir, dirs, path_in, out_dir, output_format, interpolation_type, convert_num, converted_num
            )

            # Convert single image files to non-dicom in current_dir
            if output_format.lower() != 'dicom':
                for file_name in files:
                    input_file_path = os.path.join(current_dir, file_name)
                    relative_path = os.path.relpath(input_file_path, path_in)
                    out_directory = os.path.join(out_dir, os.path.split(relative_path)[0])
                    
                    # Use convert_single_image for single file conversion
                    self.convert_single_image(
                        input_file_path,
                        out_directory,
                        output_format,
                        interpolation_type,
                        []
                    )

            # If converting to dicom check for masks to convert to rtss
            elif output_format.lower() == 'dicom':

                # Find masks in current_dir
                mask_file_paths = {} # Name and shape
                for file_name in files:
                    input_file_path = os.path.join(current_dir, file_name)

                    # Find any masks in current_dir (boolean or binary voxels)
                    img_arr, _, _, _, _, _, _, _ = any_to_numpy(input_file_path, "viewing", False)

                    # Check whether contains only 0s and 1s or is boolean
                    if np.unique(img_arr).shape[0] == 2:
                        mask_file_paths[input_file_path] = img_arr.shape
                    elif np.min(img_arr) >= 0 and np.max(img_arr) <= 1:
                        mask_file_paths[input_file_path] = img_arr.shape

                # Find non-masks in current_dir
                image_file_paths = {} # Name and shape
                for file_name in files:
                    input_file_path = os.path.join(current_dir, file_name)

                    # Find any masks in current_dir (boolean or binary voxels)
                    img_arr, _, _, _, _, _, _, _ = any_to_numpy(input_file_path, "viewing", False)

                    # Check whether contains only 0s and 1s or is boolean, or is between 0 and 1
                    if np.unique(img_arr).shape[0] != 2 and np.min(img_arr) <= 0 and np.max(img_arr) >= 1:
                        image_file_paths[input_file_path] = img_arr.shape
                if len(image_file_paths) == 0:
                    self.log_error(f'No images found in \n{current_dir}')
                    if len(mask_file_paths) != 0:
                        self.log_error(f'No masks found in \n{current_dir}')
                    continue

                # Convert each non-mask to a dicom image series
                for file_path in image_file_paths.keys():
                    print('file path', file_path)
                    relative_path = os.path.relpath(file_path, path_in)
                    print('relative_path', relative_path)
                    image_out_dir = os.path.join(out_dir, os.path.split(relative_path)[0])
                    print('image_out_dir', image_out_dir)
                    
                    # Use convert_single_image for single file conversion
                    self.convert_single_image(
                        file_path,
                        image_out_dir,
                        output_format,
                        interpolation_type,
                        []
                    )

                    dicom_image_series_path = os.path.join(image_out_dir, os.path.split(relative_path)[1].split('.')[0])

                # Create RTSTRUCT file
                self.create_rtstruct(dicom_image_series_path, mask_file_paths)

    def zyx_to_xyz(self, array):
        mask = np.transpose(array, (2, 1, 0))
        mask = np.rot90(mask, k=1, axes=(0, 1))
        mask = np.flip(mask, axis=0)
        return mask

    def create_rtstruct(self, dicom_series_path, mask_file_paths):
        print('create_rtstruct')

        # Load the masks
        masks = {}
        for mask_path in mask_file_paths:
            mask = sitk.ReadImage(mask_path)
            mask = sitk.GetArrayFromImage(mask)
            mask = self.zyx_to_xyz(mask)
            mask[mask > 0.5] = 1
            mask[mask <= 0.5] = 0
            mask = mask.astype(bool)
            masks[mask_path] = mask

        # Separate structures in masks
        masks_processed = {}
        for mask_path, mask in masks.items():
            # Use structure element that includes diagonal connections
            structure = ndimage.generate_binary_structure(3, 3)  # 3D, full connectivity
            labeled_array, num_features = ndimage.label(mask, structure=structure)
            
            # Separate structures in masks
            count = 1
            for i in range(1, num_features + 1):
                mask = (labeled_array == i)  # Extract the i-th volume mask
                mask = mask.astype(bool)  # Ensure the mask is boolean type

                print(f'Component {i} has {np.sum(mask)} voxels and count is {count}')
                if np.sum(mask) < 3: # Must be at least 3 voxels
                    continue
                mask_name = os.path.split(mask_path)[1].split('.')[0] + f"_{count}" + f"_{np.sum(mask)}"
                masks_processed[mask_name] = mask
                print('SUM', np.sum(mask), mask_name)
                count += 1

        # Create rtstruct
        rtstruct = RTStructBuilder.create_new(dicom_series_path=dicom_series_path)
        for mask_name, mask in masks_processed.items():
            # Define a list of valid ROI colors that work with rt_utils
            valid_roi_colors = [
                [255, 0, 0],    # Red
                [0, 0, 255],    # Blue
                [0, 255, 255],  # Cyan
                [255, 0, 255],  # Magenta
                [255, 255, 0],  # Yellow
                [255, 128, 0],  # Orange
                [0, 255, 128],  # Spring green
                [128, 0, 255],  # Purple
                [255, 128, 128] # Pink
            ]
            
            # Select a random color from the valid colors
            random_color = random.choice(valid_roi_colors)
            
            try:
                rtstruct.add_roi(
                    mask=mask, 
                    color=random_color,  # Use the color as a list
                    name=mask_name
                )
            except Exception as e:
                print(f"Error adding ROI {mask_name}: {str(e)}")
                continue

        # Save the RTStruct to the predictions folder
        rtstruct_save_path = os.path.join(dicom_series_path, "rt-struct.dcm")
        rtstruct.save(rtstruct_save_path)

    def convert_dicom_folders(self, current_dir, dirs, path_in, out_dir, output_format, interpolation_type, convert_num, converted_num):
        dirs_copy = dirs.copy()
        for dir_name in dirs_copy:
            input_dir_path = os.path.join(current_dir, dir_name)
            output_dir_path = os.path.join(out_dir, os.path.relpath(input_dir_path, path_in))
            os.mkdir(output_dir_path)

            has_dicom, rtss_file_names, contains_image = contains_dicom(input_dir_path)
            if has_dicom:
                dirs.remove(dir_name)
                if contains_image:
                    try:
                        self.to_imageconverter(input_dir_path, output_dir_path, output_format, interpolation_type)
                    except Exception as e:
                        self.log_error((input_dir_path, str(e)))
                    converted_num += 1
                    self.update_progress(converted_num, convert_num)
                    self.load_files(self.current_path.get())
                # Convert rtss files in dicom folder
                for rtss_file_name in rtss_file_names:
                    try:
                        rtss_file_path = os.path.join(input_dir_path, rtss_file_name)
                        self.to_imageconverter(rtss_file_path, output_dir_path, output_format, interpolation_type)
                    except Exception as e:
                        self.log_error((rtss_file_path, str(e)))
                    converted_num += 1
                    self.update_progress(converted_num, convert_num)
                    self.load_files(self.current_path.get())
        return converted_num

    def log_error(self, error_detail):
        self.errors.append(error_detail)

    def finalize_conversion(self):
        if self.master != self.original_master:
            self.master = self.original_master
        self.show_errors_and_traceback()
        self.reset_convert_button_state()

    def update_progress(self, num_counted, total_files):
        print("update_progress")
        # Calculate the progress as a value between 0 and 100
        progress = num_counted / total_files
        progress_percent = progress * 100
        print('num_counted', num_counted, 'total_files', total_files, 'progress_percent', progress_percent)
        self.convert_button.configure(text=f"Converting ({progress_percent:.2f}%)")
        self.master.update_idletasks()
        
    def to_imageconverter(self, path_in, out_dir, output_format, interpolation_type):
        print("to_imageconverter")

        try:
            content_name = os.path.split(path_in)[1].split('.')[0]
            path_out = os.path.join(out_dir, content_name)
            perform_resample = False
            resample_shape = None
            resample_voxels = None
            perform_crop = False
            crop_shape = None

            if self.enable_resample_shape.get() == 1:
                perform_resample = 'Shape'
                resample_shape = self.resample_shape_entry.get()
                resample_shape = list(resample_shape.strip().split(','))
                resample_shape = list(map(int, resample_shape))

            elif self.enable_resample_voxel.get() == 1:
                perform_resample = 'Voxels'
                resample_voxels = self.resample_voxel_entry.get()
                resample_voxels = list(resample_voxels.strip().split(','))
                resample_voxels = list(map(float, resample_voxels))

            if self.enable_crop.get() == 1:
                perform_crop = True
                crop_shape = self.crop_entry.get()
                crop_shape = list(crop_shape.strip().split(','))
                crop_shape = list(map(int, crop_shape))
                crop_shape = tuple(crop_shape)

            converter = ImageConverter(path_in, path_out, output_format, perform_resample, resample_shape, resample_voxels, interpolation_type, perform_crop, crop_shape, self.lps_convert_switch.get())

            converter.convert()
        except Exception as e:
            self.store_errors_and_traceback(path_in, e)

    def store_errors_and_traceback(self, path_in, exception):
        print("store_errors_and_traceback")
        # Get the last exception's traceback details
        tb = traceback.format_exc()

        # Record the error with the traceback including the line number
        self.errors.append(f'Failed to convert:\n {path_in}:\n\n {exception}\n\nTraceback:\n{tb} \n\n')

    def show_errors_and_traceback(self):
        print("show_errors_and_traceback")

        # Function to get the error string based on the state
        def get_error_str():
            if self.show_traceback:
                return ''.join(self.errors)  # Show full errors with traceback
            else:
                return ''.join([error.split('Traceback:')[0] + '\n' for error in self.errors])  # Hide traceback

        # Get the initial error string
        errors_str = get_error_str()

        # Background color setting
        bg_color = '#D3D3D3'

        error_window = CTkToplevel()
        error_window.title("Console Output")
        error_window.configure(bg=bg_color)  # Set the background color for the window
        error_window.withdraw()

        # Configure the grid layout for the error window
        error_window.columnconfigure(0, weight=1)
        error_window.rowconfigure(0, weight=1)
        error_window.rowconfigure(1, weight=0)

        # Frame to hold the Text widget and Scrollbar
        text_frame = CTkFrame(error_window)
        text_frame.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)

        # Configure grid for text_frame
        text_frame.columnconfigure(0, weight=1)
        text_frame.rowconfigure(0, weight=1)

        # Create a Text widget and a Scrollbar with the same background color
        text_widget = CTkTextbox(text_frame, wrap="word")
        text_widget.grid(row=0, column=0, sticky="nsew")

        scrollbar = CTkScrollbar(text_frame, command=text_widget.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")

        text_widget.configure(yscrollcommand=scrollbar.set)

        # Insert all the errors initially
        text_widget.insert('end', errors_str)
        text_widget.configure(state="disabled")

        # Create a separate frame for the close and toggle traceback buttons
        button_frame = CTkFrame(error_window)
        button_frame.grid(row=1, column=0, sticky="ew", padx=0, pady=(0, 0))

        # Configure grid for button_frame
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)

        # Function to toggle traceback visibility
        def toggle_traceback():
            self.show_traceback = not self.show_traceback

            # Update the text content in the text widget
            text_widget.configure(state="normal")
            text_widget.delete(1.0, 'end')
            text_widget.insert('end', get_error_str())
            text_widget.configure(state="disabled")

            error_window.destroy()
            self.show_errors_and_traceback()

        # Toggle button for showing/hiding tracebacks
        toggle_button = CTkButton(button_frame, text="Show Traceback", command=toggle_traceback)
        toggle_button.configure(text="Hide Traceback" if self.show_traceback else "Show Traceback")
        toggle_button.grid(row=0, column=0, sticky="e", padx=self.button_padx, pady=self.button_pady)

        # Close button
        close_button = CTkButton(button_frame, text="Close", command=error_window.destroy)
        close_button.grid(row=0, column=1, sticky="w", padx=self.button_padx, pady=self.button_pady)

        centre_window(error_window, (600, 400))
        error_window.deiconify()

        # self.errors = []

    def reset_convert_button_state(self):
        print("reset_convert_button_state")
        self.convert_button.configure(text="Convert")
        self.convert_button.configure(state="normal")
        self.update_button_state_appearance()
        
        self.load_files(self.current_path.get()) # Reload files

    def reset_view_structures_button_state(self):
        print("reset_view_structures_button_state")
        self.view_contours_button.configure(text="View Contours")
        self.view_contours_button.configure(state="normal") 
        self.update_button_state_appearance()        

    def reset_view_image_button_state(self):
        print("reset_view_images_button_state")
        self.view_image_button.configure(text="View Image")
        self.view_image_button.configure(state="normal")
        self.update_button_state_appearance()

    def update_resample_shape_entry(self):
        print("update_resample_shape_entry")
        if self.display_img_array is not None:
            # Temporarily enable the entry for update
            self.resample_shape_entry.configure(state='normal')
            
            shape_str = str(self.original_shape)[1:-1]

            self.resample_shape_entry.delete(0, tk.END)
            self.resample_shape_entry.insert(0, shape_str)
            
            # Re-apply the intended state based on the checkbox
            if self.enable_resample_shape.get() == 1:
                self.resample_shape_entry.configure(state='normal')
            else:
                self.resample_shape_entry.configure(state='readonly')

    def update_resample_voxel_entry(self):
        print("update_resample_voxel_entry")
        if self.display_img_array is not None:
            # Temporarily enable the entry for update
            self.resample_voxel_entry.configure(state='normal')
            
            # Round each voxel spacing value and format to two decimal places
            # try:
            voxels_str = str(tuple([f"{round(x, 2):.2f}" for x in self.voxel_spacing]))[1:-1]
            voxels_str = voxels_str.replace("'", "")
            # except:
            #     voxels_str = "1.00, 1.00, 1.00"

            self.resample_voxel_entry.delete(0, tk.END)
            self.resample_voxel_entry.insert(0, voxels_str)

            # Re-apply the intended state based on the checkbox
            if self.enable_resample_voxel.get() == 1:
                self.resample_voxel_entry.configure(state='normal')
            else:
                self.resample_voxel_entry.configure(state='readonly')

    def update_crop_entry(self):
        print("update_crop_entry")
        if self.display_img_array is not None:
            # Temporarily enable the entry for update
            self.crop_entry.configure(state='normal')

            # Round each voxel spacing value and format to two decimal places
            crop_str = str(self.display_img_array.shape)[1:-1]
            crop_str = crop_str.replace("'", "")

            self.crop_entry.delete(0, tk.END)
            self.crop_entry.insert(0, crop_str)

            # Re-apply the intended state based on the checkbox
            if self.enable_crop.get() == 1:
                self.crop_entry.configure(state='normal')
            else:
                self.crop_entry.configure(state='readonly')

def main(folder_path=None):
    root = CTk()
    root.title(f"Viewdoo - {version}")

    # Set theme and appearance mode
    set_appearance_mode("light")
    if hasattr(sys, '_MEIPASS'):
        theme_path = os.path.join(sys._MEIPASS, 'user_themes/Blue.json')
    else:
        theme_path = 'user_themes/Blue.json'
    set_default_color_theme(theme_path)

    app = App(root)
    if folder_path:
        app.current_path.set(folder_path)  # Open the specified folder path
        app.load_files(folder_path)  # Load files in the given folder

    root.geometry("1300x750")
    centre_window(root, (1300, 750))
    root.mainloop()

if __name__ == "__main__":
    main()
# %%