def get_players_images():
    img_label_dict = {'image': [], 'name': []}

    for img_folder, label in zip(img_folders, labels):
        directory_path = f"raw_data/faces/{img_folder}"
        img_files = os.listdir(directory_path)

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