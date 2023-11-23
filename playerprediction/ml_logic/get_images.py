import os
import numpy as np
from PIL import Image

def get_players_images():
<<<<<<< HEAD:get_images.py
    
    directory_path = "raw_data/faces"
    img_folders = os.listdir(directory_path)
    labels = [' '.join(folder.replace('Man.', '').replace('Real', '').split()[:-1]) for folder in img_folders]
        
    img_label_dict = {'image': [], 'name': []}
    
    for img_folder, label in zip(img_folders, labels):
        if img_folder != '.DS_Store':
            directory_path = f"raw_data/faces/{img_folder}"
            img_files = os.listdir(directory_path)

            # print(f'{img_folder}: {len(img_files)}')

            for img_file in img_files:
                try:
                    image_path = f"raw_data/faces/{img_folder}/{img_file}"

                    image_pil = Image.open(image_path)
                    image_np = np.array(image_pil)

                    img_label_dict['image'].append(image_np)
                    img_label_dict['name'].append(label)
                    
                except:
                    pass
            
=======
    img_label_dict = {'image': [], 'name': []}

    # Get the list of all folder names inside the "faces" folder
    directory_path = "raw_data/faces"
    img_folders = os.listdir(directory_path)

    # Preprocess labels (players names)
    labels = [' '.join(folder.replace('Man.', '').replace('Real', '').split()[:-1]) for folder in img_folders]

    # Get the list of png files inside each folder
    for img_folder, label in zip(img_folders, labels):
        directory_path = f"raw_data/faces/{img_folder}"
        img_files = os.listdir(directory_path)

        # Loop through list of png files, load them, convert to array and add to a dictionary
        for img_file in img_files:
            try:
                image_path = f"raw_data/faces/{img_folder}/{img_file}"
                image_tf = load_img(image_path)
                image_np = img_to_array(image_tf)

                img_label_dict['image'].append(image_np)
                img_label_dict['name'].append(label)
            except:
                pass

>>>>>>> master:playerprediction/ml_logic/get_images.py
    return img_label_dict
