# FileForge 
anti-forensics-tool

**FileForge: A File Scrambler and Timestamp Manager**
Description:

FileForge is a Python-based desktop application designed to:
- Scramble various file types (e.g., text, images, executables, Word documents, videos, presentations) for security or privacy reasons.
- Modify file timestamps (creation, modification, and access times) to protect metadata or adjust file records.
- Obfuscation of Payloads 

This tool uses a simple GUI built with Tkinter and Pillow, with additional support for working with .docx and .pptx files. It's ideal for anyone needing to modify or obfuscate file metadata or content.

**Features:**
1. File Scrambler
- Scramble contents of text files, images, executables, Word documents, MP4 videos, and PowerPoint presentations.
2. Timestamp Management
- Modify file timestamps (creation, modification, access). Creation times are precise to the millisecond, modification and access times are precise to the microseconds.
- Automatically suggest a timestamp based on the average of files in the same folder.
- Supports updating creation time on Windows with the pywin32 library.
3. File Type Detection
- Automatically detects file types and applies relevant scrambling methods.

**Installation:**
Clone this repository: 
git clone https://github.com/jojojogate/FileForge.git

Navigate to the project directory:
cd FileForge

Install required dependencies:
pip install -r requirements.txt

To run the application:
python FileForgeV3.py


**Usage**:
Scrambler Tab:
1. Click the "Select File" button to choose a file to scramble.
2. Select the appropriate file, and the program will auto-detect the file type.
3. Click "Scramble File" to obfuscate the content of the file.
4. Click "Save Scrambled File" to save file with the scrambled content.
   
**Timestamp Update Tab:**
1. Click the "Select File" button to choose a file.
2. Use the checkboxes to select which timestamps to modify (Creation, Modification, or Access).
3. Use the calendar and time input fields to specify the new timestamp.
4. Click "Update Time" to apply the new timestamp to the selected file.
5. You can also set the timestamp to the suggested mean timestamp calculated from other files in the same directory by clicking "Set Suggested Time".

**Dependencies:**
Tkinter: For GUI components.
Pillow: For image processing.
python-magic: For file type identification.
python-docx: For handling .docx files.
pywin32: For manipulating file creation times on Windows.
Known Issues:
The creation timestamp only updates to the nearest millisecond, while the modification and access times update to the nearest microseconds.
Some file types (e.g., encrypted files) might not be supported for scrambling.
