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
    tempo_inicio = time.time() # pega o tempo de início

    print("Montando o dataframe...")

    try:
        mascaras = sorted(glob(f"{CAMINHO}/*/*_mask.png"))
    except:
        raise Exception('Erro ao ler as mascaras, verifique o caminho informado')

    try:
        images = sorted(glob(f"{CAMINHO}/*/*).png"))
    except:
        raise Exception('Erro ao ler as imagens, verifique o caminho informado')
    
    df = pd.DataFrame(columns=['images', 'mascaras', 'classe', 'altura', 'largura'])

    try:
        for i in range(len(images)):    

            img = cv2.imread(images[i]) # lê a imagem

            altura, largura = img.shape[:2] # pega a altura e largura da imagem
            
            label = images[i].split('\\')[2].split(' ')[0] # pega o label

            df.loc[i] = [images[i], mascaras[i], label, altura, largura] # adiciona as informações no dataframe
    except:
        raise Exception('Erro ao montar o dataframe')

    tempo_fim = time.time()

    print(df.head())

    print("Dataframe montado com sucesso! Tempo de execução: {:.2F}s\n".format(tempo_fim - tempo_inicio)) # imprime o tempo de execução

    return df


def redimensiona_imagens(df, altura=None, largura=None):
    '''
    Redimensiona as imagens do dataframe
    Parâmetros:
    df (DataFrame) : Informe o dataframe
    altura (int) : Informe a altura
    largura (int) : Informe a largura
    '''
    tempo_inicio = time.time() # pega o tempo de início

    if altura == None:
        raise Exception('altura precisa ser informado')
    
    if largura == None:
        raise Exception('largura precisa ser informado')

    print("Redimensionando as imagens...")

    images_resized = []

    classe = []

    try:
        for i in range(len(df)):
            
            img = cv2.imread(df['images'][i]) # pega a imagem
            
            img = cv2.resize(img, (altura, largura)) # redimensiona a imagem
            
            images_resized.append(img) # adiciona a imagem redimensionada na lista
            
            classe.append(df['classe'][i]) # adiciona o label na lista
    except:
        raise Exception('Erro ao redimensionar as imagens, verifique o dataframe informado')

    df2 = pd.DataFrame(columns=['imagem_redimensionada', 'classe'])

    try:
        for i in range(len(images_resized)):
            df2.loc[i] = [images_resized[i], classe[i]] # adiciona as informações no dataframe
    except:
        raise Exception('Erro ao montar o dataframe das imagens redimensionadas')

    tempo_fim = time.time() # pega o tempo de fim

    print(df2.head())

    print("Imagens redimensionadas com sucesso! Tempo de execução: {:.2F}s\n".format(tempo_fim - tempo_inicio)) # imprime o tempo de execução

    return df2

def salva_imagens(df, caminho=None):
    '''
    Salva as imagens do dataframe
    Parâmetros:
    df (DataFrame) : Informe o dataframe
    caminho (str) : Informe o caminho onde deseja salvar as imagens
    '''
    tempo_inicio = time.time() # pega o tempo de início

    if caminho == None:
        raise Exception('caminho precisa ser informado')

    print("Salvando as imagens...")

    try:
        for i in range(len(df)):
            cv2.imwrite(f"{caminho}/{df['classe'][i]}_{i}.png", df['imagem_redimensionada'][i]) # salva as imagens
    except:
        raise Exception('Erro ao salvar as imagens, verifique o dataframe informado')

    tempo_fim = time.time() # pega o tempo de fim

    print("Imagens salvas com sucesso! Tempo de execução: {:.2F}s\n".format(tempo_fim - tempo_inicio)) # imprime o tempo de execução

    return df

