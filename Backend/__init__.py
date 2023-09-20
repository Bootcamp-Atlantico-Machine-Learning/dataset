from flask import Flask, request
from flask import send_file
# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
from glob import glob
import cv2


app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload():
    # Obtém o arquivo de imagem do pedido HTTP
    img = request.files['image']

    # salva a imagem
    img.save('image.jpg')

    # Lê a imagem salva
    img = cv2.imread('image.jpg')

    # Converte a imagem para escala de cinza
    # img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Aplica o filtro de média
    # img = cv2.blur(img, (5, 5))

    # Salva a imagem
    cv2.imwrite('image.jpg', img)

    # # Retorna o arquivo de imagem como uma resposta HTTP
    return send_file('image.jpg')

if __name__ == '__main__':
    app.run(debug=True)