import numpy as np
import cv2
from utils import ArducamUtils
import array
import fcntl
import os
from matplotlib import pyplot as plt

def resize(frame, dst_width):
    width = frame.shape[1]
    height = frame.shape[0]
    scale = dst_width * 1.0 / width
    return cv2.resize(frame, (int(scale * width), int(scale * height)))

cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
arducam_utils = ArducamUtils(0)
cap.set(cv2.CAP_PROP_CONVERT_RGB, arducam_utils.convert2rgb)
cv2.namedWindow("window")


while cap.isOpened():
	ret, frame = cap.read()
	frame = arducam_utils.convert(frame)
	resizedImg = resize(frame, 1280.0)
	#dimensions = resizedImg.shape
 
	image_height = resizedImg.shape[0]
	image_width = resizedImg.shape[1]
	left_img = frame[0:image_height, 0:(image_width//2)]
	right_img = frame[0:image_height, (image_width//2):image_width]
	
	stereo = cv2.StereoBM_create(numDisparities=16, blockSize=15)
	#disparity = stereo.compute(left_img, right_img)
	
	#cv2.imshow('gray', disparity)
	
	cv2.imshow("left", left_img)
	cv2.imshow("right", right_img)
	
	key = cv2.waitKey(1)
	if key == ord('q'):
		break


#plt.imshow(disparity,'gray')
#plt.show()

cap.release()
cv2.destroyAllWindows()
