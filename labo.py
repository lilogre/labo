# Data aquisition and processing script
# This script reads data from various sensors, processes it, and writes it to an Excel file using openpyxl.
from datetime import datetime
from pathlib import Path
import logging
from modules.ImageAnalysis import AnalyzeColor
from modules.AudioAnalysis import AnalyzeAudio

# Configure settings
log_lvl = logging.INFO  # Set the logging level
log_dir = Path("./logs") # Directory for log files
data_dir = Path("./datafiles") # Directory for data files

testimg = "./example_data/test.jpg"
testaudio = "./example_data/Recording6.mp3"

# Create a directory for data files if it doesn't exist
if not data_dir.is_dir():
    try:
        data_dir.mkdir(parents=True)
    except Exception as e:
        print(f"Failed to create data directory: {e}")
        exit(1)

# Create a directory for log files if it doesn't exist
if not log_dir.is_dir():
    try:
        log_dir.mkdir(parents=True)
    except Exception as e:
        print(f"Failed to create log directory: {e}")
        exit(1)

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(filename=f"{log_dir}/{datetime.now().strftime("%Y-%m-%d")}.log", level=log_lvl, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

def main():
    logger.info("Starting data acquisition and processing script.")

    AnalyzeColor(data_dir, testimg, 500, 1000, 1000, 1500)
    #AnalyzeAudio(data_dir, testaudio)
    
    logger.info("Data acquisition and processing completed successfully.")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"An error occurred: {e}")
    else:
        logger.info("Script completed successfully.")
    finally:
        logger.info("Exiting script.")