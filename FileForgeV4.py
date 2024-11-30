import os
import io
import magic
import ctypes
import random
import zipfile
import datetime
import tkinter as tk
from PIL import Image
from tkinter import ttk
from docx import Document
from ctypes import wintypes
from tkcalendar import Calendar
from tkinter import filedialog, messagebox 


# Constants and structures for Windows SetFileTime
FILE_ATTRIBUTE_NORMAL = 0x80
GENERIC_WRITE = 0x40000000
OPEN_EXISTING = 3

# Define FILETIME structure to handle file times
class FILETIME(ctypes.Structure):
    _fields_ = [("dwLowDateTime", wintypes.DWORD),
                ("dwHighDateTime", wintypes.DWORD)]

# Load kernel32.dll (Windows system library) to work with file times
kernel32 = ctypes.windll.kernel32

# Define function prototypes for interacting with file times in Windows
CreateFileW = kernel32.CreateFileW
CreateFileW.argtypes = [wintypes.LPCWSTR, wintypes.DWORD, wintypes.DWORD, wintypes.LPVOID,
                        wintypes.DWORD, wintypes.DWORD, wintypes.HANDLE]
CreateFileW.restype = wintypes.HANDLE

SetFileTime = kernel32.SetFileTime
SetFileTime.argtypes = [wintypes.HANDLE, ctypes.POINTER(FILETIME), ctypes.POINTER(FILETIME), ctypes.POINTER(FILETIME)]
SetFileTime.restype = wintypes.BOOL

