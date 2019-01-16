#!/usr/bin/env python
from time import sleep
from networktables import NetworkTables
NetworkTables.initialize(server='10.29.84.2')


def connectionListener(connected, info):
    print(info, "; Connected=%s" % connected)


NetworkTables.addConnectionListener(connectionListener, immediateNotify=True)
table = NetworkTables.getTable("vision")

while True:
    table.putNumberArray("VISION DATA", 2984)
    sleep(1)
