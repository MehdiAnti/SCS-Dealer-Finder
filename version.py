import os
import subprocess
import re
import logging

def extract_game_version(folder_path, temp_folder):
    version_file_path = os.path.join(folder_path, "version.scs")

    if os.path.isfile(version_file_path):
        command = ["data/converter_pix.exe", "-b", version_file_path, "-extract_d", "/", "-e", temp_folder]
        try:
            subprocess.run(command, check=True, creationflags=subprocess.CREATE_NO_WINDOW)
            sui_file_path = os.path.join(temp_folder, "version.sii")
            if os.path.isfile(sui_file_path):
                with open(sui_file_path, 'r', encoding='utf-8', errors='ignore') as file:
                    content = file.read()
                    match = re.search(r'version:\s*"([^"]*)"', content)
                    if match:
                        return match.group(1)
        except subprocess.CalledProcessError:
            logging.error(f"Error extracting version from {version_file_path}")

    return None
