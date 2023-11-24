import os
import numpy as np
from PIL import Image
import face_recognition
import matplotlib.pyplot

faces_folder = "../../data_processing/raw_data/faces/"
cropped_faces_directory = "../../data_processing/raw_data/cropped_faces"


# Removing black and white pictures
def black_white(directory) :
    for filename in os.listdir(directory):
        if filename.endswith(".jpg") or filename.endswith(".jpeg"):
            file_path = os.path.join(directory, filename)

            img = Image.open(file_path)
            img = img.convert('RGB')  # Convert to RGB in case it's grayscale

            # Check if all pixels have similar RGB values
            is_black_white = all(
                all(180 <= value <= 240 for value in pixel)
                for pixel in img.getdata()
            )

            if is_black_white:
                os.remove(file_path)
                print(f"Removed {filename} as it was black and white.")


# Crop only the faces and save them in a new directory
def crop(input_directory, output_directory) :
     # Create the output directory if it doesn't exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    for filename in os.listdir(input_directory):
        if filename.endswith(".jpg") or filename.endswith(".jpeg"):
            file_path = os.path.join(input_directory, filename)

            # Load the image using face_recognition library
            image = face_recognition.load_image_file(file_path)
            face_locations = face_recognition.face_locations(image)

            # Check if a face is detected
            if len(face_locations) > 0:
                # Crop and save each face detected
                for idx, face_location in enumerate(face_locations):
                    top, right, bottom, left = face_location
                    face_image = image[top:bottom, left:right]
                    pil_image = Image.fromarray(face_image)
                    cropped_file_name = f"{os.path.splitext(filename)[0]}_face_{idx + 1}.jpg"
                    cropped_file_path = os.path.join(output_directory, cropped_file_name)
                    pil_image.save(cropped_file_path)
                    print(f"Face cropped and saved: {cropped_file_name}")
            else:
                print(f"No face detected in {filename}, skipping...")


# Delete weird pictures
def delete_face_images(directory):
    for filename in os.listdir(directory):
        if filename.endswith("_face_2.jpg") or filename.endswith("_face_3.jpg") or filename.endswith("_face_4.jpg") or filename.endswith("_face_5.jpg") :
            file_path = os.path.join(directory, filename)
            os.remove(file_path)
            print(f"Removed {filename}")


# Convert images to array ready to be used in models
def encode(directory):
    labels = []   # List to store corresponding labels for images
    players = []  # List to store arrays of resized images

    for filename in os.listdir(directory):
        if filename.endswith(".jpg") or filename.endswith(".jpeg"):
            file_path = os.path.join(directory, filename)

            # Extract player name from the filename
            player_name = os.path.splitext(filename)[0].split('_')[0].replace(" ", "_").lower()

            # Load image using PIL and resize to 64x64
            img = Image.open(file_path)
            img_resized = img.resize((64, 64))
            img_array = np.array(img_resized)

            # Append image arrays to the list
            players.append(img_array)
            labels.append(player_name)

    # Convert the list of image arrays into a NumPy array
    players = np.array(players)

    return labels, players
