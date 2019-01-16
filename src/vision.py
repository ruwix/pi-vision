#!/usr/bin/env python
import cv2
import numpy as np
import math
file = "input.jpg"
img = cv2.imread(file)
imgray = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
hsv = cv2.split(imgray)
ret, thresh = cv2.threshold(hsv[2], 200, 255, 0)
contours, _ = cv2.findContours(thresh, cv2.RETR_TREE,
                               cv2.CHAIN_APPROX_SIMPLE)
for cnt in contours:
    x0, y0, w, h = cv2.boundingRect(cnt)
    x1, y1 = x0+w, y0+h
    area = w * h
    if area > 100:
        img = cv2.rectangle(img, (x0, y0), (x1, y1), (255, 255, 255), 1)
cv2.imwrite("output.jpg", img)
