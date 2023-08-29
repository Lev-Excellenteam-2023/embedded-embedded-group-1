"""A function that send alert to server when there is a folk of birds in the processed image

DOD: a funnction that get num of birds and timstamp and send an http message to the server.
 json file{camera_id, time, birds_sum}"""
import logging

import requests
import json
import const
logging.basicConfig(filename="log.txt",level=logging.INFO)

def send_bird_alert(camera_id, timestamp, birds_count):

    server_url = const.server_url
    data = {
        "camera_id": camera_id,
        "time": timestamp,
        "birds_sum": birds_count
    }

    try:
        response = requests.post(server_url, json=data)
        if response.status_code == 200:
          logging.info("Alert sent successfully.")
        else:
            logging.info(f"Failed to send alert. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        logging.info(f"Error sending alert: {e}")
