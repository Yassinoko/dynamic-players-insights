"""
This model uses the pre-trained CNN MobileNetV2 available on Keras
https://keras.io/api/applications/mobilenet/#mobilenetv2-function
"""

# Import model, functions and libraries
from keras.applications import MobileNetV2
from keras import layers, models, utils
from sklearn.model_selection import train_test_split
import pandas as pd
import os
import requests
import time
import pandas as pd
from urllib.parse import quote
from selenium import webdriver
import sys
import numpy as np

# setting file path
sys.path.append(os.path.join(os.path.dirname("dynamic-players-insights"), "playerprediction"))

# import get_player_images function
from ml_logic.get_images import get_players_images
from ml_logic.class_preprocessing import preprocessing_classes
from ml_logic.image_preprocessing import processing_images

# load images
player_images = get_players_images()

# create dataframe
df = pd.DataFrame(player_images)

# preprocessing the images and labels
X, y = processing_images(player_images)
# encoding the labels
y = preprocessing_classes(y)

# train, test split with shuffle
# we do not use stratify (possible improvement)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, shuffle=True)


def load_model():
    "This function loads the pre-trained model"
    model = MobileNetV2(
        input_shape=X_train.shape[1:],
        alpha=1.0,
        include_top=False,
        weights="imagenet",
        input_tensor=None,
        pooling=None,
        classes=y_train.shape[-1],
        classifier_activation="softmax",
        )
    return model


def set_nontrainable_layers(model):
    "This function sets the pre-trained model layers to non-trainable"
    model.trainable = False
    return model


def add_last_layers(model):
    """ This function takes a pre-trained model,
    set its parameters as non-trainable,
    and adda additional trainable layers on top"""
    base_model = set_nontrainable_layers(model)
    flatten_layer = layers.Flatten()
    dense_layer = layers.Dense(500, activation='relu')
    prediction_layer = layers.Dense(y_train.shape[-1], activation='softmax')

    model = models.Sequential([
        base_model,
        flatten_layer,
        dense_layer,
        prediction_layer
    ])
    return model

# load and initialize the model
model = load_model()
model = add_last_layers(model)

# Define early stopping
from keras.callbacks import EarlyStopping
es = EarlyStopping(patience=2, restore_best_weights=True)

# fit model
history = model.fit(
    X_train,
    y_train,
    validation_split = 0.2,
    epochs = 5,
    batch_size = 32,
    verbose = 1,
    callbacks = [es],
    )

# evaluate model
model.evaluate(X_test, y_test)
