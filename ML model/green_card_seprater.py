from time import time
import numpy as np
import cv2
from card_classification_model import *

def showImage(images):
    for title in images:
        cv2.namedWindow(title, cv2.WINDOW_NORMAL)
        cv2.imshow(title, images[title])
    cv2.waitKey(0)
    cv2.destroyAllWindows()

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
            # thirdhalf=image[points[hi] +c+10:points[hi]+c+90,400-170:400-200+92]
            image_classified_firsthalf=get_card_name(firsthalf)
            image_classified_secondhalf=get_card_name(secondhalf)
            # image_classified_thirdhalf=get_card_name(thirdhalf)
            #mycards["group"+str(groupno)+"-"+str(i)]={"first":image_classified_firsthalf,"second":image_classified_secondhalf,"third":image_classified_thirdhalf}
            # if image_classified_thirdhalf=="JCard":
                # mycards[groupno].append(["joker",image_classified_secondhalf])
            if image_classified_firsthalf=="joker":
                mycards[groupno].append(["joker",None])
            else:
                mycards[groupno].append([image_classified_firsthalf,image_classified_secondhalf])
            b += 91
            #cv2.imshow(image_classified_thirdhalf+str(i)+str(hi), thirdhalf)
        hi+=2
        groupno+=1

    return mycards

def openJokerDeckCard(image_name):
    image = cv2.imread(image_name)
    y_start_position = 0
    y_end_position = 0
    for i in range(500, 680):
        if (image[i, 700][0] == image[i, 700][1] == image[i, 700][2]) and (image[i, 700][0] > 210):
            if y_start_position == 0:
                y_start_position = i
            else:
                y_end_position = i

    x_start_position = 0
    xy_start_position = y_start_position + ((y_end_position - y_start_position) // 2)
    for i in range(570, 650):
        if (image[xy_start_position,i][0] == image[xy_start_position,i][1] == image[xy_start_position,i][2]) and (image[xy_start_position,i][0] > 210):
            if x_start_position == 0:
                x_start_position = i
                break

    # image = cv2.circle(image, (700, y_start_position), 7, (0, 0, 255), 2)
    # image = cv2.circle(image, (700, y_end_position), 7, (0, 0, 255), 2)
    # cv2.rectangle(image, (x_start_position, y_start_position), (x_start_position + 60, y_end_position), (0, 0, 255), 5) #   draw the rectangle around the joker card
    joker_deck_card = image[y_start_position:y_end_position, x_start_position:x_start_position + 60]     #   y :y+h, x :x+w
    joker_deck_card = cv2.rotate(joker_deck_card, cv2.cv2.ROTATE_90_CLOCKWISE)
    joker_deck_card_name = get_card_name(joker_deck_card)

    mid=image.shape[0]//2
    reslmean=int(image.shape[0] *(3.45/100))
    joker_deck_card1 = image[mid-reslmean:mid-20, x_start_position+123:x_start_position + 200]     #   y :y+h, x :x+w
    joker_deck_card2 = image[mid-reslmean:mid-20, x_start_position+80:x_start_position + 130]     #   y :y+h, x :x+w
    showImage({'image1': joker_deck_card1, 'image2': joker_deck_card2})

    return joker_deck_card_name, [x_start_position, y_end_position]

def getOpenDeckCard(image_name, position):
    image = cv2.imread(image_name)
    y_start_position = 0
    y_end_position = 0
    start = position[1] + 300
    for i in range(start, start + 1000):
        if ((image[i,700][0] != image[i,700][1]) and (image[i,700][0] != image[i,700][2]) and (image[i,700][1] != image[i,700][2])) and np.argmax(image[i,700]) == 1:
                if (image[i+5,700][0] == image[i+5,700][1] == image[i+5,700][2]) or (image[i-5,700][0] == image[i-5,700][1] == image[i-5,700][2]):
                    if y_start_position == 0:
                        y_start_position = i
                    else:
                        y_end_position = i
    
    image = cv2.circle(image, (700, y_start_position), 7, (0, 0, 255), 2)
    image = cv2.circle(image, (700, y_end_position), 7, (0, 0, 255), 2)
    showImage({'image', image})
