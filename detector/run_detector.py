"""
this file is used to run the detector.
it is the main file of the detector.
"""
import logging
import time
from datetime import datetime
import threading

from detector.alert_sender import send_bird_alert
from detector.cam import take_image
from detector.neural_network_accses import process_image
from detector.listener import run_listener
from detector.const import BIRDS_COUNT_THRESHOLD, INTERVAL


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
            if birds_count > BIRDS_COUNT_THRESHOLD[0]:
                timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                send_bird_alert(timestamp, birds_count)
            time.sleep(INTERVAL)
        except Exception as e:
            logging.error(f"Error occurred: {e}")


if __name__ == '__main__':
    logging.basicConfig(filename='detector.log', level=logging.INFO, format='%(asctime)s %(message)s')
    # I am running the listener in a separate thread
    listener_thread = threading.Thread(target=run_listener,args=(BIRDS_COUNT_THRESHOLD,))
    listener_thread.start()

    # and the detector in the main thread
    main()
