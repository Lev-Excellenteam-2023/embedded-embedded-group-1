import cv2
import time


def camra():
    camera = cv2.VideoCapture(0)
    return_value, image = camera.read()
    if (not return_value):
        raise Exception("camera disconnected")
    return image
