import requests
import zipfile
import os

def download_data():

    LOGIN = "exemp@gmail.com"
    PASSWORD = "exemp123"

    if not os.path.exists('src/data/Dataset_BUSI_with_GT'):
        # Especifica o link do arquivo zip
        LINK = "https://storage.googleapis.com/kaggle-data-sets/1209633/2021025/bundle/archive.zip?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=gcp-kaggle-com%40kaggle-161607.iam.gserviceaccount.com%2F20230920%2Fauto%2Fstorage%2Fgoog4_request&X-Goog-Date=20230920T170025Z&X-Goog-Expires=259200&X-Goog-SignedHeaders=host&X-Goog-Signature=0d5bc2b73fe3f0dc9d1c3d3fc07545da02406ca262e30e499e813a98e3e2d8cc3ca2ed174ba10f704c4e054ca45517f25acd5ff1a4841d58601f4d94a9c82e1c7683477712e24bbf11d5e00022f9adc794421374c49a3ec35559d3eb2084556b74be6f283cb5d2c9d38f038c7a805caca05e59bf31f9a740f0eeb91335539284102cc49ec9e307c371e332a114c3de4ac42233366286b9136159599d6962de30932cdbfd5bd7a24326dcacb2c7f825a8ebcdd2fd1e4f311d3366f2449f93092bcc7a46faa2b923f85c82b2dc91ecb28d26e2a711579584de33d359c6131f4c6b5db1c562e1315c6d422dfe99976c0b24701974505d3bc20c82a8ccbe7ed8f754"

        # Especifica o caminho do arquivo zip
        CAMINHO = "src/data"

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