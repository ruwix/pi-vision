import cv2
import numpy as np
import math


class Vision:
    def __init__(self):
        self.camera = cv2.VideoCapture(0)

    def update(self):
        _, frame = self.camera.read()
        imgray = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        hsv = cv2.split(imgray)
        ret, thresh = cv2.threshold(hsv[2], 200, 255, 0)
        self.contours, _ = cv2.findContours(thresh, cv2.RETR_TREE,
                                            cv2.CHAIN_APPROX_SIMPLE)

    def getPosition(self):
        return [0, 0]

    def getMovement(self):
        return [0, 0]
