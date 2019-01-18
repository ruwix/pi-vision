#!/usr/bin/env python
from client import Client
from vision import Vision
client = Client("10.29.84.2")
vision = Vision()


while True:
    vision.update()
    movement = vision.movement
    # client.table.putNumberArray(movement)
