import os
import numpy as np
from PIL import Image


def get_players_images(): # before using this function, make sure you have images in faces folder
    
    """ This function retrieves images from 'faces' folder, puts them in a dictionary and 
returns this dictionary """

    directory_path = "../../raw_data/faces"
    img_folders = os.listdir(directory_path)
    labels = [' '.join(folder.replace('Man.', '').replace('Real', '').split()[:-1]) for folder in img_folders]

    img_label_dict = {'image': [], 'name': []}

    for img_folder, label in zip(img_folders, labels):
        if img_folder != '.DS_Store':
            directory_path = f"../../raw_data/faces/{img_folder}"
            img_files = os.listdir(directory_path)

            # print(f'{img_folder}: {len(img_files)}')

            for img_file in img_files:
                try:
                    image_path = f"../../raw_data/faces/{img_folder}/{img_file}"

                    image_pil = Image.open(image_path)
                    image_np = np.array(image_pil)

                    img_label_dict['image'].append(image_np)
                    img_label_dict['name'].append(label)

                except:
                    pass

    return img_label_dict
