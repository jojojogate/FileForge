# FileForge 
An Anti-forensics-tool


# A File Scrambler and Timestamp Manager

FileForge is a Python-based desktop application designed to:
- Scramble various file types (e.g., text, images, executables, Word documents, videos, presentations) for security or privacy reasons.
- Modify file timestamps (creation, modification, and access times) to protect metadata or adjust file records. 

This tool uses a simple GUI built with Tkinter and Pillow, with additional support for working with .docx and .pptx files. It's ideal for anyone needing to modify or obfuscate file metadata or content.

# Features:
1. File Scrambler
- Scramble contents of text files, images, executables, Word documents, MP4 videos, and PowerPoint presentations.
2. Timestamp Management
- Modify file timestamps (creation, modification, access). Edited times are precise to the microseconds to prevent detection of timestomping.
- Automatically suggest a timestamp based on the average of other files in the same folder to camouflage wanted file.

# Installation: (6 Steps)

Step 1. Install  Python 3.12 https://www.python.org/downloads/

Step 2. Install Git https://git-scm.com/downloads/win

Step 3. Clone this repository: git clone https://github.com/jojojogate/FileForge.git

Step 4. Navigate to the project directory: cd FileForge

Step 5. Install required dependencies: pip install -r requirements.txt

Step 6. To run the application(run as administrator): python FileForgeV4.py

# Usage:

**Scrambler Tab:**
1. Click on the "Scrambler" Tab
2. Click the "Select File" button to choose a file to scramble.
3. Select the appropriate file, and the program will auto-detect the file type.
4. Click "Scramble File" to obfuscate the content of the file. (Scrambled file will automatically be saved)

   
**Timestamp Update Tab:**
1. Click on the "Timestamp Update" Tab
2. Click the "Select File" button to choose a file.
3. Use the checkboxes to select which timestamps to modify (Creation, Modification, or Access).
4. Use the calendar and time input fields to specify the new timestamps.
5. Use the "Set Suggested Time" button to fill the boxes with the calculated mean timestamp of the other files in the same directory. (Optional)
6. Click "Update Time" to apply the new timestamp to the selected file.
   

**Decoy Generator Tab:**
1. Click on the "Decoy Generator" Tab
2. Click the "Browse" button to choose a target directory.
3. Specify the number of decoy files to generate.
4. Click "Generate Decoy Files" to generate.


# Dependencies:
Tkinter: For GUI components.

Pillow: For image processing.

python-magic: For file type identification.

python-docx: For handling .docx files.

pywin32: For manipulating file creation times on Windows.

# Known Issues:
Some file types (e.g., encrypted files) might not be supported for scrambling.
