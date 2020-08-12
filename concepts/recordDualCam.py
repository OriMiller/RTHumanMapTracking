from utils import ArducamUtils
import cv2

cv2.startWindowThread()

cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
arducam_utils = ArducamUtils(0)
cap.set(cv2.CAP_PROP_CONVERT_RGB, arducam_utils.convert2rgb)

ret, frame = cap.read()
frame = arducam_utils.convert(frame)
frame_height, frame_width = frame.shape[0:2]
scale = 0.25
image_width = int(frame_width * scale)
image_height = int(frame_height * scale)

out = cv2.VideoWriter('outpy.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 10, (image_width, image_height))
start = True
while cv2.waitKey(10) != ord('q'):
	ret, frame = cap.read()
	frame = arducam_utils.convert(frame)
	frame = cv2.resize(frame, (image_width, image_height))
	out.write(frame)
	cv2.imshow('frame',frame)

cap.release()
out.release()
cv2.destroyAllWindows() 
