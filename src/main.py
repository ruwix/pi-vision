#!/usr/bin/env python
from client import Client
from vision import Vision
import cv2
client = Client("10.29.84.2")
vision = Vision(filename="images/photo2.jpg")
vision.update()

cv2.imshow("Image", vision.frame)
cv2.waitKey(0)

# while True:
#     vision.update()
#     movement = vision.getMovement()
#     client.table.putNumberArray(movement)
