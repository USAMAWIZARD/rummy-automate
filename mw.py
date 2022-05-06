import cv2
from PIL import Image,ImageFilter
import os
import time

from find_image import *
croped_grp={}
all_groups={}
load_comparison_images()
#print(len(comparison_dict.keys()))

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

# Load iamge, grayscale, adaptive threshold

img = Image.open("2.png")
img = img.convert("L")
img = img.filter(ImageFilter.FIND_EDGES)
#img.save("result.png")
nimg = np.array(img)
image = cv2.cvtColor(nimg, cv2.COLOR_RGB2BGR)

#image =cv2.imread("result.png")
# print("dim",np.asarray(img).shape)
# img = img.convert("L")
# print("dim",np.asarray(img).shape)
# img = img.filter(ImageFilter.FIND_EDGES)
# image=np.asarray(img)
#image = cv2.imread('./Data-set/result.png')
image= cv2.rectangle(image, (0, 0), (160, image.shape[0]), (0,0,0), -1)
image= cv2.rectangle(image, (600, 1200), (image.shape[1], image.shape[0]), (0,0,0), -1)
image= cv2.rectangle(image, (580, 0), (image.shape[1], 850), (0,0,0), -1)
image= cv2.rectangle(image, (850, 800), (image.shape[1], image.shape[0]), (0,0,0), -1)

result = image.copy()
gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
#gray=image
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

# for c in cnts:
x,y,w,h = cv2.boundingRect(c)

# if w>200 and h>50:

diclen="group"+str(len(croped_grp.keys()))
croped_group = [image[y:3000, x:500]]

all_groups[diclen]={}
print(x,y,w,h)
# if x>300:
croped_grp["imagedeck"]=image #its a deck card
cards_in_this_group= find_card_in_group(croped_group)
all_groups[diclen]["deck"]=cards_in_this_group
#continue

#croped_grp[diclen]["image"]=croped_group
all_groups[diclen]["x"]=x
all_groups[diclen]["y"]=y
all_groups[diclen]["h"]=h
all_groups[diclen]["w"]=w
cards_in_this_group= find_card_in_group(croped_group)
all_groups[diclen]["cards"]=cards_in_this_group


print(all_groups)

cv2.imshow('thresh', ResizeWithAspectRatio(thresh,300))
cv2.imshow('opening', ResizeWithAspectRatio(opening,300))
cv2.imshow('image', ResizeWithAspectRatio(image,300))
cv2.waitKey()