import cv2
from PIL import Image,ImageFilter
import os
import time

from find_image import *
print("start",time.time())

croped_grp={}
all_groups={}
load_comparison_images()

def get_groups_of_all_cards():
    for c in cnts:
        x,y,w,h = cv2.boundingRect(c)
        cv2.rectangle(image, (x, y), (x + w, y + h), (36,255,12), 3) #draw the rectangle around the total cards
        if w>200 and h>50:
            for card in all_cards_dict.keys():
                all_cards_dict[card]["y"]
            print(x,y,w,h)
        
    print(all_cards_dict)
# Load iamge, grayscale, adaptive threshold

img = Image.open("./without-binnary/6.png")
img = img.convert("L")
img = img.filter(ImageFilter.FIND_EDGES)
nimg = np.array(img)
image = cv2.cvtColor(nimg, cv2.COLOR_RGB2BGR)
image= cv2.rectangle(image, (0, 0), (160, image.shape[0]), (0,0,0), -1)
image= cv2.rectangle(image, (600, 1200), (image.shape[1], image.shape[0]), (0,0,0), -1)
image= cv2.rectangle(image, (580, 0), (image.shape[1], 850), (0,0,0), -1)
image= cv2.rectangle(image, (850, 800), (image.shape[1], image.shape[0]), (0,0,0), -1)
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


croped_screen = [image[250:3000, 0:500]]  #can be optimized
#cv2.imshow('thresh', ResizeWithAspectRatio(croped_screen[0],200))
#cv2.waitKey(0)
all_cards_dict= find_cards_on_screen(croped_screen)
get_groups_of_all_cards()


print("end",time.time())

cv2.imshow('thresh', ResizeWithAspectRatio(thresh,300))
cv2.imshow('opening', ResizeWithAspectRatio(opening,300))
cv2.imshow('image', ResizeWithAspectRatio(image,300))
cv2.waitKey()