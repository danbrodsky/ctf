from keras.models import load_model
from keras import backend
from keras.preprocessing.image import img_to_array, array_to_img
from keras.applications.mobilenet import decode_predictions, preprocess_input
from PIL import Image
from networks.lenet import LeNet
import numpy as np
import tensorflow as tf
#from imagehash

class_names = ['airplane', 'automobile', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']
WRONG_CLASS = 4
IMAGE_DIMS = (32, 32)

def mse(imageA, imageB):
    # the 'Mean Squared Error' between the two images is the
    # sum of the squared difference between the two images;
    # NOTE: the two images must have the same dimension
    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])

    # return the MSE, the lower the error, the more "similar"
    # the two images are
    return err

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
    #image = color_process(image)
    image = preprocess_input(image)
    # return the processed image
    return image

#lenet = LeNet()
#model = lenet._model
model = load_model('./networks/models/lenet.h5')
sess =  backend.get_session()

from cleverhans.attacks import FastGradientMethod
from cleverhans.attacks import BasicIterativeMethod
from cleverhans.utils_keras import KerasModelWrapper

from matplotlib import pyplot as plt

def labels_to_output_layer(labels):
    layers = np.zeros((len(labels), 1000))
    layers[np.arange(len(labels)), labels] = 1
    return layers

def gen_adv(img):
    wrap = KerasModelWrapper(model)
    bim = BasicIterativeMethod(wrap, sess=sess)
    border_color = 'black'
    output_layer = labels_to_output_layer([4])
    #output_layer = model.layers[-1].output
    bim_params = {'eps_iter': 0.05,
                  'nb_iter': 25,
                  'y_target': output_layer
                 }
    adv_digit = bim.generate_np(img, **bim_params)
    return adv_digit

def get_predictions(image):
    preds = model.predict(image)
    print(preds.argmax(axis=-1))
    dec_preds = decode_predictions(preds)[0]
    print(dec_preds)
    _, label1, conf1 = decode_predictions(preds)[0][0]
    return label1, conf1, dec_preds

def create_img(img_path, img_res_path, model_path, target_str, target_idx, des_conf=0.95):
    test = Image.open(img_path).resize(IMAGE_DIMS)
    test = prepare_image(test)

    test = gen_adv(test)
    print(get_predictions(test))

    test = test.reshape((32,32,3))
    img = array_to_img(test)
    plt.imshow(img)
    img.save(img_res_path)

create_img("./static/1.jpg", "./static/test/11.jpg", "./model.h5", class_names[WRONG_CLASS], WRONG_CLASS)
print(is_similar_img("./static/1.jpg", "./static/test/11.jpg"))
