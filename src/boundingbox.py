class BoundingBox:
    def __init__(self, points, center, corners, area, offset):
        self.points = points
        self.center = center
        self.corners = corners
        self.area = area
        self.offset = offset

    def __str__(self):
        return "Center: {}\nArea: {}\nOffset {}".format(
            self.center, self.area, self.offset)
