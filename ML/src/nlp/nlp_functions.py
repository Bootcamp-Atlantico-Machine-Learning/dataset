# importando bibliotecas necessárias
import tensorflow as tf
from sklearn.model_selection import train_test_split
import numpy as np
import matplotlib.pyplot as plt
from keras import layers, models
import pathlib
import os
import cv2
import string
from keras.metrics import Accuracy, Precision, Recall
from sklearn.metrics import classification_report, accuracy_score
from sklearn.metrics import confusion_matrix, precision_score, recall_score
from sklearn.metrics import f1_score
import seaborn as sns
import pandas as pd
from sklearn.preprocessing import MinMaxScaler


class readDataset:
    def __init__(self, datasetpath, imageShape):
        self.datasetpath = datasetpath
        self.imageShape = imageShape

    def imagesPath(self, folder, name):
        images = list(pathlib.Path(os.path.join(self.datasetpath,folder)).glob('*{}.*'.format(name)))
        return images
    
    def readImages(self, images, channels):
        listImages = []
        images = np.sort(images)
        for image in images:
            image = tf.io.read_file(str(image))
            image = tf.image.decode_png(image, channels = channels)
            image = tf.image.resize(image, self.imageShape)
            image/= 255
            listImages.append(image)
        return listImages
    
    def allDataset(self, label):
        images = self.readImages(self.imagesPath(label, name = ')'), channels = 3)
        masks = np.array(self.readImages(self.imagesPath(label, name = 'mask'), channels = 1))
        masks = (masks >= 0.5).astype('int32')
        return np.array(images), masks
    
    def finalDataset(self, labels):
        images_benign, masks_benign = self.allDataset(labels[0])
        images_malignant, masks_malignant = self.allDataset(labels[1])
        images_normal, masks_normal = self.allDataset(labels[2])
        images = np.vstack([images_benign, images_malignant, images_normal])
        masks = np.vstack([masks_benign, masks_malignant, masks_normal])
        labels = np.hstack([np.ones(shape = (len(images_benign),))*0,
                           np.ones(shape = (len(images_malignant), ))*1,
                           np.ones(shape = (len(images_normal), ))*2])
        return images, masks, labels
    
    def dataAugmentation(self, images, masks, labels):
        imagesupdate = []
        masksupdate = []
        labelsupdate = []
        for image, mask, label in zip(images, labels, masks):
          for aug in range(5):
            imageup = image
            maskup = mask
            if aug == 0:
              imageup = image
              maskup = mask
            elif aug == 1:
              imageup = tf.image.adjust_contrast(imageup, contrast_factor = 2)
            elif aug == 2:
              imageup = tf.image.adjust_brightness(imageup, delta = 0.3)
            elif aug == 3:
              imageup = tf.image.flip_left_right(imageup)
              maskup = tf.image.flip_left_right(maskup)
            else:
              imageup = cv2.GaussianBlur(imageup,(5, 5),0)
            imagesupdate.append(imageup), masksupdate.append(maskup), labelsupdate.append(label)
        return np.array(imagesupdate), np.array(masksupdate), np.array(labelsupdate)
    
def showImagesWithMask(images, masks, labels):
    plt.figure(figsize = (12, 12))
    for i in range(len(images)):
        plt.subplot(8, 8, (i + 1))
        plt.imshow(images[i])
        plt.imshow(masks[i], alpha = 0.3, cmap = 'jet')
        plt.title(labels[i])
    plt.legend()

# treinamento da CNN
def convolution(inputs, padding, strides, filter, kernel_size):
    x = inputs

    y = layers.Conv2D(filter, kernel_size = 1, padding = padding,
                     strides = strides,
                     kernel_regularizer = tf.keras.regularizers.L2(0.001))(x)

    x = layers.Conv2D(filter, kernel_size = kernel_size, padding = padding,
                     strides = strides,
                     kernel_regularizer = tf.keras.regularizers.L2(0.001))(y)

    x = layers.BatchNormalization()(x)

    x = layers.Activation('relu')(x)

    x = layers.Conv2D(filter, kernel_size = kernel_size, padding = padding,
                     strides = strides,
                     kernel_regularizer = tf.keras.regularizers.L2(0.001))(x)

    x = layers.BatchNormalization()(x)

    x = layers.add([x, y])

    x = layers.Activation('relu')(x)

    return x

def encoder(inputs, filter):

    correlation = convolution(inputs, padding = 'same', strides = 1, filter = filter, kernel_size = 5)

    downsample = layers.AveragePooling2D()(correlation)

    return correlation, downsample

def decoder(inputs, skip_connection, filter):
    upsample = layers.Conv2DTranspose(filter, 5, padding = 'same', strides = 2, kernel_regularizer = tf.keras.regularizers.L2(0.001))(inputs)

    upsample = layers.Activation('relu')(upsample)

    upsample = layers.BatchNormalization()(upsample)

    connection = layers.average([upsample, skip_connection])

    correlation = convolution(connection, padding = 'same', strides = 1, filter = filter, kernel_size = 5)

    return correlation

def readModel(model_path):
    try:
      model = tf.keras.models.load_model(model_path)

      print('Modelo carregado com sucesso!')

    except:
      raise Exception('Erro ao carregar o modelo!')
    
    return model