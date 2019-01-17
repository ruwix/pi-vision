from networktables import NetworkTables


class Client:
    def __init__(self, ip, tablename="vision"):
        NetworkTables.initialize(server=ip)
        NetworkTables.addConnectionListener(
            self._connectionListener, immediateNotify=True)
        self.table = NetworkTables.getTable(tablename)

    def _connectionListener(self, connected, info):
        print(info, "; Connected=%s" % connected)
