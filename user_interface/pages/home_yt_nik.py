import streamlit as st
import os
import tensorflow as tf
import numpy as np
from lib.data_processing import encode
from lib.video_processing import *
from stats.kpi_formulas import *
from pytube import YouTube


# Define emoji variables
soccer_emoji = '\u26BD'
celebration_emoji = '\U0001F389'
chart_increasing_emoji = '\U0001F4C8'

# Remove Streamlit sidebar
st.set_page_config(layout="wide")

page_bg_img = f'''
<style>
[data-testid="stAppViewContainer"] > .main {{
background-image: url("https://images5.alphacoders.com/571/571559.jpg");
background-size: 180%;
background-position: top left;
background-repeat: no-repeat;
background-attachment: local;
}} '''

st.markdown(page_bg_img, unsafe_allow_html=True)

# Introduction
st.image('logo.png')

st.markdown(
    f"""
    ## The Art of the Game is in your hands
    """
)

# Markdown in quote block
st.markdown("""
> Faces recognition during live games to display analysis statistics.
""")

# Request user to input video URL
video_url = st.text_input("Enter video URL", "")
yt = None

# Check if URL is provided
if video_url:
    # Display video from the URL
        #st.video(video_url)

    # try:
        # Download the video using pytube
        yt = YouTube(video_url)
        video_path = yt.streams.get_highest_resolution().download()
        st.success(f"Video Successfully Downloaded  {celebration_emoji}")

        # Perform face recognition or other processing with the downloaded video
        # Use 'video_path' as the downloaded video file for further processing
        # For example, you can use 'video_path' as the file path for open(video_path, 'rb')

        # Displaying the video using st.video
        video_file = open(video_path, 'rb')
        video_bytes = video_file.read()
        st.video(video_bytes)

        # Other parts of your code for processing and analysis using the video
        # ...

    # except Exception as e:
    #     st.error(f"Error: {e}")


# # Save video in uploaded_video folder using name of the file uploaded
# if video_file is not None:
#     # video details saved to present if needed
#     # video_details = {"FileName": video_file.name, "FileType": video_path.type}
#     # create folder name to store uploaded videos
#     upload_dir = "uploaded_videos"
#     # create the directory if it does not exist
#     os.makedirs(upload_dir, exist_ok=True)
#     # define the file_path of the video
#     file_path = os.path.join(upload_dir, video_file.name)
#     # save the video using the file_path defined
#     with open(file_path, "wb") as f:
#         f.write(video_path.getbuffer())
#     # inform the user if the video was successfully uploaded
#     st.success(f"Video Successfully Uploaded  {celebration_emoji}")

# st.write("file path : ", file_path)

col1, col2 = st.columns(2)

if yt is not None:

    model_83 = load_model('lib/model_83_nik.h5')

    face_arrays = extract_faces_from_video(video_path)
    processed_faces = preprocess_faces(face_arrays)
    results = get_predictions(processed_faces, model_83)
    names = get_unique_names_appearing_twice_or_more(results)

    video_file = open(video_path, 'rb')
    video_bytes = video_file.read()
    with col1:
        st.header("Video Display")
        vid = st.video(video_bytes)

    with col2:
        st.header("Data List")
        selected_data = st.multiselect("Select Data Items", names)
        # for name in names:
        #     st.write(name)

    # Comparison Bar Charts
    st.header("Comparison Bar Charts")

    # Generate random data for the bar charts
    data1 = np.random.randint(1, 10, size=5)
    data2 = np.random.randint(1, 10, size=5)

    # Display bar charts
    st.bar_chart({"Data 1": data1, "Data 2": data2})

    for player in selected_data :
        st.write(building_kpis(player))
