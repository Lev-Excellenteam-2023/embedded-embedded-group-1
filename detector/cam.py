import cv2
import logging


def take_image():
    """
    this function take an image from the camera.
    :return: image
    """
    try:
        camera = cv2.VideoCapture(0)
        return_value, image = camera.read()
        if not return_value:
            raise ValueError("unable to capture image")
        return image
    except Exception as e:
        logging.error(f"Error taking image: {e}")
        raise e
