from flask import Flask, request, render_template
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'backend/imagens'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def Resultado():
    return None

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    Resultado = 'o'
    if request.method == 'POST':
        if 'file' not in request.files:
            return "Escolha uma imagem raio x"

        file = request.files['file']

        if file.filename == '':
            return "Nome do arquivo vazio"

        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
        if '.' not in file.filename or file.filename.split('.')[-1].lower() not in allowed_extensions:
            return "Arquivo não é existe ou não foi baixado"

        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        if Resultado() != None:
            Resultado = Resultado()
        else:
            Resultado = 'espere'
            

        return render_template('upload.html', uploaded_image=file_path,Resultado=Resultado)

    return render_template('upload.html',Resultado=Resultado)

if __name__ == '__main__':
    app.run(debug=True)
