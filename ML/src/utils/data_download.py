import requests
import zipfile
import os

def download_data():

    LOGIN = "exemp@gmail.com"
    PASSWORD = "exemp123"

    if not os.path.exists('../data/Dataset_BUSI_with_GT'):
        # Especifica o link do arquivo zip
        LINK = "https://storage.googleapis.com/kaggle-data-sets/1209633/2021025/bundle/archive.zip?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=gcp-kaggle-com%40kaggle-161607.iam.gserviceaccount.com%2F20230904%2Fauto%2Fstorage%2Fgoog4_request&X-Goog-Date=20230904T182143Z&X-Goog-Expires=259200&X-Goog-SignedHeaders=host&X-Goog-Signature=89c9344d630ffd4face6d22441d3e094b56c36a7b1089918a2201da0dfc27b91964d6c41703345d5fbb739358368ec4aed129974d43b69a870e5283417fcdfbd54e522d218883253ee4212ae4e1c050b0cd330444db8dd80185568eb203cdf54458d5db1e65dec08b21c12f401008d8be3057a1240dd2c27345784f8a7e4dc6675786653d79dafc4ed918cac3a53dbc45c80ad2b52de19332ad0abf3dbdeb83384cdeebf3ac60cd0f25a00b1883422e2f96d8e95892366ec1c2018cc8f39ef70afaa53097cdce168781892b746840cd544c6f37427f14273b903cfd523a15b38f50c7f3c2d91b217d4015ee098ee5b299fa37c40780f5804936d6f00fd7bbf78"

        # Especifica o caminho do arquivo zip
        CAMINHO = "../data"

        # Baixa o arquivo zip para o diretório atual
        r = requests.get(LINK, stream=True)
        with open(CAMINHO + "arquivo.zip", "wb") as f:
            for chunk in r.iter_content(chunk_size=1024):
                f.write(chunk)

        # # espera o arquivo ser baixado
        # while not os.path.exists(CAMINHO + "arquivo.zip"):
        #     pass

        # Extrai os arquivos do arquivo zip
        with zipfile.ZipFile(CAMINHO + "arquivo.zip", "r") as zip_file:
            zip_file.extractall(CAMINHO)

        # Apaga o arquivo zip
        os.remove(CAMINHO + "arquivo.zip")

def main():
    download_data()

if __name__ == "__main__":
    main()