'''
This model.py is used to build and load the model only once at the start of the bento-service container.

'''

import tensorflow as tf
from tensorflow import keras


def build_and_load_model(weights_path):
    
    ## Define the model architecture from colab
    input_shape = (259, 160, 1)
    ## create model
    model = keras.Sequential()

    ## 1st conv layer
    model.add(keras.layers.Conv2D(32, (3,3), activation = 'relu', input_shape = input_shape))
    model.add(keras.layers.MaxPool2D((3,3), strides =(2,2), padding ='same'))
    model.add(keras.layers.BatchNormalization())

    ## 2nd conv layer
    model.add(keras.layers.Conv2D(32, (3,3), activation = 'relu', input_shape = input_shape))
    model.add(keras.layers.MaxPool2D((3,3), strides =(2,2), padding ='same'))
    model.add(keras.layers.BatchNormalization())

    ## 3rd conv layer
    model.add(keras.layers.Conv2D(32, (2,2), activation = 'relu', input_shape = input_shape))
    model.add(keras.layers.MaxPool2D((2,2), strides =(2,2), padding ='same'))
    model.add(keras.layers.BatchNormalization())

    ## flatten the output and feed it into dense layer

    model.add(keras.layers.Flatten())
    model.add(keras.layers.Dense(64, activation = 'relu'))
    model.add(keras.layers.Dropout(0.3))


    ## output layer
    model.add(keras.layers.Dense(10, activation = 'softmax'))

    # Load weights
    model.load_weights(weights_path)

    return model
