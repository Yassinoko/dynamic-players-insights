from keras.models import load_model
from data_processing import encode

import numpy as np

import cv2
import dlib
import os


def extract_faces_from_video(video_path, output_folder='extracted_faces'):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Load the pre-trained face detector model from dlib
    detector = dlib.get_frontal_face_detector()

    # Open the video file
    cap = cv2.VideoCapture(video_path)

    frame_count = 0
    face_saved = False

    while cap.isOpened() and not face_saved:
        ret, frame = cap.read()

        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the current frame
        faces = detector(gray)

        for face_idx, face in enumerate(faces):
            x, y, w, h = face.left(), face.top(), face.width(), face.height()

            # Crop the detected face from the frame
            cropped_face = frame[y:y+h, x:x+w]

            # Save the cropped face as an image file
            face_filename = os.path.join(output_folder, f'face_{frame_count}_{face_idx}.jpg')
            cv2.imwrite(face_filename, cropped_face)

            face_saved = True  # Set flag to True after saving one face
            break  # Break the loop after saving one face

        frame_count += 1

    cap.release()
    cv2.destroyAllWindows()

    num_files = len([f for f in os.listdir(output_folder) if os.path.isfile(os.path.join(output_folder, f))])
    print(f"Number of face files saved: {num_files}")
    print(f"Extracted faces saved in the folder: '{output_folder}'")
