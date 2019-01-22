#!/usr/bin/env python
from client import Client
from vision import Vision
import cv2
client = Client("10.29.84.2")
vision = Vision(filename="photo.jpg")

# while True:
vision.update()
vision.getPosition()
cv2.imshow("Image",vision.frame)
cv2.waitKey(0)
# movement = vision.movement
    # client.table.putNumberArray(movement)
