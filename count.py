import cv2
import numpy as np
import matplotlib.pyplot as plt
img =  cv2.imread("2.png")

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

ret,thresh = cv2.threshold(gray,127,255,0)
contours,hierarchy = cv2.findContours(thresh.astype(np.uint8), 1, 2)
cnt = contours[0]

epsilon = 0.05*cv2.arcLength(cnt,True)
approx = cv2.approxPolyDP(cnt, epsilon,True)

hull = cv2.convexHull(cnt,returnPoints = False)
defects = cv2.convexityDefects(cnt,hull)

mask = np.zeros_like(thresh)
for i in range(defects.shape[0]):
    s,e,f,d = defects[i,0]
    start = tuple(cnt[s][0])
    end = tuple(cnt[e][0])
    far = tuple(cnt[f][0])
    cv2.line(img,start,end,[255,1,255],2)



cv2.imwrite("img_semRect.png", img)
plt.imshow(img)
plt.show()