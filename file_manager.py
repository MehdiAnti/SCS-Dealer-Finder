import logging
import json

ets2_files = set()
ats_files = set()

def load_scs_files(scs_files_path):
    global ets2_files, ats_files
    ets2_files.clear()
    ats_files.clear()

    try:
        with open(scs_files_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            sections = content.splitlines()
            current_section = None

            for line in sections:
                line = line.strip()
                if line.startswith("ets_entries:"):
                    current_section = 'ets'
                elif line.startswith("ats_entries:"):
                    current_section = 'ats'
                elif line.startswith("{") or line.startswith("}"):
                    continue
                elif current_section == 'ets':
                    ets2_files.add(line)
                elif current_section == 'ats':
                    ats_files.add(line)

    except FileNotFoundError:
        logging.error("scs_files.txt not found.")
        print("Error: scs_files.txt not found.")
        exit(1)
    except ValueError as ve:
        logging.error(f"Error in scs_files.txt format: {ve}")
        print(f"Error: {ve}")
        exit(1)



def export_to_file(dealer_dict, output_file, file_type):
    try:
        if file_type == 'txt':
            export_to_txt(dealer_dict, output_file)
        elif file_type == 'json':
            export_to_json(dealer_dict, output_file)
        elif file_type == 'xml':
            export_to_xml(dealer_dict, output_file)
        else:
            logging.error(f"Unsupported file type: {file_type}")
    except Exception as e:
        logging.error(f"Error exporting data: {e}")

def export_to_txt(dealer_dict, output_file):
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            for dealer, cities in dealer_dict.items():
                f.write(f"{dealer}: {', '.join(cities)}\n\n")
        logging.info(f"Data exported to {output_file}")
    except Exception as e:
        logging.error(f"Error exporting data to .txt: {e}")

def export_to_json(dealer_dict, output_file):
    json_data = {}
    for dealer, cities in dealer_dict.items():
        json_data[dealer] = cities

    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, indent=4)
        logging.info(f"Data exported to {output_file}")
    except Exception as e:
        logging.error(f"Error exporting data to .json: {e}")

def export_to_xml(dealer_dict, output_file):
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("<dealers>\n")
            for dealer, cities in dealer_dict.items():
                f.write(f"  <dealer name=\"{dealer}\">\n")
                for city in cities:
                    f.write(f"    <city>{city}</city>\n")
                f.write("  </dealer>\n")
            f.write("</dealers>\n")
        logging.info(f"Data exported to {output_file}")
    except Exception as e:
        logging.error(f"Error exporting data to .xml: {e}")

def select_folder():
    import tkinter as tk
    from tkinter import filedialog
    root = tk.Tk()
    root.withdraw()
    folder_selected = filedialog.askdirectory()
    return folder_selected
