import numpy as np
import cv2
import imutils
from time import time

def getImageCoOrdinates(template):
    image_o = cv2.imread('assets/1080x1920/4.png')
    template = cv2.imread(template)
    template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    image = cv2.cvtColor(image_o, cv2.COLOR_BGR2GRAY)
    loc = False
    threshold = 0.75
    w, h = template.shape[::-1]
    for scale in np.linspace(0.2, 1.0, 20)[::-1]:
        resized = imutils.resize(template, width = int(template.shape[1] * scale))
        w, h = resized.shape[::-1]
        res = cv2.matchTemplate(image,resized,cv2.TM_CCOEFF_NORMED)
        max_confidence = np.max(res)
        if max_confidence < threshold:
            return False
        loc = np.where(res >= max_confidence)
        print(max_confidence)
        if len(list(zip(*loc[::-1]))) > 0:
            break
    if loc and len(list(zip(*loc[::-1]))) > 0:
        for pt in zip(*loc[::-1]):
            image_o = cv2.rectangle(image_o, pt, (pt[0] + w, pt[1] + h), (0, 255, 255), 2)
            return pt[0], pt[1], w, h
    return False

template = 'assets/1080x1920/buttons/box.png'

res = getImageCoOrdinates(template)

print(res)