class TimestomperApp:
    def __init__(self, root):
        self.root = root   # The main window of the application
        self.root.title("FileForge")  # Set the window title
        self.root.geometry("650x700")  # Set the window size

        root.configure(bg='#333333')  # Set a dark background color for the window

        # Title label in the main window
        label = tk.Label(root, text="Welcome to FileForge!", bg='#333333', fg='white', font=("Arial", 20, "bold"))
        label.pack(padx=10, pady=10) 

        # Separate file path variables for each tab
        self.file_path_tab1 = None
        self.file_path_tab2 = None
        self.file_path_tab3 = None

        # Suggested timestamp for tab2
        self.suggested_timestamp_tab2 = None

        # Create a notebook (tabs)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=20, pady=20)

        # Add tabs to the notebook
        self.tab1 = ttk.Frame(self.notebook, width=300, height=200, relief="solid", borderwidth=1)
        self.tab2 = ttk.Frame(self.notebook, width=300, height=200, relief="solid", borderwidth=1)
        self.tab3 = ttk.Frame(self.notebook, width=300, height=200, relief="solid", borderwidth=1)

        # Add the tabs with their titles
        self.notebook.add(self.tab1, text=" Scrambler ")
        self.notebook.add(self.tab2, text=" Timestamp Update ")
        self.notebook.add(self.tab3, text=" Decoy Generator ")

        # Change the appearance of the tab buttons to be equally wide
        style = ttk.Style()

        # Define a new style for the tabs to make the buttons share the width equally
        style.configure("TNotebook.Tab", width=50, anchor="center", font=("Arial", 12, "bold"))  # Make tabs equally wide
        style.configure("TNotebook", padding=5)  # Add padding around tabs

        # Initialize widgets for each tab
        self.create_tab1_widgets()
        self.create_tab2_widgets()
        self.create_tab3_widgets()
    
    def create_tab1_widgets(self):
        """Tab 1 - File Scrambler""" 
        self.tab1_label = tk.Label(self.tab1, text="This is the File Scrambler")
        self.tab1_label.grid(pady=10)

        # File Selection Button for Tab 1
        self.tab1_select_file_button = tk.Button(self.tab1, text="Select File", command=self.select_file_tab1)
        self.tab1_select_file_button.grid(pady=10)

        # Display File Path and Type
        self.file_path_label = tk.Label(self.tab1, text="File Path: None")
        self.file_path_label.grid()
        self.file_type_label = tk.Label(self.tab1, text="File Type: Unknown")
        self.file_type_label.grid()

        # Scramble Button
        self.scramble_button = tk.Button(self.tab1, text="Scramble File", command=self.scramble_file, state=tk.DISABLED)
        self.scramble_button.grid(pady=10)
    
    #File type checking
    def scramble_file(self):
        if "text" in self.file_type:
            self.scramble_text_file()
        elif "image" in self.file_type:
            self.scramble_image_file()
        elif "application" in self.file_type and "exe" in self.file_type:
            self.scramble_executable_file()
        elif "application" in self.file_type and "vnd.openxmlformats-officedocument.wordprocessingml.document" in self.file_type: 
            self.scramble_docx_file()
        elif "video" in self.file_type:
            self.scramble_mp4_file()
        elif "application" in self.file_type and ("ppt" in self.file_path_tab1 or "powerpoint" in self.file_type):
            self.scramble_ppt_file()
        else:
            messagebox.showinfo("Unsupported File", "This file type is not supported for scrambling.")
            return        
        self.save_button.config(state=tk.NORMAL)  # Enable save button after scrambling

    def scramble_text_file(self):
        try:
            # Define the scrambled file path
            scrambled_path = f"{os.path.splitext(self.file_path_tab1)[0]}_scrambled.txt"
            
            # Open the input and output files
            with open(self.file_path_tab1, 'r', encoding='utf-8') as infile, open(scrambled_path, 'w', encoding='utf-8') as outfile:
                # Process the file line by line
                for line in infile:
                    # Scramble content by shifting character codes
                    scrambled_line = ''.join([chr((ord(char) + 5) % 256) for char in line])
                    outfile.write(scrambled_line)
            
            messagebox.showinfo("Success", f"Text file scrambled and saved as {scrambled_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to scramble text file: {e}")

    def scramble_image_file(self):
        try:
            # Define the scrambled file path
            scrambled_path = f"{os.path.splitext(self.file_path_tab1)[0]}_scrambled.png"
            
            # Open the image and apply a basic scrambling
            with Image.open(self.file_path_tab1) as img:
                # Convert image to RGB if not already
                img = img.convert("RGB")
                
                # Apply pixel shuffling to make the image appear scrambled
                pixels = list(img.getdata())
                random.shuffle(pixels)  # Shuffle the pixel data
                
                # Create a new image and put the shuffled data back
                scrambled_img = Image.new(img.mode, img.size)
                scrambled_img.putdata(pixels)
                
                # Save the scrambled image to disk
                scrambled_img.save(scrambled_path, format="PNG")
                
                messagebox.showinfo("Success", f"Image file scrambled and saved as {scrambled_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to scramble image file: {e}")

    def scramble_executable_file(self):
        try:
            # Define the scrambled file path
            scrambled_path = f"{os.path.splitext(self.file_path_tab1)[0]}_scrambled.exe"

            # Open the input file in binary read mode and output file in binary write mode
            with open(self.file_path_tab1, 'rb') as infile, open(scrambled_path, 'wb') as outfile:
                # Process the file in chunks to handle large files
                chunk_size = 4096  # Process 4 KB at a time
                while chunk := infile.read(chunk_size):
                    # Scramble each byte by flipping it (XOR with 0xFF)
                    scrambled_chunk = bytearray([byte ^ 0xFF for byte in chunk])
                    outfile.write(scrambled_chunk)

            # Notify user of success
            messagebox.showinfo("Success", f"Executable file scrambled and saved as {scrambled_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to scramble executable file: {e}")

    def scramble_docx_file(self): 
        try: 
            # Define the scrambled file path
            scrambled_path = f"{os.path.splitext(self.file_path_tab1)[0]}_scrambled.docx"

            # Open the DOCX file
            doc = Document(self.file_path_tab1)

            # Scramble text content in the DOCX file
            for paragraph in doc.paragraphs:
                for run in paragraph.runs:
                    if run.text:
                        scrambled_text = ''.join(
                            chr(((ord(char) - 32 + 5) % 95) + 32) if 32 <= ord(char) <= 126 else char
                            for char in run.text
                        )
                        run.text = scrambled_text

            # Scramble embedded images in the DOCX file
            for rel in doc.part.rels.values():
                if "image" in rel.target_ref:  # Check if the relationship target is an image
                    image_stream = io.BytesIO(rel.target_part.blob)
                    img = Image.open(image_stream)
                    img = img.convert("RGB")

                    # Shuffle pixels to scramble the image
                    pixels = list(img.getdata())
                    random.shuffle(pixels)
                    scrambled_img = Image.new(img.mode, img.size)
                    scrambled_img.putdata(pixels)

                    # Save the scrambled image back to the relationship
                    scrambled_stream = io.BytesIO()
                    scrambled_img.save(scrambled_stream, format="PNG")
                    scrambled_stream.seek(0)
                    rel.target_part._blob = scrambled_stream.read()

            # Save the scrambled DOCX file to disk
            doc.save(scrambled_path)

            # Notify the user of success
            messagebox.showinfo("Success", f"DOCX file scrambled and saved as {scrambled_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to scramble DOCX file: {e}")

    def scramble_mp4_file(self):
        try:
            scrambled_path = f"{os.path.splitext(self.file_path_tab1)[0]}_scrambled{os.path.splitext(self.file_path_tab1)[1]}"
            with open(self.file_path_tab1, 'rb') as infile, open(scrambled_path, 'wb') as outfile:
                chunk_size = 1024 * 1024  # 1 MB chunks
                header = infile.read(1024)
                outfile.write(header)
                while chunk := infile.read(chunk_size):
                    scrambled_chunk = bytearray([byte ^ 0x55 for byte in chunk])
                    outfile.write(scrambled_chunk)
            messagebox.showinfo("Success", f"MP4 file scrambled and saved as {scrambled_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to scramble MP4 file: {e}")

    def scramble_ppt_file(self):
        try:
            scrambled_path = f"{os.path.splitext(self.file_path_tab1)[0]}_scrambled{os.path.splitext(self.file_path_tab1)[1]}"
            with zipfile.ZipFile(self.file_path_tab1, 'r') as pptx, zipfile.ZipFile(scrambled_path, 'w') as scrambled_pptx:
                for item in pptx.infolist():
                    with pptx.open(item) as file_data:
                        if item.filename.endswith('.xml') or item.filename.endswith('.rels'):
                            scrambled_content = ''.join(chr((ord(char) + 5) % 256) for char in file_data.read().decode('utf-8', errors='ignore'))
                            scrambled_pptx.writestr(item, scrambled_content.encode('utf-8'))
                        else:
                            scrambled_pptx.writestr(item, file_data.read())
            messagebox.showinfo("Success", f"PPT file scrambled and saved as {scrambled_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to scramble PPT file: {e}") 

    def save_scrambled_file(self): 
        if self.scrambled_content: 
            try: 
                # Define the scrambled file path 
                scrambled_path = f"{os.path.splitext(self.file_path_tab1)[0]}_scrambled{os.path.splitext(self.file_path_tab1)[1]}" 
                
                # Open in binary mode if the file is an image, executable, or any binary file 
                if 'image' in self.file_type or 'exe' in self.file_type or 'application' in self.file_type: 
                    with open(scrambled_path, 'wb') as scrambled_file:  # Binary write mode for binary content
                        scrambled_file.write(self.scrambled_content) 
                else: 
                    # Open in text mode if the file is a text-based file (like .txt or .docx) 
                    with open(scrambled_path, 'w', encoding='utf-8') as scrambled_file:  # Text write mode for text content
                        scrambled_file.write(self.scrambled_content)                  
                messagebox.showinfo("File Saved", f"Scrambled file saved as {scrambled_path}") 
            except Exception as e: 
                messagebox.showerror("Error", f"Failed to save scrambled file: {e}") 
        else: 
            messagebox.showerror("Error", "No scrambled content to save.")  

    def select_file_tab1(self):
        # Open file dialog to select a file
        self.file_path_tab1 = filedialog.askopenfilename()
        if self.file_path_tab1:
            self.file_path_label.config(text=f"File Path: {self.file_path_tab1}")
            self.file_type = self.identify_file_type()
            self.file_type_label.config(text=f"File Type: {self.file_type}")
            self.scramble_button.config(state=tk.NORMAL)  # Enable scramble button
    
    def identify_file_type(self):
        # Identify file type using magic
        try:
            file_type = magic.from_file(self.file_path_tab1, mime=True)
            return file_type
        except Exception as e:
            messagebox.showerror("Error", f"Failed to detect file type: {e}")
            return "Unknown"

