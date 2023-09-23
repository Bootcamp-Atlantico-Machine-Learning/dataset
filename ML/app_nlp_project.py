from src.nlp.nlp_functions import *

def main():
    datasetpath = 'src\data\Dataset_BUSI_with_GT'
    datasetObject = readDataset(datasetpath, [128, 128])
    images, masks, labels = datasetObject.finalDataset(['benign', 'malignant', 'normal'])



    images, masks, labels = datasetObject.dataAugmentation(images, labels, masks)



    np.unique(labels, return_counts = True)

    np.unique(masks, return_counts = True)

    # Dividindo o dataset em imagens de treino e imagens de teste
    randomIndexs = np.random.randint(0, len(images), size = (len(images), ))
    images = images[randomIndexs]
    masks = masks[randomIndexs]
    labels = labels[randomIndexs]

    valid = int(len(images)*0.15)

    trainDataset = [
    images[:images.shape[0] - valid],
    masks[:images.shape[0] - valid],
    labels[:images.shape[0] - valid]
    ]

    validDataset = [
    images[images.shape[0] - valid:],
    masks[images.shape[0] - valid:],
    labels[images.shape[0] - valid:]
    ]

    scaler = MinMaxScaler()
    curr = layers.Flatten()(trainDataset[0])
    scaler.fit(curr)
    trainImages = scaler.transform(curr)
    validImages = scaler.transform(layers.Flatten()(validDataset[0]))
    trainDataset[0] = np.reshape(trainImages, (trainDataset[0].shape[0], 128, 128, 3))
    validDataset[0] = np.reshape(validImages, (validDataset[0].shape[0], 128, 128, 3))
    trainDataset[0].shape, validDataset[0].shape

    input = layers.Input(shape = (128, 128, 3))

    filter = 16

    corr1, downsample1 = encoder(input, filter)

    corr2, downsample2 = encoder(downsample1, filter*2)

    corr3, downsample3 = encoder(downsample2, filter*4)

    corr4, downsample4 = encoder(downsample3, filter*8)

    downsample4 = convolution(downsample4, padding = 'same', strides = 1, filter = filter*8, kernel_size = 5)

    features_vector_1 = layers.GlobalAveragePooling2D()(downsample4)

    features_vector_2 = layers.Flatten()(downsample4)

    features_vector_2 = layers.Dropout(0.7)(features_vector_2)

    features_vector_1 = layers.Dropout(0.5)(features_vector_1)

    encoder_x = layers.Dense(64, name = 'latent_space', kernel_regularizer = tf.keras.regularizers.L2(0.001))(features_vector_1)

    x = layers.Dense(downsample4.shape[1]*downsample4.shape[2]*downsample4.shape[3], kernel_regularizer = tf.keras.regularizers.L2(0.001))(encoder_x)

    x = layers.Reshape((downsample4.shape[1], downsample4.shape[2], downsample4.shape[3]), name = 'reshape')(x)

    x = layers.BatchNormalization()(x)

    x = layers.Dropout(0.4)(x)

    decoder_corr1 = decoder(x, corr4, filter*8)

    decoder_corr2 = decoder(decoder_corr1, corr3, filter*4)

    decoder_corr3 = decoder(decoder_corr2, corr2, filter*2)

    decoder_corr4 = decoder(decoder_corr3, corr1, filter)

    output = layers.Conv2DTranspose(1, 5, padding = 'same', strides = 1)(decoder_corr4)

    output = layers.Activation('sigmoid', name = 'UNET')(output)

    labelOutput = layers.Dense(32, activation = 'relu')(features_vector_2)

    labelOutput = layers.BatchNormalization()(labelOutput)

    labelOutput = layers.Dropout(0.5)(labelOutput)

    labelOutput = layers.Dense(16, activation = 'relu')(labelOutput)

    labelOutput = layers.BatchNormalization()(labelOutput)

    labelOutput = layers.Dropout(0.5)(labelOutput)

    labelOutput = layers.Dense(1, name = 'label')(labelOutput)

    m = models.Model(inputs = input, outputs = [output, labelOutput])

    m.compile(loss = [tf.keras.losses.BinaryFocalCrossentropy(), 'mae'],
            optimizer = tf.keras.optimizers.Adam(learning_rate = 0.00001),
            metrics = ['accuracy', Precision(name = 'precision'), Recall(name = 'recall')]
            )
    m.summary()

    history = m.fit(trainDataset[0], [trainDataset[1], trainDataset[2]], epochs = 600,
                validation_data = (validDataset[0], [validDataset[1], validDataset[2]]),
                batch_size = 64, callbacks = [
                    tf.keras.callbacks.EarlyStopping(patience = 12, monitor = 'val_loss',
                                                    mode = 'min', restore_best_weights = True),
                ])

    m.save('/content/modeloTreinado')

if __name__ == "__main__":
    main()