#!/usr/bin/env python
import numpy as np
import cv2
import glob
# images = glob.glob('*.jpg')


class Calibrate:
    def __init__(self, images, checkersize, height=9, width=7):
        self.images = images
        self.checkersize = checkersize
        self.height = height
        self.width = width
        self.criteria = (cv2.TERM_CRITERIA_EPS +
                         cv2.TERM_CRITERIA_MAX_ITER, self.checkersize, 0.001)
        self.objp = np.zeros((width*height, 3), np.float32)
        self.objp[:, :2] = np.mgrid[0:height, 0:width].T.reshape(-1, 2)
        self.camera_matrix = None
        self.dist_coeffs = None

    def calibrate(self):
        objpoints = []
        imgpoints = []
        for filename in images:
            img = cv2.imread(filename)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            ret, corners = cv2.findChessboardCorners(
                gray, (self.height, self.width), None)
            if ret == True:
                objpoints.append(self.objp)

                corners2 = cv2.cornerSubPix(
                    gray, corners, (11, 11), (-1, -1), self.criteria)
                imgpoints.append(corners2)

                img = cv2.drawChessboardCorners(
                    img, (self.height, self.width), corners2, ret)

        ret, self.camera_matrix, self.dist_coeffs, rvecs, tvecs = cv2.calibrateCamera(
            objpoints, imgpoints, gray.shape[::-1], None, None)

    def save(self):
        np.savez("calibration-data", camera_matrix=self.camera_matrix,
                 dist_coeffs=self.dist_coeffs)

    def drawSquares(self):
        axis = np.float32([[0, 0, 0], [0, 3, 0], [3, 3, 0], [3, 0, 0],
                           [0, 0, -3], [0, 3, -3], [3, 3, -3], [3, 0, -3]])
        for filename in self.images:
            img = cv2.imread(filename)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            ret, corners = cv2.findChessboardCorners(
                gray, (self.height, self.width), None)
            if ret == True:
                corners2 = cv2.cornerSubPix(
                    gray, corners, (11, 11), (-1, -1), self.criteria)
                _, rvecs, tvecs, inliers = cv2.solvePnPRansac(
                    self.objp, corners2, self.camera_matrix, self.dist_coeffs)
                imgpts, jac = cv2.projectPoints(
                    axis, rvecs, tvecs, self.camera_matrix, self.dist_coeffs)

                img = self._drawBox(img, corners2, imgpts)
                cv2.imshow('img', img)
                k = cv2.waitKey(0) & 0xff

        cv2.destroyAllWindows()

    def _drawBox(self, img, corners, imgpts):
        imgpts = np.int32(imgpts)
        imgpts = np.reshape(imgpts, (-1, 2))

        img = cv2.drawContours(img, [imgpts[:4]], -1, (0, 255, 0), -3)

        for i, j in zip(range(4), range(4, 8)):
            img = cv2.line(img, tuple(imgpts[i]), tuple(imgpts[j]), (255), 3)

        img = cv2.drawContours(img, [imgpts[4:]], -1, (0, 0, 255), 3)

        return img


images = glob.glob("calibration-images/*.jpg")
c = Calibrate(images, 20)
c.calibrate()
c.save()
c.drawSquares()
