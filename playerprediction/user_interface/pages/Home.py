import streamlit as st
import os

# Define emoji variables
soccer_emoji = '\u26BD'
celebration_emoji = '\U0001F389'
chart_increasing_emoji = '\U0001F4C8'

# Introduction
st.markdown(
    f"""
    ## Welcome to Dynamic Players Insights {soccer_emoji}
    #### Enhance your viewing experience with data insights {chart_increasing_emoji}
    """
)

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

st.write("file path : ", file_path)

if video is not None:
    video_file = open(file_path, 'rb')
    video_bytes = video_file.read()
    st.video(video_bytes)
