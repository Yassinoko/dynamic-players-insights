from keras.models import load_model
from lib.data_processing import encode
# from array2class import get_class_from_array

import numpy as np

import cv2
import dlib
import os
import numpy as np

from collections import Counter

def get_class_from_array(array):

    predicted_class_index = np.argmax(array)

    unique_classes = ['alexander-arnold', 'asensio','benzema', 'carvajal',
                      'ceballos', 'courtois','henderson', 'lucas vázquez',
                      'mané', 'salah']

    return unique_classes[predicted_class_index]


def extract_faces_from_video_old(video_path):
    face_arrays = []

    detector = dlib.get_frontal_face_detector()

    cap = cv2.VideoCapture(video_path)
    frame_count = 0
    fps = cap.get(cv2.CAP_PROP_FPS)

    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            break

        current_frame_time = cap.get(cv2.CAP_PROP_POS_MSEC)
        next_second_time = current_frame_time + 1000

        cap.set(cv2.CAP_PROP_POS_MSEC, next_second_time)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector(gray)

        for face in faces:
            x, y, w, h = face.left(), face.top(), face.width(), face.height()
            cropped_face = frame[y:y+h, x:x+w]
            is_new_face = True

            if is_new_face:

                face_arrays.append(cropped_face)

                frame_count += int(fps)

                cap.set(cv2.CAP_PROP_POS_FRAMES, frame_count)

    cap.release()
    cv2.destroyAllWindows()

    return face_arrays


def extract_faces_from_video(video_path):
    face_arrays = []

    detector = dlib.get_frontal_face_detector()
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)

    while cap.isOpened():
        ret, frame = cap.read()
        
        try:
            blurred_frame = cv2.GaussianBlur(frame, (35, 35), 0)
        except:
            pass

        if not ret:
            break

        gray = cv2.cvtColor(blurred_frame, cv2.COLOR_BGR2GRAY)
        faces = detector(gray)

        for face_idx, face in enumerate(faces):
            x, y, w, h = face.left(), face.top(), face.width(), face.height()
            cropped_face = frame[y:y+h, x:x+w]

            # Convert BGR to RGB
            cropped_face_rgb = cv2.cvtColor(cropped_face, cv2.COLOR_BGR2RGB)
            face_arrays.append(cropped_face_rgb)

            # Move to the next second in the video
            cap.set(cv2.CAP_PROP_POS_MSEC, cap.get(cv2.CAP_PROP_POS_MSEC) + 10)

        cap.set(cv2.CAP_PROP_POS_FRAMES, cap.get(cv2.CAP_PROP_POS_FRAMES) + int(fps))

    cap.release()
    return face_arrays


def preprocess_faces(face_arrays):
    processed_faces = []

    for face in face_arrays:
        resized_face = cv2.resize(face, (64, 64))
        resized_face = np.expand_dims(resized_face, axis=0)
        processed_faces.append(resized_face)

    return processed_faces


def get_predictions(processed_faces, model):
    predictions = []

    for face in processed_faces:
        prediction = model.predict(face)
        predictions.append(prediction)

    return predictions


def get_unique_names_appearing_twice_or_more(results):
    players_name = []
    for array in results:
        players_name.append(get_class_from_array(array))

    name_counts = Counter(players_name)

    filtered_names = [name for name, count in name_counts.items() if count >= 1]

    unique_filtered_names = list(set(filtered_names))

    return unique_filtered_names
