# SCS Dealer Finder

**SCS Dealer Finder** is a Python-based tool for extracting and identifying truck dealer cities from `.scs` map files used in **Euro Truck Simulator 2 (ETS2)** and **American Truck Simulator (ATS)**. It helps you collect the cities of the truck dealer from game files and export it in multiple formats.


## Features

- Extract dealer and city name from `.scs` files for ETS2 and ATS.  
- Normalize dealer names and fix common typos.  
- Export data in **TXT**, **JSON**, or **XML** formats.
- Extract game version from `version.scs`.


## Requirements

- **Python 3.10+**  
- **Windows OS** (tested)  
- `tkinter` (usually included with Python)  
- `converter_pix.exe` (included in `data/` folder)  
- SCS files list configuration (`data/scs_files.txt`)  


## Installation

1. Clone the repository:
```bash
git clone https://github.com/MehdiAnti/SCS-Dealer-Finder.git
cd scs-dealer-finder
```
2. Ensure Python 3.10+ is installed.
3. Make sure converter_pix.exe and scs_files.txt are in the data/ folder.

## Usage

1. Run the program:
```
python main.py
```
2. Select the folder containing your .scs files.
3. The program will extract dealer and city data.
4. Choose an export format:

    0 → TXT
   
    1 → JSON
   
    2 → XML
5. Check log.txt for detailed logs.

    ⚠️ Only run one instance at a time to avoid conflicts in temporary folders and log files.

## Thanks to

[**mwl4**](https://github.com/mwl4) - [Converter PIX](https://github.com/mwl4/ConverterPIX) project

## License

This project is licensed under the **MIT License**.

## Contributing

Contributions are welcome! Please submit bug reports, feature requests, or pull requests via GitHub.

## Disclaimer

This tool is provided as-is. The author is not responsible for any damage or data loss resulting from its use. Always backup your files before processing.
