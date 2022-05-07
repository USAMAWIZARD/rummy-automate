import cv2
import numpy as np
from time import sleep
import os
import time
from PIL import Image,ImageFilter
comparison_dict={}
def load_comparison_images():
	all_file_names=os.listdir('Data-set/')
	for file_name in all_file_names:
		image=cv2.imread('Data-set/'+file_name)
		comparison_dict[file_name]=image #cv2.Canny(image, 50, 150)

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

def find_cards_on_screen(croped_screen):
	cards_on_screen = {}
	all_file_names=comparison_dict.keys()
	for card_name in all_file_names:
		(found,x,y,h,w)=find_card(card_name,croped_screen)
		if found:
			cards_on_screen[card_name]={'x':x[0],'y':y[0],'h':h,'w':w}	
		else:
			print("not found")
	return cards_on_screen
		

def find_card(image_name,image):
	#change paratmeter to screen shot or frame
	template = comparison_dict[image_name]
	result = cv2.matchTemplate(image[0], template, cv2.TM_CCOEFF_NORMED)
	threshold = 0.8
	loc = np.where( result >= threshold)
	height, width = template.shape[:2]
	if len(loc[0])==0:
		return (False,0,0,0,0)
	x = []
	y = []

	for pt in zip(*loc[::-1]):
		x.append(pt[0])
		y.append(pt[1])      # have to write for multiple same cards on the screen
		cv2.rectangle(image[0], pt, (pt[0]+width, pt[1]+height), (0,0,255), 5)
	return (True,x,y,height,width)

	cv2.imshow("detected",ResizeWithAspectRatio(image[0],width=300))
	cv2.waitKey(0)					#test code
	cv2.destroyAllWindows()



