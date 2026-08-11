import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image

model = tf.keras.models.load_model("models/civic_model.h5")

classes = ["pothole", "crack", "garbage", "normal"]

def predict_image(img_path):

    img = image.load_img(img_path, target_size=(224,224))
    img = image.img_to_array(img)

    img = np.expand_dims(img, axis=0)
    img = img/255.0

    prediction = model.predict(img)

    return classes[np.argmax(prediction)]