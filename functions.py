# import modules
import cv2
import os
import pandas as pd

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



#### Function to save a given number of frames per second of an mp4 video

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

# Example variables:
# file = '/Users/Jason/Code/Yassinoko/dynamic-players-insights/raw_data/video/video_test.mp4'
# folder = '/Users/Jason/Code/Yassinoko/dynamic-players-insights/raw_data/video/video_images/'
# basename = 'test_frames'

# Example call of the function with 5 frames per second
# save_frames_at_fps(file, folder, basename, frames_per_second=5)