#               2nd Tab                #

    def create_tab2_widgets(self):
        """Tab 2 - Timestomper"""
        # File Selection Button for Tab 2
        self.tab2_select_file_button = tk.Button(self.tab2, text="Select File", command=self.select_file_tab2)
        self.tab2_select_file_button.grid(row=0, column=0, padx=5, pady=10)

        # File Label for Tab 2
        self.tab2_file_label = tk.Label(self.tab2, text="No file selected.")
        self.tab2_file_label.grid(row=0, column=1, columnspan=4, padx=5, pady=5)

        # Checkbox for selecting timestamp types
        self.creation_var = tk.BooleanVar()
        self.modification_var = tk.BooleanVar()
        self.access_var = tk.BooleanVar()

        # Creation Modification Access checkboxes
        self.creation_checkbox = tk.Checkbutton(self.tab2, text="Creation Time", variable=self.creation_var)
        self.creation_checkbox.grid(row=1, column=0, columnspan=2, pady=2, sticky="w")
        self.modification_checkbox = tk.Checkbutton(self.tab2, text="Modification Time", variable=self.modification_var)
        self.modification_checkbox.grid(row=2, column=0, columnspan=2, pady=2, sticky="w")
        self.access_checkbox = tk.Checkbutton(self.tab2, text="Access Time", variable=self.access_var)
        self.access_checkbox.grid(row=3, column=0, columnspan=2, pady=2, sticky="w")

        # Calendar for selecting the date
        self.calendar_label = tk.Label(self.tab2, text="Select Date:")
        self.calendar_label.grid(row=4, column=0, padx=5, pady=5)
        self.calendar = Calendar(self.tab2, date_pattern='mm/dd/y')
        self.calendar.grid(row=4, column=1, columnspan=4, padx=5, pady=5)

        # Time input fields
        self.time_label = tk.Label(self.tab2, text="Enter Time:")
        self.time_label.grid(row=5, column=0, columnspan=4, pady=5)

        # Label and input field for Hours (HH)
        self.hours_label = tk.Label(self.tab2, text="Hours (HH):")
        self.hours_label.grid(row=6, column=0, sticky="e")
        self.hours_entry = tk.Entry(self.tab2, width=5)
        self.hours_entry.grid(row=6, column=1, sticky="w")

        # Label and input field for Minutes (MM)
        self.minutes_label = tk.Label(self.tab2, text="Minutes (MM):")
        self.minutes_label.grid(row=6, column=2, sticky="e")
        self.minutes_entry = tk.Entry(self.tab2, width=5)
        self.minutes_entry.grid(row=6, column=3, sticky="w")

        # Label and input field for Seconds (SS)
        self.seconds_label = tk.Label(self.tab2, text="Seconds (SS):")
        self.seconds_label.grid(row=7, column=0, sticky="e")
        self.seconds_entry = tk.Entry(self.tab2, width=5)
        self.seconds_entry.grid(row=7, column=1, sticky="w")

        # Label and input field for Microseconds (ssssss)
        self.microseconds_label = tk.Label(self.tab2, text="Microseconds (ssssss):")
        self.microseconds_label.grid(row=7, column=2, sticky="e")
        self.microseconds_entry = tk.Entry(self.tab2, width=10)
        self.microseconds_entry.grid(row=7, column=3, sticky="w")

        # Suggested time label for Tab 2
        self.tab2_suggestion_label = tk.Label(self.tab2, text="Suggested Time: None")
        self.tab2_suggestion_label.grid(row=8, column=0, columnspan=4, pady=10)

        # Buttons for Tab 2
        self.tab2_update_button = tk.Button(self.tab2, text="Update Time", command=self.update_file_time)
        self.tab2_update_button.grid(row=10, column=2, columnspan=2, pady=10)
        self.tab2_set_suggested_button = tk.Button(self.tab2, text="Set Suggested Time", command=self.set_suggested_time)
        self.tab2_set_suggested_button.grid(row=9, column=2, columnspan=2, pady=10)

    def select_file_tab2(self):
        # Open file dialog to select a file
        self.file_path_tab2 = filedialog.askopenfilename(title="Select File")
        if self.file_path_tab2:
            self.tab2_file_label.config(text=f"Selected: {self.file_path_tab2}")

            # Auto-calculate suggested timestamp upon file selection
            self.suggested_timestamp_tab2 = self.calculate_mean_timestamp()
            if self.suggested_timestamp_tab2:
                self.tab2_suggestion_label.config(
                    text=f"Suggested Time: {self.suggested_timestamp_tab2.strftime('%m/%d/%Y %H:%M:%S.%f')}"
                )

    def calculate_mean_timestamp(self):
        # Calculate the mean timestamp of all other files in the folder containing the selected file (excludes the selected file)
        if not self.file_path_tab2:
            messagebox.showerror("Error", "Please select a file first.")
            return None

        folder_path = os.path.dirname(self.file_path_tab2)
        timestamps = []

        try:
            # Iterate through the files in the folder
            for file_name in os.listdir(folder_path):
                full_path = os.path.join(folder_path, file_name)

                # Compare the absolute paths to ensure we are excluding the selected file
                if os.path.isfile(full_path) and os.path.abspath(full_path) != os.path.abspath(self.file_path_tab2):
                    stats = os.stat(full_path)
                    timestamps.append(stats.st_mtime)  # Only use modification time

            # Check if there are enough files to calculate the mean
            if not timestamps:
                raise ValueError("No valid files found in the folder (excluding the selected file).")

            # Calculate the mean timestamp
            mean_timestamp = sum(timestamps) / len(timestamps)
            mean_datetime = datetime.datetime.fromtimestamp(mean_timestamp)
            return mean_datetime

        except Exception as e:
            messagebox.showerror("Error", f"Could not calculate mean timestamp: {e}")
            return None
        
    def convert_to_filetime(self, input_time):
        # Convert user input time to FILETIME format (100-nanosecond intervals since 1601)
        try:
            # Ensure proper length of the input
            if len(input_time) != 20:
                raise ValueError(f"Invalid input length. Expected 20 characters, but got {len(input_time)}.")
            
            # Parse the input string in the format "YYYYMMDDHHMMSSssssss"
            year = int(input_time[0:4])
            month = int(input_time[4:6])
            day = int(input_time[6:8])
            hour = int(input_time[8:10])
            minute = int(input_time[10:12])
            second = int(input_time[12:14])
            microseconds = int(input_time[14:20])  # Microseconds (6 digits)

            # Ensure the microseconds are valid (should be in the range 0-999999)
            if microseconds < 0 or microseconds > 999999:
                raise ValueError("Microseconds should be between 0 and 999999.")

            # Construct a datetime object
            dt = datetime.datetime(year, month, day, hour, minute, second, microseconds)

            # Convert to FILETIME (100-nanosecond intervals since January 1, 1601)
            timestamp = dt.timestamp()  # Seconds since epoch
            filetime_value = int(timestamp * 10000000 + 116444736000000000)
            filetime = FILETIME(filetime_value & 0xFFFFFFFF, (filetime_value >> 32) & 0xFFFFFFFF)

            return filetime

        except Exception as e:
            messagebox.showerror("Error", f"Could not convert time: {e}")
            return None    

    def update_file_time(self):
        # Update the file time based on user input
        # Get date from calendar
        selected_date = self.calendar.get_date()
        month, day, year = map(int, selected_date.split('/'))

        # Get time from text fields (HH, MM, SS, microseconds)
        hours = self.hours_entry.get().zfill(2)  # Ensure two digits
        minutes = self.minutes_entry.get().zfill(2)
        seconds = self.seconds_entry.get().zfill(2)
        microseconds = self.microseconds_entry.get().zfill(6)  # Ensure six digits

        # Construct the input_time string (YYYYMMDDHHMMSSssssss)
        input_time = f"{year:04d}{month:02d}{day:02d}{hours}{minutes}{seconds}{microseconds}"

        # Debugging: print the constructed time string
        print(f"Constructed input time: {input_time}")

        # Validate the length of the input string
        if len(input_time) != 20:
            messagebox.showerror("Invalid Input", "Time format should be 20 characters long (YYYYMMDDHHMMSSssssss).")
            return

        # Convert to FILETIME
        filetime = self.convert_to_filetime(input_time)
        if not filetime:
            return

        # Open the file and set timestamps
        handle = CreateFileW(self.file_path_tab2, GENERIC_WRITE, 0, None, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, None)
        if handle == -1:
            messagebox.showerror("Error", "Could not open file to modify.")
            return

        # Update the file timestamps based on selected checkboxes
        if self.creation_var.get():
            SetFileTime(handle, ctypes.pointer(filetime), None, None)
        
        if self.modification_var.get():
            SetFileTime(handle, None, ctypes.pointer(filetime), None)

        if self.access_var.get():
            SetFileTime(handle, None, None, ctypes.pointer(filetime))

        # Close the handle
        kernel32.CloseHandle(handle)
        
        messagebox.showinfo("Info", "File timestamps successfully updated.")

    def set_suggested_time(self):
        # Set the suggested time to the input fields
        if not self.suggested_timestamp_tab2:
            messagebox.showerror("Error", "No suggested timestamp available.")
            return
        
        # Populate the time input fields with the suggested timestamp
        self.hours_entry.delete(0, tk.END)
        self.minutes_entry.delete(0, tk.END)
        self.seconds_entry.delete(0, tk.END)
        self.microseconds_entry.delete(0, tk.END)

        # Fill in the time entries
        self.hours_entry.insert(0, self.suggested_timestamp_tab2.strftime('%H'))
        self.minutes_entry.insert(0, self.suggested_timestamp_tab2.strftime('%M'))
        self.seconds_entry.insert(0, self.suggested_timestamp_tab2.strftime('%S'))
        self.microseconds_entry.insert(0, self.suggested_timestamp_tab2.strftime('%f'))

