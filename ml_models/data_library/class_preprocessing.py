from sklearn.preprocessing import LabelEncoder
import numpy as np
from keras.utils import to_categorical


def preprocessing_classes(y):

    """ This function takes labels (classes) from image_processing.py output and returns preprocessed y's values which are ready to be used to train the model """


    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(np.array(y))

    y_cat = to_categorical(y=y_encoded)

    return y_cat
