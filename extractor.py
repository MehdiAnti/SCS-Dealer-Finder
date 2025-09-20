import os
import subprocess
import logging
import re
from file_manager import ets2_files, ats_files


def extract_scs_files(folder_path, converter_path):
    scs_files = get_scs_files(folder_path)
    total_scs = len(scs_files)

    if total_scs == 0:
        logging.info("No relevant .scs files found.")
        return None

    temp_dir = os.path.join(folder_path, "temp")
    os.makedirs(temp_dir, exist_ok=True)

    for i, scs_file in enumerate(scs_files, start=1):
        normalized_scs_file = os.path.normpath(scs_file)
        normalized_temp_dir = os.path.normpath(temp_dir)

        command = ["data/converter_pix.exe", "-b", normalized_scs_file, "-extract_d", "/def/city/", "-e", normalized_temp_dir]
        logging.info(f"Processing: {os.path.basename(scs_file)}")

        try:
            # Execute the command and wait for it to complete
            result = subprocess.run(command, check=True, creationflags=subprocess.CREATE_NO_WINDOW)
            logging.info(f"Successfully processed {os.path.basename(scs_file)}")
        except subprocess.CalledProcessError as e:
            logging.error(f"Error processing  {os.path.basename(scs_file)}: {e.stderr}")
            return None  # Stop further processing if extraction fails

        print_progress_bar(i, total_scs)

    return temp_dir


def get_scs_files(folder_path):
    scs_files = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.scs'):
            full_path = os.path.join(folder_path, filename)
            if "Euro Truck Simulator 2" in folder_path and filename in ets2_files:
                scs_files.append(full_path)
            elif "American Truck Simulator" in folder_path and filename in ats_files:
                scs_files.append(full_path)
    return scs_files

def search_sui_files(folder_path):
    dealer_dict = {}
    unsupported_chars = re.compile(r'[^a-zA-Z0-9 _-]')
    norm_folder_path = os.path.normpath(folder_path)
    for root, dirs, files in os.walk(norm_folder_path):
        for file_name in files:
            if file_name.endswith('.sui'):
                file_path = os.path.join(root, file_name)
                norm_file_path = os.path.normpath(file_path)
                try:
                    with open(norm_file_path, 'r', encoding='utf-8', errors='ignore') as file:
                        content = file.read()
                        names = re.findall(r'city_name:\s*"([^"]*)"', content)
                        dealers = re.findall(r'vehicle_brands\[\]:\s*"([^"]*)"', content)
                        name_dic_values = re.findall(r'city_name_localized:\s*"@@?([^@]*)@@?"', content)

                        for name, dealer, name_dic in zip(names, dealers, name_dic_values):
                            dealer = dealer.replace("intnational", "international")
                            dealer = dealer.capitalize()

                            if "daf" in dealer.lower():
                                dealer = dealer.upper().replace("DAF", "DAF")
                            elif "man" in dealer.lower():
                                dealer = dealer.upper().replace("MAN", "MAN")

                            name_dic = name_dic.capitalize()
                            if unsupported_chars.search(name):
                                formatted_name = f"{name} ({name_dic})"
                            else:
                                formatted_name = name

                            if dealer not in dealer_dict:
                                dealer_dict[dealer] = []

                            dealer_dict[dealer].append(formatted_name)

                except Exception as e:
                    logging.error(f"Error reading {os.path.basename(norm_file_path)}: {e}")

    if not dealer_dict:
        logging.info("No .sui files found in the extracted directory.")

    return dealer_dict

def print_progress_bar(iteration, total, length=40):
    percent = (iteration / total) * 100
    filled_length = int(length * iteration // total)
    green_color = "\033[92m"  # Green text
    reset_color = "\033[0m"   # Reset to default color
    bar = f"{green_color}#" * filled_length + "-" * (length - filled_length)
    print(f'\r|{bar}{reset_color}| {percent:.2f}%', end='\r')

    if iteration == total:
        print()
