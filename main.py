import numpy as np
import cv2
from utils import ArducamUtils
import array
import fcntl
import os

inputPoints = []
blue = (255, 0, 0)
bound = False
outputWidth = 0
outputHeight = 0


def addpoint(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        inputPoints.append((x, y))

def resize(frame, dst_width):
    width = frame.shape[1]
    height = frame.shape[0]
    scale = dst_width * 1.0 / width
    return cv2.resize(frame, (int(scale * width), int(scale * height)))
    

cap = cv2.VideoCapture(0, cv2.CAP_V4L2)

arducam_utils = ArducamUtils(0)

cap.set(cv2.CAP_PROP_CONVERT_RGB, arducam_utils.convert2rgb)

cv2.namedWindow("polyim")
cv2.setMouseCallback("polyim", addpoint)

while cap.isOpened():
    ret, frame = cap.read()
    frame = arducam_utils.convert(frame)
    resizedImg = resize(frame, 1280.0)
    if bound:
        rows, cols, ch = resizedImg.shape

        pts1 = np.float32(np.float32(inputPoints))
        pts2 = np.float32([[0, 0], [0, outputHeight], [outputWidth, outputHeight], [outputWidth, 0]])

        M = cv2.getPerspectiveTransform(pts1, pts2)
        warpedImg = cv2.warpPerspective(resizedImg, M, (outputWidth, outputHeight))

        cv2.imshow("Input", resizedImg)
        cv2.imshow("Output", warpedImg)

    else:
        cv2.putText(resizedImg, "Click 4 points counter clockwise from top left, Press 'S' when Done", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0))
        polyim = cv2.polylines(resizedImg, [np.array(inputPoints)], True, blue)
        cv2.imshow("polyim", polyim)
        for p in inputPoints:
            cv2.circle(polyim, p, 3, blue)

    key = cv2.waitKey(1)
    if key == ord('s'):
        outputWidth = abs(inputPoints[2][0] - inputPoints[0][0])
        outputHeight = abs(inputPoints[2][1] - inputPoints[0][1])
        print("Input List")
        print(inputPoints)
        print("Output Width")
        print(outputWidth)
        print("Output Height")
        print(outputHeight)
        bound = True
        cv2.destroyWindow("polyim")

    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
