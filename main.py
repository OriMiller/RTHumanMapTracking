import numpy as np
import cv2

inputPoints = []
blue = (255, 0, 0)
bound = False
outputWidth = 0
outputHeight = 0


def addpoint(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        inputPoints.append((x, y))


cap = cv2.VideoCapture(0)

cv2.namedWindow("polyim")
cv2.setMouseCallback("polyim", addpoint)

while cap.isOpened():
    ret, frame = cap.read()

    scale_percent = 50
    width = int(frame.shape[1] * scale_percent / 100)
    height = int(frame.shape[0] * scale_percent / 100)
    dim = (width, height)
    resizedImg = cv2.resize(frame, dim)

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
