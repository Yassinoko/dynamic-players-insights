# import modules
import cv2
import os
import pandas as pd
from PIL import Image
import numpy as np
import face_recognition
from data_processing import crop
import dlib

# load key_stats into notebook
key_stats = pd.read_csv("raw_data/stats/key_stats.csv")
# create Real Madrid and Man. United list of players
real_player_list = list(key_stats[key_stats.club == 'Real Madrid'].player_name.unique())
man_player_list = list(key_stats[key_stats.club == 'Man. United'].player_name.unique())


def player_name_list_preprocessing(player_list):
    """ This function takes a list of player names from kaggle dataset and lowers + replaces spaces by dashes"""
    preprocessed_list = []
    for player in player_list:
        player = player.lower()
        player = player.replace(" ", "-")
        preprocessed_list.append(player)
    return preprocessed_list


def save_frames_at_fps(video_path, dir_path, basename, ext='jpg', frames_per_second=1):
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        return

    os.makedirs(dir_path, exist_ok=True)
    base_path = os.path.join(dir_path, basename)

    digit = len(str(int(cap.get(cv2.CAP_PROP_FRAME_COUNT))))
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = 0

    frame_interval = int(fps / frames_per_second) if frames_per_second > 0 else 1

    while True:
        ret, frame = cap.read()
        if ret:
            if frame_count % frame_interval == 0:
                cv2.imwrite('{}_{}.{}'.format(base_path, str(frame_count).zfill(digit), ext), frame)
            frame_count += 1
        else:
            break

    cap.release()


def save_frames_at_fps_cropped(video_path, dir_path, basename, ext='jpg', frames_per_second=1):
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        return

    os.makedirs(dir_path, exist_ok=True)
    base_path = os.path.join(dir_path, basename)

    digit = len(str(int(cap.get(cv2.CAP_PROP_FRAME_COUNT))))
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = 0

    frame_interval = int(fps / frames_per_second) if frames_per_second > 0 else 1

    while True:
        ret, frame = cap.read()
        if ret:
            if frame_count % frame_interval == 0:
                image_pil = Image.fromarray(frame)
                cropped_face = crop(image_pil)

                if cropped_face:
                    cropped_face.save(f'{base_path}_cropped_face.{ext}')
                    cropped_image = cropped_face
                    break

            frame_count += 1
        else:
            break

    cap.release()

    return cropped_image


def get_cropped_image_dict(cropped_image):
    """This modified function processes a cropped image and adds it to the dictionary of images."""

    try:
        image_np = np.array(cropped_image)

        img_label_dict = {'image': [], 'name': []}

        label = 'Unknown'

        img_label_dict['image'].append(image_np)
        img_label_dict['name'].append(label)

        return img_label_dict
    except Exception as e:
        print(f"Error processing cropped image: {e}")
        return None


def extract_faces_from_video(video_path, output_folder='extracted_faces'):

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    detector = dlib.get_frontal_face_detector()

    cap = cv2.VideoCapture(video_path)

    frame_count = 0
    face_saved = False

    while cap.isOpened() and not face_saved:
        ret, frame = cap.read()

        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = detector(gray)

        for face_idx, face in enumerate(faces):
            x, y, w, h = face.left(), face.top(), face.width(), face.height()

            cropped_face = frame[y:y+h, x:x+w]

            face_filename = os.path.join(output_folder, f'face_{frame_count}_{face_idx}.jpg')
            cv2.imwrite(face_filename, cropped_face)

            face_saved = True
            break

        frame_count += 1

    cap.release()
    cv2.destroyAllWindows()

    num_files = len([f for f in os.listdir(output_folder) if os.path.isfile(os.path.join(output_folder, f))])
    print(f"Number of face files saved: {num_files}")
    print(f"Extracted faces saved in the folder: '{output_folder}'")
