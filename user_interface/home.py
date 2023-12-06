import streamlit as st
import os
import tensorflow as tf
import numpy as np
from lib.data_processing import encode
from lib.video_processing import *
from stats.kpi_formulas import *
from stats.graphics import *


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
background-size: cover;
background-position: center;
background-repeat: no-repeat;
background-attachment: fixed;
}} '''

st.markdown(page_bg_img, unsafe_allow_html=True)

# Introduction
st.markdown(
    """
    <style>
        [data-testid=stImage] {
            text-align: center;
            display: block;
            margin-left: auto;
            margin-right: auto;
            width: 100%;
        }
    </style>
    """, unsafe_allow_html=True
)

ospath = os.path.dirname(os.path.abspath(__file__))
img_path = os.path.join(ospath, "KickVision_X_UCL_3.png")

st.image(img_path)

st.markdown(
    f"""
    <h2 style='color: white;'>The Art of the Game is in your hands</h2>
    """,
    unsafe_allow_html=True
)


# Markdown in quote block
st.markdown("""
    <h2 style='color: white;'>
    > Faces recognition during live games to display statistics analysis.
    """,
   unsafe_allow_html=True)

text_list = [
    "The model is trained on recognizing the faces of 10 different players from both Real Madrid FC and Liverpool FC. The players are the following :",
    "- Trend Alexander-Arnold",
    "- Marco Asensio",
    "- Karim Benzema",
    "- Dani Carvajal",
    "- Dani Ceballos",
    "- Thibaut Courtois",
    "- Lucas Henderson",
    "- Lucas Vázquez",
    "- Sadio Mané",
    "- Mohamed Salah",
    " ",
    "The statistics are about the 21/22 UEFA Champions League season. If the model recognizes the faces of the video, statistics will be displayed below."
]

for text in text_list:
    st.markdown(f"<p style='color: white;'>{text}</p>", unsafe_allow_html=True)

st.markdown(
    f"""
    <p style='color: white;'>Upload a short video of your favorite highlight from the UCL 21/22</p>
    """,
    unsafe_allow_html=True
)

video = st.file_uploader(
    " ",
    type=['mp4', 'mov']
)

# Reset file path
file_path = None

# Save video in uploaded_video folder using name of the file uploaded
if video is not None:
    # video details saved to present if needed
    # video_details = {"FileName": video.name, "FileType": video.type}
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
    # st.success(f"Video Successfully Uploaded  {celebration_emoji}")

    # Loading gif

    # gif_path = os.path.join(ospath, "51LA.gif")
    # gif_display = st.image(gif_path, width=275)

if video is not None:

    model_path = os.path.join(ospath, "lib" ,"model_83_nik.h5")
    model_83 = load_model(model_path)

    face_arrays = extract_faces_from_video(file_path)
    processed_faces = preprocess_faces(face_arrays)
    results = get_predictions(processed_faces, model_83)
    names = get_unique_names_appearing_twice_or_more(results)

    video_file = open(file_path, 'rb')
    video_bytes = video_file.read()

    # Displying video
    st.markdown(
                f'<h1 style="color: white;">Uploaded Video</h1>',
                unsafe_allow_html=True
            )
    vid = st.video(video_bytes)

    # Remove gif
    # gif_display.empty()

    st.markdown(
        f'<h1 style="color: white;">Players from the video</h1>',
        unsafe_allow_html=True
    )

    # Converting names to uppercase for multiselect options
    uppercase_names = list(map(lambda x: x.upper(), names))

    # Using st.write to display styled text for each option
    st.markdown(
        f'<p style="color: white;">Select Players to compare</p>',
        unsafe_allow_html=True
    )

    # Displaying the multiselect dropdown
    selected_data = st.multiselect(
        "",
        uppercase_names
)
    selected_data = map(lambda x: x.lower(), selected_data)

    # Displying graphs
    if selected_data != []:
            # Comparison Bar Charts
            # st.header("Comparison Bar Charts")

            player_positions = {
            'benzema': 'forward and midfield',
            'salah' : 'forward and midfield',
            'mané' : 'forward and midfield',
            'asensio' : 'forward and midfield',
            'henderson' : 'forward and midfield',
            'carvajal' : 'defender',
            'courtois' : 'goalkeeper',
            'alexander-arnold' : 'defender',
            'ceballos' : 'forward and midfield',
            'lucas vázquez' : 'forward and midfield'
            }

            dict_pos = {'forward and midfield':[], 'defender':[], 'goalkeeper':[]}

            # Generate random data for the bar charts
            for player in selected_data:
                dict_pos[player_positions[player]].append(player)

                st.markdown(
                f'<h1 style="color: white;">Players Satistics</h1>',
                unsafe_allow_html=True
            )

            for pos, players in dict_pos.items():
                if len(players) != 0:
                    if pos in 'forward and midfield':
                            st.plotly_chart(plot_combined_goal_types(*players), use_container_width=True)
                            st.plotly_chart(plot_pass_stats(*players), use_container_width=True)
                    elif pos == 'defender':
                            st.plotly_chart(plot_tackle_stats(*players), use_container_width=True)
                            st.plotly_chart(plot_pass_stats(*players), use_container_width=True)
                    else:
                        st.plotly_chart(plot_goalkeeper_performance(*players), use_container_width=True)

    for player in selected_data :
        st.write(building_kpis(player))
