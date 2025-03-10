from decouple import config

WRDS_USERNAME = config("WRDS_USERNAME", default="test")
BASE_DIR = config("BASE_DIR")
DATA_DIR = config("DATA_DIR")
