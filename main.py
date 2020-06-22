import numpy as np
import cv2
import matplotlib.pyplot as plt

points = []
bound = False


def addpoint(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        points.append((x, y))


cap = cv2.VideoCapture(0)

cv2.namedWindow("polyim")
cv2.setMouseCallback("polyim", addpoint)

while cap.isOpened():
    ret, frame = cap.read()

    scale_percent = 35  # percent of original size
    width = int(frame.shape[1] * scale_percent / 100)
    height = int(frame.shape[0] * scale_percent / 100)
    dim = (width, height)
    resized = cv2.resize(frame, dim)

    npts = np.array(points)
    polyim = cv2.polylines(resized, [npts], True, (255, 0, 0))
    cv2.imshow("polyim", polyim)
    for p in points:
        cv2.circle(polyim, p, 3, (255, 0, 0))


    key = cv2.waitKey(1)
    if key == ord('s'):
        cv2.waitKey()

    elif key == ord('q'):
        break;

cap.release()
cv2.destroyAllWindows()
