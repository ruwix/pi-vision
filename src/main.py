#!/usr/bin/env python
from client import Client
from vision import Vision
client = Client("10.29.84.2")
vision = Vision()
while True:
    movement = vision.getMovement()
    client.table.putNumberArray(movement)
