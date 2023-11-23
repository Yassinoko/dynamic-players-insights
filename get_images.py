def get_players_images():
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

    return img_label_dict
