import os
import random
import io
from PIL import Image
from docx import Document
import zipfile

def reverse_text_file(input_path, output_path=None):
    try:
        with open(input_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        unscrambled = ''.join([chr((ord(char) - 5) % 256) for char in content])
        
        output_path = output_path or f"{os.path.splitext(input_path)[0]}_unscrambled.txt"
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(unscrambled)
        
        print(f"Text file unscrambled and saved as {output_path}")
    except Exception as e:
        print(f"Error unscrambling text file: {e}")

def reverse_image_file(input_path, output_path=None):
    try:
        print("Reversing scrambled image requires the original scrambling order, which is not reversible in this method.")
        return
    except Exception as e:
        print(f"Error unscrambling image file: {e}")

def reverse_executable_file(input_path, output_path=None):
    try:
        with open(input_path, 'rb') as file:
            content = bytearray(file.read())
        
        unscrambled_content = bytearray([byte ^ 0xFF for byte in content])
        
        output_path = output_path or f"{os.path.splitext(input_path)[0]}_unscrambled.exe"
        with open(output_path, 'wb') as file:
            file.write(unscrambled_content)
        
        print(f"Executable file unscrambled and saved as {output_path}")
    except Exception as e:
        print(f"Error unscrambling executable file: {e}")

def reverse_docx_file(input_path, output_path=None):
    try:
        doc = Document(input_path)
        for paragraph in doc.paragraphs:
            for run in paragraph.runs:
                if run.text:
                    run.text = ''.join([chr((ord(char) - 5) % 256) for char in run.text])
        
        for rel in doc.part.rels.values():
            if "image" in rel.target_ref:
                print("Reversing scrambled images in DOCX requires the original order, which is not reversible.")
        
        output_path = output_path or f"{os.path.splitext(input_path)[0]}_unscrambled.docx"
        doc.save(output_path)
        
        print(f"DOCX file unscrambled and saved as {output_path}")
    except Exception as e:
        print(f"Error unscrambling DOCX file: {e}")

def reverse_mp4_file(input_path, output_path=None):
    try:
        with open(input_path, 'rb') as file:
            content = bytearray(file.read())
        
        unscrambled_content = content[:1024] + bytearray([byte ^ 0x55 for byte in content[1024:]])
        
        output_path = output_path or f"{os.path.splitext(input_path)[0]}_unscrambled.mp4"
        with open(output_path, 'wb') as file:
            file.write(unscrambled_content)
        
        print(f"MP4 file unscrambled and saved as {output_path}")
    except Exception as e:
        print(f"Error unscrambling MP4 file: {e}")

def reverse_ppt_file(input_path, output_path=None):
    try:
        unscrambled_data = io.BytesIO()
        with zipfile.ZipFile(input_path, 'r') as pptx:
            with zipfile.ZipFile(unscrambled_data, 'w') as unscrambled_pptx:
                for item in pptx.infolist():
                    data = pptx.read(item.filename)
                    if item.filename.endswith('.xml') or item.filename.endswith('.rels'):
                        unscrambled_content = ''.join(chr((ord(char) - 5) % 256) for char in data.decode('utf-8'))
                        unscrambled_pptx.writestr(item, unscrambled_content.encode('utf-8'))
                    else:
                        unscrambled_pptx.writestr(item, data)
        
        output_path = output_path or f"{os.path.splitext(input_path)[0]}_unscrambled.pptx"
        with open(output_path, 'wb') as file:
            file.write(unscrambled_data.getvalue())
        
        print(f"PPT file unscrambled and saved as {output_path}")
    except Exception as e:
        print(f"Error unscrambling PPT file: {e}")

def reverse_file(file_type, input_path, output_path=None):
    # Dispatcher mapping file type to reverse function
    dispatcher = {
        'text': reverse_text_file,
        'image': reverse_image_file,
        'executable': reverse_executable_file,
        'docx': reverse_docx_file,
        'mp4': reverse_mp4_file,
        'ppt': reverse_ppt_file,
    }

    # Call the appropriate function
    if file_type in dispatcher:
        dispatcher[file_type](input_path, output_path)
    else:
        print(f"Unsupported file type for reversal: {file_type}")

# Example usage
if __name__ == "__main__":
    file_type = input("Enter the file type to reverse (text, image, executable, docx, mp4, ppt): ").strip().lower()
    input_path = input("Enter the scrambled file path: ").strip().strip('"').strip("'")
    output_path = input("Enter the output file path (optional): ").strip().strip('"').strip("'") or None

    reverse_file(file_type, input_path, output_path)
