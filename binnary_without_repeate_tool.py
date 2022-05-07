#convert to binnary without repeating the cards from PIL import Image,ImageFilter
import cv2
import numpy as np
from time import sleep
import os
import time
from PIL import Image,ImageFilter

from find_image import *
img = Image.open("./without-binnary/2.png")
img = img.convert("L")
img = img.filter(ImageFilter.FIND_EDGES)
nimg = np.array(img)
image = cv2.cvtColor(nimg, cv2.COLOR_RGB2BGR)
image = cv2.cvtColor(nimg, cv2.COLOR_RGB2BGR)
image= cv2.rectangle(image, (0, 0), (160, image.shape[0]), (0,0,0), -1)
image= cv2.rectangle(image, (600, 1200), (image.shape[1], image.shape[0]), (0,0,0), -1)
image= cv2.rectangle(image, (580, 0), (image.shape[1], 850), (0,0,0), -1)
image= cv2.rectangle(image, (850, 800), (image.shape[1], image.shape[0]), (0,0,0), -1)
cards_found=find_cards_on_screen([image])

print(img)
for card in cards_found.keys():
    x=cards_found[card]["x"]
    y=cards_found[card]["y"]
    w=cards_found[card]["w"]
    h=cards_found[card]["h"]

    cv2.rectangle(image, (x, y), (x + w, y + h), (36,255,12), 5) #draw the rectangle around the total cards
cv2.imshow('thresh', ResizeWithAspectRatio(image,300))
cv2.waitKey(0)

print(cards_found)
#img.save("result.png")