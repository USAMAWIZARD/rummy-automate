from asyncio import constants
from keras.models import load_model
from PIL import Image, ImageOps ,ImageFilter
import numpy as np
import cv2
card_names=['clubs','diamonds','2','3','4','5','6','7','8','9','10','ace','jack','king','queen','joker','JCard',"hearts","spades"]


# Load the model
model = load_model('keras_model.h5')
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)


def get_card_name(image):

    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = Image.fromarray(image)
    image = image.convert("L")
    image = image.filter(ImageFilter.FIND_EDGES)
    size = (224, 224)
    image=image.convert('RGB')
    image = ImageOps.fit(image, size, Image.ANTIALIAS)
    image_array = np.asarray(image)
    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
    data[0] = normalized_image_array
    prediction = model.__call__(data)
    return card_names[np.argmax(prediction)]


#image = Image.open('../Data-set/9/_BIC/H-9_9.png').convert('RGB')
#get_card_name(image)