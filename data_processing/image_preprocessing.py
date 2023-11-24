from collections import Counter
import os
import pandas as pd
import numpy as np
from keras.layers import Resizing
from tqdm import tqdm
from PIL import Image 
# from data_processing.get_images import get_players_images


def processing_images(img_label_dict): # img_label_dict from get_images.py file

    """ This function takes the dictionary (from get_images.py), preprocess
each image and returns 2 separate variables:
prepocessed images and all labels (not only unique). Preprocessed images ready to be used as X.
Labels need to be preprocessed by class_preprocessing.py """

    shapes = [img.shape for img in list(img_label_dict['image'])]

    counter = Counter(shapes)
    most_common_item = max(counter, key=counter.get)

    height = most_common_item[0]
    width = most_common_item[1]

    resize = Resizing(height, width)

    preprocessed_img = []
    print(len(img_label_dict['image']))
    for img in tqdm(img_label_dict['image']):
        # try:
        img = Image.fromarray(img)
        img_resize = np.asarray(img.resize((129, 129)))
        preprocessed_img.append(img_resize)
#         except:
            
#             pass

    preprocessed_img = np.array(preprocessed_img)
    print(preprocessed_img.shape)

    try:
        print(shapes.index((408, 612)))
        print(shapes.index((418, 612)))
    except:
        pass

    total_labels = img_label_dict['name']
    
    try:
        del total_labels[shapes.index((408, 612))]
        del total_labels[shapes.index((418, 612))]
    except:
        pass

    return preprocessed_img, total_labels


# preprocessed_img, preprocessed_labels = processing_images(get_players_images())
# print('success')
