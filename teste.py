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

class lerDataSet:

    def __init__(self, caminho, dimensao):
        '''
        caminho (str) : caminho do dataset
        dimensao (tuple) : dimensão das imagens        
        '''
        self.caminho = caminho # caminho do dataset

        self.dimensao = dimensao # dimensão das imagens
        
    def imagesPath(self, pasta, name):
        '''
        pasta (str) : pasta do dataset
        name (str) : nome da imagem
        '''
        images = list(pathlib.Path(os.path.join(self.caminho,pasta)).glob('*{}.*'.format(name))) # lista de imagens

        return images

    def lerImagens(self, images, channels):

        listaDeImagens = [] # lista de imagens

        images = np.sort(images) # ordena as imagens

        for image in images:

            image = tf.io.read_file(str(image)) # lê a imagem

            image = tf.image.decode_png(image, channels = channels) # decodifica a imagem

            image = tf.image.resize(image, self.dimensao) # redimensiona a imagem

            image /= 255 # normaliza a imagem

            listaDeImagens.append(image) # adiciona a imagem na lista
            
        return listaDeImagens

    def datasetCompleto(self, label):
        '''
        label (str) : label da imagem        '''

        images = self.lerImagens(self.imagesPath(label, name = ')'), channels = 3) # lê as imagens

        masks = np.array(self.lerImagens(self.imagesPath(label, name = 'mask'), channels = 1)) # lê as máscaras

        masks = (masks >= 0.5).astype('int32') # binariza as máscaras

        return np.array(images), masks # retorna as imagens e as máscaras
    
    def datasetFinal(self, classificacao):
        '''
        classificacao (list) : lista com as classificações
        '''
        images_benign, masks_benign = self.datasetCompleto(classificacao[0]) # lê as imagens e as máscaras benignas

        images_malignant, masks_malignant = self.datasetCompleto(classificacao[1]) # lê as imagens e as máscaras malignas

        images_normal, masks_normal = self.datasetCompleto(classificacao[2]) # lê as imagens e as máscaras normais

        images = np.vstack([images_benign, images_malignant, images_normal]) # empilha as imagens

        masks = np.vstack([masks_benign, masks_malignant, masks_normal]) # empilha as máscaras

        classificacao = np.hstack(
           [np.ones(shape = (len(images_benign),))*0, np.ones(shape = (len(images_malignant), ))*1, np.ones(shape = (len(images_normal), ))*2]
        ) # cria a classificação

        return images, masks, classificacao
    
    def dataAugmentation(self, images, masks, classificacao):

        imagesupdate = [] # lista de imagens

        masksupdate = [] # lista de máscaras

        classificacaoupdate = [] # lista de classificação

        for image, mask, label in zip(images, classificacao, masks):
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
            imagesupdate.append(imageup), masksupdate.append(maskup), classificacaoupdate.append(label)
        return np.array(imagesupdate), np.array(masksupdate), np.array(classificacaoupdate)

datasetpath = '/kaggle/input/breast-ultrasound-images-dataset/Dataset_BUSI_with_GT'
datasetObject = lerDataSet(datasetpath, [128, 128])
images, masks, labels = datasetObject.finalDataset(['benign', 'malignant', 'normal'])



images, masks, labels = datasetObject.dataAugmentation(images, labels, masks)



np.unique(labels, return_counts = True)

np.unique(masks, return_counts = True)

np.min(images), np.max(images)



def showImagesWithMask(images, masks, labels):
    plt.figure(figsize = (12, 12))
    for i in range(len(images)):
        plt.subplot(8, 8, (i + 1))
        plt.imshow(images[i])
        plt.imshow(masks[i], alpha = 0.3, cmap = 'jet')
        plt.title(labels[i])
    plt.legend()

showImagesWithMask(images[:64], masks[:64], labels[:64])



