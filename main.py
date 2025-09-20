import os
import shutil
import logging
import colorama
from file_manager import load_scs_files, export_to_file, select_folder, ets2_files, ats_files
from extractor import extract_scs_files, search_sui_files
from version import extract_game_version
from logger import setup_logging

# Set up colorama
colorama.init()

# Set up logging
setup_logging()

logging.info("Application opened")

# Load SCS files
load_scs_files("data/scs_files.txt")

selected_folder = select_folder()

if selected_folder:
    logging.info(f"Selected folder: {selected_folder}")
    temp_dir = extract_scs_files(selected_folder, "data/converter_pix.exe")
    
    if temp_dir:
        dealer_data = search_sui_files(temp_dir)

        game_version = extract_game_version(selected_folder, temp_dir)
        version_suffix = f"_{game_version}" if game_version else ""

        game_type = "ets2" if "Euro Truck Simulator 2" in selected_folder else "ats" if "American Truck Simulator" in selected_folder else ""

        while True:
            print("\033[92mSelect export format:\033[0m")
            print("\033[92m0 for .txt (Plain text file)\033[0m")
            print("\033[92m1 for .json (JavaScript Object Notation)\033[0m")
            print("\033[92m2 for .xml (eXtensible Markup Language)\033[0m")
            file_type = input("\033[92mSelect an option (0, 1, 2): \033[0m")

            file_type_map = {'0': 'txt', '1': 'json', '2': 'xml'}

            if file_type in file_type_map:
                output_file = f"{game_type}_dealers_cities{version_suffix}.{file_type_map[file_type]}"
                export_to_file(dealer_data, output_file, file_type_map[file_type])
                break
            else:
                print("\033[91mInvalid option selected.\033[0m")

        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)

print(f"\033[92mProcessing completed. Check log.txt for details.\033[0m")

# Log application closing
logging.info("Application closed")

input("\n\033[92mPPress ENTER to close")
