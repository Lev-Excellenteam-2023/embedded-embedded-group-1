import os

from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")
PROJECT_NAME = "birds-detector-tis9s"
CONFIDENCE_THRESHOLD = 55
OVERLAP_THRESHOLD = 30
BIRDS_COUNT_THRESHOLD = [1]
INTERVAL = 5

SERVER_URL = "http://127.0.0.1:5000/get_alert"
CAMERA_ID = 1
