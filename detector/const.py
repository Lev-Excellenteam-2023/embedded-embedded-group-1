import os

from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")
CAMERA_ID = os.getenv("CAMERA_ID")

PROJECT_NAME = "birds-detector-tis9s"
CONFIDENCE_THRESHOLD = 55
OVERLAP_THRESHOLD = 30
INTERVAL = 5
BIRDS_COUNT_THRESHOLD = [10]

SERVER_URL = "http://127.0.0.1:5000"
SERVER_GET_ALERT_PATH = "/get_alert"

LISTENER_PORT = 5009
