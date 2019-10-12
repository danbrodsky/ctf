#!/usr/bin/env python3
import os
import sys
import time
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
# Custom Networks
from networks.lenet import LeNet
import tensorflow as tf
from PIL import Image
from imagehash import phash
from functools import reduce

from keras.applications.mobilenet import preprocess_input
from keras.models import load_model
from keras.preprocessing.image import img_to_array, array_to_img
from PIL import Image
from imagehash import phash
import numpy as np
from keras import backend as K

DIR = os.path.abspath(os.path.dirname(__file__))
class_names = ['airplane', 'automobile', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']
WRONG_CLASS = 7
IMAGE_DIMS = (32, 32)

def predictimg(path,lenet):
    image = plt.imread(path)
    confidence = lenet.predict(image)[0]
    predicted_class = np.argmax(confidence)
    #predicted_class = WRONG_CLASS
    return  predicted_class, class_names[predicted_class],confidence[predicted_class]

def mse(imageA, imageB):
    # the 'Mean Squared Error' between the two images is the
    # sum of the squared difference between the two images;
    # NOTE: the two images must have the same dimension
    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])

    # return the MSE, the lower the error, the more "similar"
    # the two images are
    return err


# I'm pretty sure I borrowed this function from somewhere, but cannot remember
# the source to cite them properly.
def hash_hamming_distance(h1, h2):
    s1 = str(h1)
    s2 = str(h2)
    return sum(map(lambda x: 0 if x[0] == x[1] else 1, zip(s1, s2)))


def is_similar_img(path1, path2):
    image1 = np.asarray(Image.open(path1))
    image2 = np.asarray(Image.open(path2))

    dist = mse(image1, image2)
    return dist < 200

def color_process(imgs):
    if imgs.ndim < 4:
        imgs = np.array([imgs])
        imgs = imgs.astype('float32')
        mean = [125.307, 122.95, 113.865]
        std  = [62.9932, 62.0887, 66.7048]
        for img in imgs:
            for i in range(3):
                img[:,:,i] = (img[:,:,i] - mean[i]) / std[i]
        return imgs

def prepare_image(image, target=IMAGE_DIMS):
    # if the image mode is not RGB, convert it
    if image.mode != "RGB":
        image = image.convert("RGB")

    # resize the input image and preprocess it
    image = image.resize(target)
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)
    image = preprocess_input(image)
    processed = color_process(image)

    # return the processed image
    return processed


def create_img(img_path, img_res_path, target_idx, des_conf=0.95):
    original_image = Image.open(img_path).resize(IMAGE_DIMS)
    original_image = prepare_image(original_image)
    model = load_model('./networks/models/lenet.h5')

    model_input_layer = model.layers[0].input
    model_output_layer = model.layers[-1].output

    max_change_above = original_image + 0.01
    max_change_below = original_image - 0.01

    # Create a copy of the input image to hack on
    hacked_image = np.copy(original_image)

    # How much to update the hacked image in each iteration
    learning_rate = 0.01

    # Define the cost function.
    # Our 'cost' will be the likelihood out image is the target class according to the pre-trained model
    cost_function = model_output_layer[0, 0]

    # We'll ask Keras to calculate the gradient based on the input image and the currently predicted class
    # In this case, referring to "model_input_layer" will give us back image we are hacking.
    gradient_function = K.gradients(cost_function, model_input_layer)[0]

    # Create a Keras function that we can call to calculate the current cost and gradient
    grab_cost_and_gradients_from_model = K.function([model_input_layer, K.learning_phase()], [cost_function, gradient_function])

    cost = 0.0

    # In a loop, keep adjusting the hacked image slightly so that it tricks the model more and more
    # until it gets to at least 80% confidence
    while cost < 0.99:
        # Check how close the image is to our target class and grab the gradients we
        # can use to push it one more step in that direction.
        # Note: It's really important to pass in '0' for the Keras learning mode here!
        # Keras layers behave differently in prediction vs. train modes!
        cost, gradients = grab_cost_and_gradients_from_model([hacked_image, WRONG_CLASS])

        # Move the hacked image one step further towards fooling the model
        # print gradients
        hacked_image += np.sign(gradients) * learning_rate

        # Ensure that the image doesn't ever change too much to either look funny or to become an invalid image
        #hacked_image = np.clip(hacked_image, max_change_below, max_change_above)
        #hacked_image = np.clip(hacked_image, -1.0, 1.0)

        print("Model's predicted likelihood that the image is a {}: {:.8}%".format(class_names[WRONG_CLASS],cost * 100))

    hacked_image = hacked_image.reshape((32,32,3))
    img = array_to_img(hacked_image)
    img.save(img_res_path)


if __name__ == "__main__":
    a,b,c = predictimg('./static/0.jpg', LeNet())
    print(a, b, c)
    create_img("./static/0.jpg", "./static/test/00.jpg", 7)
    print( is_similar_img("./static/0.jpg", "./static/test/00.jpg"))
    a,b,c = predictimg('./static/test/00.jpg', LeNet())
    print(a, b, c)

