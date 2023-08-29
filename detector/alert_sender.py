"""A function that send alert to server when there is a folk of birds in the processed image

DOD: a funnction that get num of birds and timstamp and send an http message to the server.
 json file{camera_id, time, birds_sum}"""
import logging

import requests
from detector.const import SERVER_URL, CAMERA_ID


def send_bird_alert(timestamp, birds_count):
    """
    this function send alert to server when there is a folk of birds in the processed image.
    :param timestamp: time of the alert.
    :param birds_count: number of birds in the image.
    :return: None
    """
    logging.info(f"Sending alert. Timestamp: {timestamp}, Birds count: {birds_count}")
    data = {
        "camera_id": CAMERA_ID,
        "time": timestamp,
        "birds_sum": birds_count
    }

    try:
        response = requests.post(SERVER_URL, json=data)
        if response.status_code == 200:
            logging.info("Alert sent successfully.")
        else:
            logging.error(f"Failed to send alert. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Error sending alert: {e}")
