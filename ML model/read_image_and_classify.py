from PIL import Image, ImageOps
#from card_classification_model import *
import cv2
import numpy as np
from PIL import Image,ImageFilter
import os
import webcolors
import time
def ResizeWithAspectRatio(image, width=None, height=None, inter=cv2.INTER_AREA):
    dim = None
    (h, w) = image.shape[:2]

    if width is None and height is None:
        return image
    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))

    return cv2.resize(image, dim, interpolation=inter)

print("start",time.time())

croped_grp={}
all_groups={}

# Load iamge, grayscale, adaptive threshold

img = Image.open("../without-binnary/_BIC/3.png")
img = img.convert("L")
img = img.filter(ImageFilter.FIND_EDGES)
nimg = np.array(img)
image = cv2.cvtColor(nimg, cv2.COLOR_RGB2BGR)
image= cv2.rectangle(image, (0, 0), (300, image.shape[0]), (22,22,0), -1)
image= cv2.rectangle(image, (600, 1300), (image.shape[1], image.shape[0]), (0,0,0), -1)
image= cv2.rectangle(image, (580, 0), (image.shape[1], 850), (0,0,0), -1)
image= cv2.rectangle(image, (850, 800), (image.shape[1], image.shape[0]), (0,0,0), -1)
image= cv2.rectangle(image, (510, 0), (image.shape[1], image.shape[0]), (0,0,0), -1)

gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
thresh = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,51,9)
# Fill rectangular contours
cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
for c in cnts:
    cv2.drawContours(thresh, [c], -1, (255,255,255), -1)

# Morph open
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1,1))
opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)

# Draw rectangles
cnts = cv2.findContours(opening, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]


i=0
for c in cnts:
    x,y,w,h = cv2.boundingRect(c)
    #cv2.rectangle(image, (x, y), (x + w, y + h), (36,255,12), 3) #draw the rectangle around the total cards

    if w>=150    and h>80:
        print(x,y,w,h)
        
        cv2.rectangle(image, (x, y), (x + w, y + h), (255,255,255), 3) #draw the rectangle around the total cards
        b=100
        for i  in range((h//100)):
            cv2.rectangle(image, (168, 230+b), (168 + 343, 230 +b), (11,111,111), 3) #draw the rectangle around the total cards
            if i%3==0:
                b-=9
            cv2.rectangle(image, (x, y+b ), (x + w+100, y +b+100), (11,111,111), 3) #draw the rectangle around the total cards
            b+=100

        print(i)
        i+=1
# for i in range(10):
#     if i%3==0:
#         b-=7
#     cv2.rectangle(image, (168, 230+b), (168 + 343, 230 +b), (11,111,111), 3) #draw the rectangle around the total cards
#     b+=100
cv2.imshow('opening', ResizeWithAspectRatio(image,350))
cv2.waitKey()
#print(get_card_name()))