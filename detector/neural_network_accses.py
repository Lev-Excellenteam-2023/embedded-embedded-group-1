"""
this module is used to access the neural network
for the purpose of detecting birds in the image
"""
import logging
from roboflow import Roboflow
from detector.const import API_KEY, PROJECT_NAME, CONFIDENCE_THRESHOLD, OVERLAP_THRESHOLD

MODEL = None


class ModelInitializationError(Exception):
    pass


def init_model():
    """
    this function is used to initialize the model
    :return: None
    """
    try:
        rf = Roboflow(api_key=API_KEY)
        project = rf.workspace().project(PROJECT_NAME)
        model = project.version(1).model
        return model
    except Exception as e:
        logging.error("Model initialization failed: %s", e)
        raise ModelInitializationError("Failed to initialize model.")


def process_image(image):
    """
    this function is used to process the image
    :param image: the image to be processed
    :return: the processed image
    """
    try:
        global MODEL
        if MODEL is None:
            MODEL = init_model()
        prediction = MODEL.predict(image, confidence=CONFIDENCE_THRESHOLD, overlap=OVERLAP_THRESHOLD).json()
        logging.info("Image processed successfully.")
        return prediction
    except ModelInitializationError:
        logging.error("Model initialization failed.")
        return None
    except Exception as e:
        logging.error("Failed to process image: %s", e)
        raise e


