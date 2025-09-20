import os
import logging

def setup_logging():
    log_file = "log.txt"
    if os.path.isfile(log_file):
        os.remove(log_file)

    logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
