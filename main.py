import numpy as np
import cv2
import matplotlib.pyplot as plt

inputPoints = []
outputPoints = []
ipts = np.array([])
opts = np.array([])
bound = False
state = False


def addpoint(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        if not state:
            inputPoints.append((x, y))

        else:
            outputPoints.append((x, y))


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

    if bound:
        rows, cols, ch = resized.shape

        pts1 = np.float32(ipts)
        pts2 = np.float32(opts)

        M = cv2.getPerspectiveTransform(pts1, pts2)
        dst = cv2.warpPerspective(resized, M, (300, 300))

        cv2.imshow("Output", dst)
        cv2.imshow("Input", resized)

    else:
        if not state:
            cv2.putText(resized, "Click 4 points, Press 'N' when done", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.25, (255, 0, 0))

        else:
            cv2.putText(resized, "Click 4 new points, Press 'S' when Done", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.25, (255, 0, 0))

        ipts = np.array(inputPoints)
        opts = np.array(outputPoints)
        if not state:
            polyim = cv2.polylines(resized, [ipts], True, (255, 0, 0))
            cv2.imshow("polyim", polyim)
            for p in inputPoints:
                cv2.circle(polyim, p, 3, (255, 0, 0))

        else:
            polyim = cv2.polylines(resized, [opts], True, (255, 0, 0))
            cv2.imshow("polyim", polyim)
            for p in outputPoints:
                cv2.circle(polyim, p, 3, (255, 0, 0))

    key = cv2.waitKey(1)
    if key == ord('s'):
        bound = True
        cv2.destroyWindow("polyim")

    elif key == ord('n'):
        state = True

    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
