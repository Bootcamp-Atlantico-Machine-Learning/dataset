import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from glob import glob
import cv2

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

# pegue uma imagem na pasta src\data\Dataset_BUSI_with_GT\benign e mostre-a

img = cv2.imread('src/data/Dataset_BUSI_with_GT/benign/benign (1).png')

# Lendo em RGB
rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# Lendo em HSV
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# Lendo em YCrCb
ycrcb = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)

# Lendo em L*U*V
luv = cv2.cvtColor(img, cv2.COLOR_BGR2Luv)

plot_image([rgb, hsv, ycrcb, luv], ['RGB', 'HSV', 'YCrCb', 'Luv'])

# gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# # normalized_image = gray_image / 255.0

# blurred_image = cv2.blur(gray_image, (4, 4))

# enhaced_image = cv2.convertScaleAbs(blurred_image, alpha=1.5, beta=0)

# mean_value = int(np.mean(blurred_image))

# print(mean_value)

# # use otsu para binarizar a imagem usando o valor minimo 

# otsu_threshold, otsu_image = cv2.threshold(blurred_image, mean_value, 255, cv2.THRESH_BINARY)

# rgb_image = cv2.cvtColor(otsu_image, cv2.COLOR_GRAY2RGB)


# plot_image([gray_image, otsu_image])


# # print("max tom de cinza", normalized_image.max())
# # print("mean tom de cinza", normalized_image.mean())
# # print("min tom de cinza", normalized_image.min())

# # plt.subplot(1, 2, 1)
# # plt.imshow(gray_image, cmap='gray')
# # plt.title("Imagem cinza")

# # plt.subplot(1, 2, 2)
# # plt.imshow(normalized_image, cmap='gray')
# # plt.title("Imagem normalizada")

# # plt.show()

# # def rgd_to_gray(image):
# #     R = 0.2989
# #     G = 0.5870
# #     B = 0.1140
# #     return np.dot(image[..., :3], [R, G, B])

# # gray_image = rgd_to_gray(img)

# # plt.subplot(1, 2, 1)
# # plt.imshow(img)
# # plt.title("Imagem RGB")

# # plt.subplot(1, 2, 2)
# # plt.imshow(gray_image, cmap='gray')
# # plt.title("Imagem cinza")

# # plt.show()

# blurred_image = cv2.blur(gray_image, (4, 4))

# # plt.subplot(1, 2, 1)
# # plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
# # plt.title("Imagem gray")

# # plt.subplot(1, 2, 2)
# # plt.imshow(cv2.cvtColor(blurred_image, cv2.COLOR_BGR2RGB))
# # plt.title("Imagem suavizada")

# # plt.show()






# # b, g, r = cv2.split(image)

# # plt.figure(figsize=(10, 5))
# # plt.subplot(131)
# # plt.imshow(r, cmap='gray')
# # plt.title("Canal R")

# # plt.subplot(132)
# # plt.imshow(g, cmap='gray')
# # plt.title("Canal G")

# # plt.subplot(133)
# # plt.imshow(b, cmap='gray')
# # plt.title("Canal B")

# # plt.tight_layout()
plt.show()

# Filtro Blur: 
# O blur é o filtro de média.
# Para aplicar esse filtro em uma imagem basta definir o tamanho do kernel e passar como parâmetro para a função cv2.blur.
filter_blur = cv2.blur(img, ksize=(3,3))

# --------------------------------------

# Filtro GaussianBlur: usa um kernel em forma de Gaussiana. Isso é como um cone no centro do kernel, os valores vão decaindo a medida que afasta.
# O kernel precisa ter dimensões ímpares para manter a simetria da Gaussiana.
# O parâmetro sigmaX permite definir o desvio padrão na direção x, (existem sigmaY, se não especificado sigmaY=sigmaX), quando o valor é 0 o sigmaX vai ser calculado em função do tamanho do kernel.
gaugaussian = cv2.GaussianBlur(src=img,ksize=(13,13),sigmaX=0)

# --------------------------------------

# Filtro medianBlur
# A principal característica do filtro medianBlur é que o pixel da nova imagem é sempre um valor de pixel da imagem anterior. 
# Isso não causa o efeito de suavização de borda como o filtro blur e GaussianBlur.
# O tamanho do kernel para medianBlur deve ser um valor ímpar
# O medianBlur é o filtro mais eficaz para remoção de ruído, porém pode custar computacionalmente 8 vezes em relação do blur. 
median=cv2.medianBlur(img, 13)

# --------------------------------------

# Filtro Bilateral
# O filtro bilateral também utiliza uma Gaussiana, porem tem uma pequena diferença. 
# No filtro gaussianoBlur é espacial, os seja ele calcula uma média ponderada dos pixels vizinhos. 
# A Gaussiana do filtro bilateral é uma função da intensidade, somente os pixels com intensidade parecida é considerado para o desfoque.
# d=13 é o tamanho do kernel. sigmaColor e sigmaspace é o desvio padrão para os kernel no espaço de cor e no espaço 2D da imagem.
bilateral = cv2.bilateralFilter(img, d=13, sigmaColor=75, sigmaSpace=75)


# Filtro de média adaptativo
# O filtro de média adaptativo é um filtro não linear que preserva as bordas.
# O filtro de média adaptativo calcula a média dos pixels vizinhos, mas o tamanho do kernel é variável, ou seja, o tamanho do kernel depende do desvio padrão.
# O filtro de média adaptativo é mais eficaz para remover ruídos de imagens com variação de iluminação.
# O filtro de média adaptativo é mais lento que os outros filtros.
adaptive = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)

plot_image([img, filter_blur, gaugaussian, median, bilateral], ['Original', 'Blur', 'Gaussian', 'Median', 'Bilateral'])

