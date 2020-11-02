from keras.applications import mobilenet_v2
from tensorflow.keras.preprocessing.image import img_to_array
import tensorflow as tf
from tensorflow.keras.preprocessing import image_dataset_from_directory
import pandas as pd
import os
import numpy as np
import sklearn.metrics.pairwise as sk
import matplotlib.pyplot as plt
from keras.applications.vgg16 import VGG16
from keras.applications.vgg16 import preprocess_input
from os import listdir
from PIL import Image as PImage
from keras.applications import mobilenet_v2

def loadImages(path):
    # return array of images

    imagesList = listdir(path)
    loadedImages = []
    for image in imagesList:
        img = PImage.open(path + image)
        loadedImages.append(img)

    return loadedImages

path = "/Users/wusongyuan/Desktop/test/test_dir/testsub_dir/"

# your images in an array
imgs = loadImages(path)

for img in imgs:
    # you can show every image
    print(type(img))

list_of_expanded_array = list()
for i in range(len(imgs)-1):
    img = imgs[i]
    new_size = (224,224)
    img = img.resize(new_size)
    tmp = img_to_array(img)
    expand = np.expand_dims(tmp, axis = 0)
    list_of_expanded_array.append(expand)
    
images = np.vstack(list_of_expanded_array)
print(images.shape)
features = preprocess_input(images)

IMG_SIZE = (224,224)
IMG_SHAPE = IMG_SIZE + (3,)
mobv2= mobilenet_v2.MobileNetV2(input_shape=IMG_SHAPE, alpha=1.0, 
                                       include_top=False, 
                                       weights='imagenet')

'''Fine-Tune the pre-trained model'''
preprocess_input = tf.keras.applications.mobilenet_v2.preprocess_input
data_augmentation = tf.keras.Sequential([
  tf.keras.layers.experimental.preprocessing.RandomFlip('horizontal'),
  tf.keras.layers.experimental.preprocessing.RandomRotation(0.2),
])
global_average_layer = tf.keras.layers.GlobalAveragePooling2D()
prediction_layer = tf.keras.layers.Dense(1)


inputs = tf.keras.Input(shape=(224, 224, 3))
x = data_augmentation(inputs)
x = preprocess_input(x)
x = mobv2(x, training=False)
x = global_average_layer(x)
x = tf.keras.layers.Dropout(0.001)(x)
outputs = prediction_layer(x)

'''model used to predict features'''
model = tf.keras.Model(inputs,outputs)
img_features = model.predict(features)
print(img_features)

'''get the list storing image file names in one directory'''
img_list = list()
basepath = '/Users/wusongyuan/Desktop/test/test_dir/testsub_dir'
for entry in os.listdir(basepath):
    img_list.append(entry)
for i in img_list:
    print(i)

'''get similarity score'''
print('============ algorithm predict features =========')

print(img_features)
print("Our image has %i features:" %img_features.size)
cosSimilarities = sk.cosine_similarity(img_features)
cos_similarities_df = pd.DataFrame(cosSimilarities, 
                                           columns=img_list[:len(img_list)-1],
                                           index=img_list[:len(img_list)-1])
print(cos_similarities_df.head())

'''recommend top five similar images in our systen'''
print("-----------------------------------------------------------------------")
print("original manga:")

given_img = 'image-15.jpg'
original = img = PImage.open('/Users/wusongyuan/Desktop/image-dataset/test/1/image-15.jpg')
plt.imshow(original)
plt.show()

print("-----------------------------------------------------------------------")
print("most similar manga:")

nb_closest_images = 5
closest_imgs = cos_similarities_df[given_img].sort_values(ascending=False)[1:nb_closest_images+1].index
closest_imgs_scores = cos_similarities_df[given_img].sort_values(ascending=False)[1:nb_closest_images+1]

for i in range(0,len(closest_imgs)):
    original = PImage.open('/Users/wusongyuan/Desktop/test/test_dir/testsub_dir/' + closest_imgs[i])
    plt.imshow(original)
    plt.show()
    print("similarity score : ",closest_imgs_scores[i])







