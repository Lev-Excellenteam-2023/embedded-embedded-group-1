"""
this file is used to run the detector.
it is the main file of the detector.
"""
import logging
import time
from datetime import datetime

from detector.alert_sender import send_bird_alert
from detector.cam import take_image
from detector.neural_network_accses import process_image
from detector.const import BIRDS_COUNT_THRESHOLD



def main():
    """
    this function is used to run the detector.
    :return: None
    """
    while True:
        try:
            image = take_image()
            if image is None:
                logging.error("Failed to take image.")
                continue
            prediction = process_image(image)
            if prediction is None:
                logging.error("Failed to process image.")
                continue
            birds_count = len(prediction["predictions"])
            if birds_count > BIRDS_COUNT_THRESHOLD:
                timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                send_bird_alert(timestamp, birds_count)
            time.sleep(5)
        except Exception as e:
            logging.error(f"Error occurred: {e}")
            time.sleep(5)


if __name__ == '__main__':
    logging.basicConfig(filename='detector.log', level=logging.INFO, format='%(asctime)s %(message)s')
    main()
