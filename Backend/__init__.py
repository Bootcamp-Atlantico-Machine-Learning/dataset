# from ..ML.src.nlp.nlp_functions import readModel
from flask import Flask, request
from flask import send_file
import numpy as np
from glob import glob
import tensorflow as tf
import cv2

def readModel(model_path):
    try:
        model = tf.keras.models.load_model(model_path)
        print('Modelo carregado com sucesso!')
    except:
      raise Exception('Erro ao carregar o modelo!')    
    return model

model = readModel('model')

app = Flask(__name__)

@app.route('/')
def verify():
    return 'Hello World!'

@app.route('/predictImage', methods=['POST'])
def predictImage():

    image = request.files['image']

    image.save('image.jpg')

    image = cv2.imread('image.jpg')

    image = cv2.resize(image, (128, 128))

    image = np.expand_dims(image, axis=0)

    image = image/255

    prediction, _ = model.predict(image)

    img = np.reshape(prediction, (128, 128))

    img = img*255

    img = img.astype('uint8')

    # Salve a imagem em um arquivo
    cv2.imwrite('img.png', img)

    # Envie o arquivo para o cliente
    return send_file('img.png', mimetype='image/png')

    

if __name__ == '__main__':
    app.run(debug=True)