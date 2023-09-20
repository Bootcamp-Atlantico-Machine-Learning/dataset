import numpy as np

from app_pdi_project import monta_dataframe, resize_images, save_images


def main():
    df = monta_dataframe('src/data/Dataset_BUSI_with_GT')
    
    # pd
    altura_media = int(np.mean(df['height']))
    largura_media = int(np.mean(df['width']))

    print(altura_media, largura_media)


if __name__ == "__main__":
    main()