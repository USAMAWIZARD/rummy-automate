import cv2
import numpy as np
from subprocess import run
from time import sleep
import os
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
def find_card_in_group(croped_group):
	cards_in_this_group = {}
	all_file_names=os.listdir('Data-set/')
	for card_name in all_file_names:
		(found,x,y,h,w)=find_card(card_name,croped_group)
		if found: #change to variable
			cards_in_this_group[card_name]={'x':x,'y':y,'h':h,'w':w}
			print(found) #add card and name
			
	return cards_in_this_group
		


def find_card(image_name,croped_group):
	image = croped_group #change paratmeter to screen shot or frame
	template = cv2.imread('Data-set/'+image_name) 
	result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
	threshold = 0.8
	loc = np.where( result >= threshold)
	height, width = template.shape[:2]
	if len(loc[0])==0:
		return (False,0,0,0,0)
	print(height,width,loc[0])
	print(loc)
	x = []
	y = []

	for pt in zip(*loc[::-1]):
		x.append(pt[0])
		y.append(pt[1])

		cv2.rectangle(image, pt, (pt[0]+width, pt[1]+height), (0,0,255), 5)
	return (True,x,y,height,width)

	cv2.imshow("detected",ResizeWithAspectRatio(image,width=300))
	cv2.waitKey(0)
	cv2.destroyAllWindows()

