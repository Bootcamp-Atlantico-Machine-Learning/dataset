import numpy as np

from app_pdi_project import monta_dataframe, redimensiona_imagens, salva_imagens


def main():
    df = monta_dataframe('src/data/Dataset_BUSI_with_GT')
    
    # pd
    altura_media = int(np.mean(df['altura']))
    largura_media = int(np.mean(df['largura']))

    # redimensiona as imagens
    imagens_redimensionadas = redimensiona_imagens(df, altura_media, largura_media)

    # salva as imagens
    salva_imagens(imagens_redimensionadas, 'src/data/Dataset_BUSI_with_GT_redimensionado')

    


if __name__ == "__main__":
    main()