# Part 3 #

    def create_tab3_widgets(self):
        """Tab 3 - Junk Decoy File Generator"""
        # Title Label
        self.tab3_label = tk.Label(self.tab3, text="Junk Decoy File Generator", font=("Arial", 14, "bold"))
        self.tab3_label.grid(row=0, column=0, columnspan=2, pady=10)

        # Directory Selection
        self.tab3_directory_label = tk.Label(self.tab3, text="Target Directory:")
        self.tab3_directory_label.grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.tab3_directory_entry = tk.Entry(self.tab3, width=50)
        self.tab3_directory_entry.grid(row=1, column=1, padx=5, pady=5)

        # Browse Button
        self.tab3_browse_button = tk.Button(self.tab3, text="Browse", command=self.select_directory_tab3)
        self.tab3_browse_button.grid(row=1, column=2, padx=5, pady=5)

        # Number of Files
        self.tab3_num_files_label = tk.Label(self.tab3, text="Number of Decoy Files:")
        self.tab3_num_files_label.grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.tab3_num_files_entry = tk.Entry(self.tab3, width=10)
        self.tab3_num_files_entry.grid(row=2, column=1, padx=5, pady=5)

        # Generate Button
        self.tab3_generate_button = tk.Button(self.tab3, text="Generate Decoy Files", command=self.generate_decoy_files)
        self.tab3_generate_button.grid(row=3, column=0, columnspan=3, pady=10)

        # Status Label
        self.tab3_status_label = tk.Label(self.tab3, text="Status: Ready", font=("Arial", 10, "italic"))
        self.tab3_status_label.grid(row=4, column=0, columnspan=3, pady=5)

    def select_directory_tab3(self):
        # Open a directory selection dialog for Tab 3
        directory = filedialog.askdirectory(title="Select Directory")
        if directory:
            self.tab3_directory_entry.delete(0, tk.END)
            self.tab3_directory_entry.insert(0, directory)

    def generate_decoy_files(self):
        # Generate junk decoy files in the specified directory 
        target_directory = self.tab3_directory_entry.get().strip()
        if not os.path.isdir(target_directory):
            messagebox.showerror("Error", "Please select a valid directory.")
            return

        # Validate the number of files to generate
        try:
            num_files = int(self.tab3_num_files_entry.get().strip())
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number for decoy files.")
            return

        if num_files <= 0:
            messagebox.showerror("Error", "Number of decoy files must be greater than zero.")
            return

        try:
            # Generate junk decoy files
            self.create_junk_decoy_files(target_directory, num_files)
            self.tab3_status_label.config(text=f"Status: Successfully created {num_files} decoy files.")
            messagebox.showinfo("Success", f"{num_files} decoy files created in {target_directory}.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create decoy files: {e}")

    def create_junk_decoy_files(self, directory, num_files):
        # Create a specified number of junk decoy files in the target directory
        # List of plausible but slightly suspicious file names
        suspicious_names = [
            "temp_data", "logfile", "update_patch", "sys_driver", "error_dump",
            "cache", "runtime_config", "sys_backup", "data_store", "debug_log"
        ]
        # Extensions that appear legitimate
        suspicious_extensions = ["dat", "bin", "tmp", "log"]

        for _ in range(num_files):
            file_name = random.choice(suspicious_names) + f"_{random.randint(100, 999)}"
            file_extension = random.choice(suspicious_extensions)
            self.create_junk_decoy_file(directory, file_name, file_extension)

    def create_junk_decoy_file(self, directory, file_name, file_extension):
        # Create a single decoy file with random junk content
        file_size = random.randint(1024, 8192)  # Random size between 1 KB and 8 KB
        decoy_path = os.path.join(directory, f"{file_name}.{file_extension}")

        try:
            content = os.urandom(file_size)
            with open(decoy_path, 'wb') as decoy_file:
                decoy_file.write(content)
        except Exception as e:
            print(f"Error creating decoy file {file_name}: {e}")

    def on_close(self): 
        # Handle window close event
        # Properly destroy the application window when closed
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()  # Initialize the main Tkinter window
    app = TimestomperApp(root)  # Create an instance of the TimestomperApp
    root.mainloop()  # Start the Tkinter event loop
    
