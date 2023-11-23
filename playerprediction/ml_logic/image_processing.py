from collections import Counter
import os
import pandas as pd
import numpy as np
from tensorflow.keras.layers import Resizing
from tqdm import tqdm
from get_images import get_players_images


def processing_images(img_label_dict): # img_label_dict from get_images.py file
    
    """ This function takes the dictionary (from get_images.py), preprocess 
each image and label (class) and returns 2 separate variables: 
prepocessed images and labels, which can then be used as X and y """
        
    shapes = [img.shape for img in list(img_label_dict['image'])]
    
    counter = Counter(shapes)
    most_common_item = max(counter, key=counter.get)
    
    height = most_common_item[0]
    width = most_common_item[1]

    resize = Resizing(height, width)

    preprocessed_img = []

    for img in tqdm(img_label_dict['image']):
        try:
            preprocessed_img.append(resize(img))
        except:
            pass  

    preprocessed_img = np.array(preprocessed_img)

    print(shapes.index((408, 612)))
    print(shapes.index((418, 612)))

    preprocessed_labels = img_label_dict['name']
    del preprocessed_labels[shapes.index((408, 612))]
    del preprocessed_labels[shapes.index((418, 612))]
    
    return preprocessed_img, preprocessed_labels
    
    
# preprocessed_img, preprocessed_labels = processing_images(get_players_images())
# print('success')