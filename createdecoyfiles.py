import os
import random

def generate_junk_content(file_size):
    """Generate random binary junk content for decoy files."""
    return os.urandom(file_size)

def create_junk_decoy_file(directory, file_name, file_extension):
    """Create a single decoy file with random junk content."""
    file_size = random.randint(1024, 8192)  # Random size between 1 KB and 8 KB
    decoy_path = os.path.join(directory, f"{file_name}.{file_extension}")

    try:
        content = generate_junk_content(file_size)
        with open(decoy_path, 'wb') as decoy_file:
            decoy_file.write(content)
    except Exception as e:
        print(f"Error creating decoy file {file_name}: {e}")

def create_junk_decoy_files(directory, num_files=10):
    """Create a specified number of junk decoy files in the target directory."""
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
        create_junk_decoy_file(directory, file_name, file_extension)

if __name__ == "__main__":
    target_directory = input("Enter the directory to create junk decoy files: ").strip()
    num_decoys = int(input("Enter the number of junk decoy files to create: ").strip())

    print("Creating junk decoy files...")
    create_junk_decoy_files(target_directory, num_decoys)
    print("Junk decoy files created successfully.")
