import cv2
import numpy as np
import math
import boundingbox


class Vision:
    def __init__(self, filename=None):
        self.camera = cv2.VideoCapture(0)
        self.filename = filename
        self.thresh = None
        self.contours = None
        self.boxes = []
        self.frame = None
        self.movement = [0, 0]

    def updateThreshold(self):
        if self.filename == None:
            _, self.frame = self.camera.read()
        else:
            self.frame = cv2.imread(self.filename)
        bgr = cv2.split(self.frame)
        green = cv2.bitwise_xor(bgr[2], bgr[1])

        lower_thresh = 190
        upper_thresh = 255
        _, self.thresh = cv2.threshold(green, lower_thresh, upper_thresh, 0)

    def updateContours(self):
        self.contours, _ = cv2.findContours(self.thresh, cv2.RETR_TREE,
                                            cv2.CHAIN_APPROX_SIMPLE)

    def updateBoxes(self):
        height, width, _ = self.frame.shape
        for cnt in self.contours:
            area = cv2.contourArea(cnt)
            if area > 100:
                moments = cv2.moments(cnt)
                if moments["m00"] != 0:
                    center = (int(moments["m10"] / moments["m00"]),
                              int(moments["m01"] / moments["m00"]))
                else:
                    center = (0, 0)
                offset = (center[0]/width, center[1]/height)
                # output = cv2.drawContours(self.frame, [cnt], -1, (0, 255, 0), 2)
                # output = cv2.circle(self.frame, center, 5, (0, 0, 255), -1)
                # cv2.imshow("Image", self.frame)
                self.boxes.append(boundingbox.BoundingBox(
                    cnt, center, area, offset))
        # cv2.waitKey(0)

    def updateMovement(self):
        length = len(self.boxes)
        if length != 2:
            print("WARNING: More than 2 boxes, using the first 2")

        x = (self.boxes[1].offset[0] + self.boxes[0].offset[0])/2
        y = (self.boxes[1].offset[1] + self.boxes[0].offset[1])/2
        x_thresh = 0.05
        x_error = x - 0.5
        if abs(x_error) > x_thresh:
            self.movement[0] = x_error * 2

    def update(self):
        self.boxes = []
        self.updateThreshold()
        self.updateContours()
        self.updateBoxes()
        self.updateMovement()

    def getMovement(self):
        return self.movement
