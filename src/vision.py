import cv2
import numpy as np
import math
import boundingbox


class Vision:
    def __init__(self, lower_thresh=180, upper_thresh=255, x_thresh=0.05, filename=None):
        self.camera = cv2.VideoCapture(0)
        if not self.camera.isOpened():
            print("WARNING: No camera found")
        self.filename = filename
        self.lower_thresh = lower_thresh
        self.upper_thresh = upper_thresh
        self.x_thresh = x_thresh
        self.mask = None
        self.contours = None
        self.image_points = []
        self.object_points = np.array([[-1, 1, 0], [-1, -1, 0], [1, 1, 0], [
                                      1, -1, 0]],dtype=np.float32)  # TODO get measurements

        self.frame = None
        self.movement = [0, 0]
        with np.load('calibration-data.npz') as X:
            self.camera_matrix, self.dist_coeffs = [
                X[i] for i in ('camera_matrix', 'dist_coeffs')]

    def updateMask(self):
        """Update the mask of the reflective tape."""
        if self.filename == None:
            _, self.frame = self.camera.read()
        else:
            self.frame = cv2.imread(self.filename)
        imgray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)
        hsv = cv2.split(imgray)
        bgr = cv2.split(self.frame)
        # green = cv2.bitwise_xor(bgr[2], bgr[1])
        # green = cv2.bitwise_and(green, hsv[2])
        green = cv2.bitwise_and(bgr[1], hsv[2])
        # cv2.imshow("IMAGE",hsv[2])
        # cv2.waitKey(0)
        _, self.mask = cv2.threshold(
            green, self.lower_thresh, self.upper_thresh, 0)

    def updateContours(self):
        """Update the contours of the mask."""
        self.contours, _ = cv2.findContours(self.mask, cv2.RETR_TREE,
                                            cv2.CHAIN_APPROX_SIMPLE)

    def updateBoxes(self):
        """Update the bounding boxes from the contours."""
        for cnt in self.contours:
            area = cv2.contourArea(cnt)
            if area > 0:
                # cv2.drawContours(
                #     self.frame, [cnt], -1, (255, 0, 0), 2)
                epsilon = 0.01*cv2.arcLength(cnt, True)
                approx = cv2.approxPolyDP(cnt, epsilon, True)
                cv2.drawContours(
                    self.frame, [approx], -1, (255, 0, 0), 3)
                for point in approx:
                    p = (point[0][0], point[0][1])
                    p2 = [float(point[0][0]), float(point[0][1])]
                    self.image_points.append([p2])
                    cv2.circle(self.frame, p, 5, (0, 0, 255), -1)

    def getPosition(self):
        corners = np.array(self.image_points,dtype=np.float32)
        _, rvec, tvec, _ = cv2.solvePnPRansac(
            self.object_points, corners, self.camera_matrix, self.dist_coeffs)
        print(tvec)
        # Rt = np.matrix(cv2.Rodrigues(rvec)[0])
        # R = Rt.transpose()
        # pos = -R * tvec
        # print(pos)

    def updateMovement(self):
        """Update the required movemnt of the robot."""
        length = len(self.boxes)
        if length != 2:
            print("WARNING: More or less than 2 boxes found, using the first 2")
        else:
            x = (self.boxes[1].offset[0] + self.boxes[0].offset[0])/2
            y = (self.boxes[1].offset[1] + self.boxes[0].offset[1])/2
            x_error = x - 0.5
            if abs(x_error) > self.x_thresh:
                self.movement[0] = x_error * 2

    def update(self):
        """Update the vision tracking (run all update functions)."""
        self.boxes = []
        self.updateMask()
        self.updateContours()
        self.updateBoxes()
        self.updateMovement()
