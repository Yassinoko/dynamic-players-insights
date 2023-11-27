import streamlit as st
import os
import tensorflow as tf
import numpy as np
# from lib.video_processing import get_cropped_image_dict, save_frames_at_fps_cropped
# from ml_models.data_library.image_preprocessing import processing_images

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

# Request user to input short video via file upload
video = st.file_uploader(
    "Upload a short video of your favorite sport moment", # user message
    type=['mp4', 'mov'], # possible to add other video types
)

# Reset file path
file_path = None

# Save video in uploaded_video folder using name of the file uploaded
if video is not None:
    # video details saved to present if needed
    video_details = {"FileName": video.name, "FileType": video.type}
    # create folder name to store uploaded videos
    upload_dir = "uploaded_videos"
    # create the directory if it does not exist
    os.makedirs(upload_dir, exist_ok=True)
    # define the file_path of the video
    file_path = os.path.join(upload_dir, video.name)
    # save the video using the file_path defined
    with open(file_path, "wb") as f:
        f.write(video.getbuffer())
    # inform the user if the video was successfully uploaded
    st.success(f"Video Successfully Uploaded  {celebration_emoji}")

# st.write("file path : ", file_path)

col1, col2 = st.columns(2)

if video is not None:
    video_file = open(file_path, 'rb')
    video_bytes = video_file.read()
    with col1:
        st.header("Video Display")
        st.video(video_bytes)

    with col2:
        st.header("Data List")
        st.write("- Data 1")
        st.write("- Data 2")
        st.write("- Data 3")

    # Comparison Bar Charts
    st.header("Comparison Bar Charts")

    # Generate random data for the bar charts
    data1 = np.random.randint(1, 10, size=5)
    data2 = np.random.randint(1, 10, size=5)

    # Display bar charts
    st.bar_chart({"Data 1": data1, "Data 2": data2})

# video_paths = "/Users/yassinebouaine/code/Yassinoko/dynamic-players-insights/uploaded_videos/Clip_test.mp4"
# dir_path = "/Users/yassinebouaine/code/Yassinoko/dynamic-players-insights/uploaded_videos"

# # Save the face of the first player detected in the video in image format
# frame = save_frames_at_fps_cropped(video_paths, dir_path, "picture")
# print(frame)

# # Convert the image to an array, ready to be processed
# frame_in_array = get_cropped_image_dict(frame)

# # Processing the image. [0] because there is no label as this is what needs to be predicted
# X_new = processing_images(frame_in_array)[0]
# print(X_new)

# # Loading the model
# model = tf.keras.models.load_model("lib/model.keras")

# # Predicting the label
# prediction = model.predict(X_new)
