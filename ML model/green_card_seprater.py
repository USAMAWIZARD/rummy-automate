import numpy as np
import os
import time
import cv2
from card_classification_model import *
def get_cards_on_screen(image_name):
    mycards=[]
    image=cv2.imread(image_name)
    points = []
    for i in range(2180):
        if ((image[i,400][0] != image[i,400][1]) and (image[i,400][0] != image[i,400][2]) and (image[i,400][1] != image[i,400][2])) and np.argmax(image[i,400]) == 1:
                if (image[i+5,400][0] == image[i+5,400][1] == image[i+5,400][2]) or (image[i-5,400][0] == image[i-5,400][1] == image[i-5,400][2]):
                    if points and abs(points[-1] - i) > 20: # card diffrence
                        image = cv2.circle(image, (400,i), 10, (0, 0, 255), 5)
                        points.append(i)
                    elif not points:
                        image = cv2.circle(image, (400,i), 10, (0, 0, 255), 5)
                        points.append(i)
    hi = 0
    mycards=[]
    groupno=0
    
    while hi < (len(points)-1):

        b=91
        h = (points[hi+1] - points[hi])-130
        #cv2.rectangle(image, (400, points[hi]), (400 + 100, points[hi] ), (11,3,111), 3) #draw the rectangle around the total cards
        mycards.append([])
        for i  in range(round(h/91)):
            #cv2.rectangle(image, (400-20, points[hi]), (400+90 , points[hi] +b), (11,i,111), 10) #draw the rectangle around the total cards
            c=b-90
            firsthalf=image[points[hi] +c+10:points[hi]+c+90,400-20:400+ 90]  #y :y+h, x :x+w
            secondhalf=image[points[hi] +c+10:points[hi]+c+90,400-110:400-100+92]
            thirdhalf=image[points[hi] +c+10:points[hi]+c+90,400-170:400-200+92]
            image_classified_firsthalf=get_card_name(firsthalf)
            image_classified_secondhalf=get_card_name(secondhalf)
            image_classified_thirdhalf=get_card_name(thirdhalf)
            #mycards["group"+str(groupno)+"-"+str(i)]={"first":image_classified_firsthalf,"second":image_classified_secondhalf,"third":image_classified_thirdhalf}
            if image_classified_thirdhalf=="JCard":
                mycards[groupno].append(["joker",image_classified_secondhalf])
            elif image_classified_firsthalf=="joker":
                mycards[groupno].append(["joker",None])
            else:
                mycards[groupno].append([image_classified_firsthalf,image_classified_secondhalf])
            b+=91
            #cv2.imshow(image_classified_thirdhalf+str(i)+str(hi), thirdhalf)
        hi+=2
        groupno+=1

    return mycards

# print("end",time.time()-start)
# print(mycards)
# cv2.namedWindow('GameWindow', cv2.WINDOW_NORMAL)
# cv2.imshow('GameWindow' , image)
# cv2.waitKey()