from asyncio import constants
from keras.models import load_model
from PIL import Image, ImageOps
import time
import numpy as np
card_names=['Club','DIM','2','3','4','5','6','7','8','9','10','A','J','K','Q','Joker','JCard',"Heart","Spade"]


# Load the model
model = load_model('keras_model.h5')
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)


def get_card_name(image):
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.ANTIALIAS)
    image_array = np.asarray(image)
    print(image_array.shape)
    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
    data[0] = normalized_image_array
    start = time.time()
    prediction = model.__call__(data)
    print(card_names[np.argmax(prediction)])
    end= time.time()-start
    print(end)
    return (np.argmax(prediction),card_names[np.argmax(prediction)])


image = Image.open('../Data-set/9/_BIC/H-9_9.png').convert('RGB')
get_card_name(image)