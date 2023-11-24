import face_recognition as fg
import numpy as np
import pandas as pd
import cv2
import matplotlib.pyplot as plt
import os
import matplotlib.pyplot as ple
from data_processing.get_images import get_players_images

""" 55% recall when training on high-quality image
and testing on a blurr images

STARTS FROM face_recognition_model, LINE 58

PUT YOUR DETECTED FACE (ARRAY!!!!) INTO THAT FUNCTION AND YOU WILL GET THE NAME OF THE PLAYER

"""

def train_model():
    directory_path = "../../raw_data/faces"
    img_folders = os.listdir(directory_path)

    shorten_img_folders = []

    for folder in img_folders:
        if 'Real Madrid' in folder or 'Chelsea' in folder:
            shorten_img_folders.append(folder)

    img_label_dict = {'encoded_face': [], 'label': []}
    labels = [folder for folder in shorten_img_folders]

    for img_folder, label in zip(shorten_img_folders, labels):
        directory_path = f"../../raw_data/faces/{img_folder}"
        img_files = os.listdir(directory_path)

        try:
            ind = 0
            while True:
                image_path = f"../../raw_data/faces/{img_folder}/{img_files[ind]}"

                image = fg.load_image_file(image_path)

                if fg.face_encodings(image) == []:
                    ind += 1

                else:

                    img_label_dict['encoded_face'].append(fg.face_encodings(image)[0])
                    img_label_dict['label'].append(label)

                    break
        except:
            print('Empty folder')


    train_data = pd.DataFrame(img_label_dict)
    return train_data


def face_recognition_model(test_image): # passing image into function

    train_data = train_model()

    test_image_encoded = np.array(fg.face_encodings(test_image))

    ind = 0
    for train_image in list(train_data['encoded_face']):
        if fg.compare_faces([train_image], test_image_encoded)[0]:
            return ' '.join(train_data['label'][ind].replace('Man.', '').replace('Real', '').split()[:-1])
        ind += 1



# print(face_recognition_model(fg.load_image_file('../../raw_data/faces/Benzema Real Madrid/Benzema Real Madrid_1.jpg')))
