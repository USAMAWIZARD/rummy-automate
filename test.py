import cv2
import numpy as np
import os
import time

image=cv2.imread('3.png')
#image= cv2.rectangle(image, (0, 0), (300, image.shape[0]), (22,22,0), -1)
# image = cv2.line(image, (400,0), (400,1200), (223,223,11), 10)

for i in range(2180):
	if ((image[i,400][0] != image[i,400][1]) and (image[i,400][0] != image[i,400][2]) and (image[i,400][1] != image[i,400][2])) and np.argmax(image[i,400]) == 1:
			if (image[i+5,400][0] == image[i+5,400][1] == image[i+5,400][2]) or (image[i-5,400][0] == image[i-5,400][1] == image[i-5,400][2]):
				image = cv2.circle(image, (400,i), 10, (0, 0, 255), 5)

cv2.namedWindow('GameWindow', cv2.WINDOW_NORMAL)
cv2.imshow('GameWindow' , image)
cv2.waitKey()




