import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from glob import glob
import cv2
import os
import time

def plot_image(img, title=None, height=5, width=5):
    plt.figure(figsize=(height, width))
    if type(img) == list:
        for i in range(len(img)):
            plt.subplot(1, len(img), i+1)
            plt.imshow(img[i], cmap='gray')
            if title:
                plt.title(title[i])
    else:
        plt.imshow(img, cmap='gray')
    plt.show()

def plot_histogram(img, title=None, height=5, width=5):
    plt.figure(figsize=(height, width))
    if type(img) == list:
        for i in range(len(img)):
            plt.subplot(1, len(img), i+1)
            plt.hist(img[i].ravel(), 256,
             [0, 256])
            if title:
                plt.title(title[i])
    else:
        plt.hist(img.ravel(), 256, [0, 256])
    plt.show()


def monta_dataframe(CAMINHO):
    '''
    Retorna um DataFrame com as informações do dataset
    Parâmetro:
    pasta (str) : Informe o caminho até a pasta 'Dataset_BUSI_with_GT'
    '''
    tempo_inicio = time.time()
    print("Montando o dataframe...")

    masks = sorted(glob(f"{CAMINHO}/*/*_mask.png"))
    images = sorted(glob(f"{CAMINHO}/*/*).png"))

    df = pd.DataFrame(columns=['images', 'masks', 'labels', 'height', 'width'])

    for i in range(len(images)):    

        # lê a imagem
        img = cv2.imread(images[i])
        # pega a altura e largura da imagem
        height, width = img.shape[:2]
        # pega o label
        label = images[i].split('\\')[2].split(' ')[0]
        # adiciona as informações no dataframe
        df.loc[i] = [images[i], masks[i], label, height, width]

    tempo_fim = time.time()

    print(df.head())

    print("Dataframe montado com sucesso! Tempo de execução: {:.2F}s\n".format(tempo_fim - tempo_inicio))

    return df

    




def resize_images(df, height=None, width=None):

    if height == None:
        raise Exception('height precisa ser informado')
    if width == None:
        raise Exception('width precisa ser informado')

    print("resize images")

    # lista com as imagens redimensionadas
    images_resized = []
    labels = []

    # percorre o dataframe
    for i in range(len(df)):
        # pega a imagem
        img = cv2.imread(df['images'][i])
        # redimensiona a imagem
        img = cv2.resize(img, (height, width))
        # adiciona a imagem redimensionada na lista
        images_resized.append(img)
        # adiciona o label na lista
        labels.append(df['labels'][i])

    # cria uma coluna no dataframe com as imagens redimensionadas
    df['images_resized'] = images_resized
    # cria uma coluna no dataframe com os labels
    df['labels'] = labels

    del images_resized
    del labels

    print("images resized")
    print(df.head())

    return df

def save_images(df):

    print("save images")
    i = 1
    # salva as imagens como png
    # for i in range(len(df)):
    image = cv2.cvtColor(df['images_resized'][i], cv2.COLOR_BGR2RGB)
    plot_image(image)
    cv2.imwrite('/src/data/Dataset_BUSI_with_GT_resized/' + df['labels'][i] + '/' + df['images'][i].split('\\')[2], image)

    print("images saved")
