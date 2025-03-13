from decouple import config
from pathlib import Path

WRDS_USERNAME = config("WRDS_USERNAME", default="test")
BASE_DIR = Path(config("BASE_DIR"))
DATA_DIR = Path(config("DATA_DIR"))
OUTPUT_DIR = Path(config("OUTPUT_DIR"))
