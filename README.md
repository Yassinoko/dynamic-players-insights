
# Dynamic Players Insights or should I say ... KickVision !

<img width="1414" alt="image" src="https://github.com/Yassinoko/dynamic-players-insights/assets/116871835/73fe201d-c53c-4de6-b134-154e2ac2d18c">

This project is about understanding the untold story of football games. Raising the stakes by bulding KPIs about players and revealing their performances during live / replays videos.

Please have a look at our project here : kickvision.streamlit.app

## Files
The main folder is user_interface. That is all you need to test the project.
Dataset : https://www.kaggle.com/datasets/azminetoushikwasi/ucl-202122-uefa-champions-league
1. lib/data_processing.py : functions which aim to clean the faces the model was trained on.
2. lib/video_processing.py : functions which process the video you pass on the app to predict players and build stats.
3. lib/model_83_nik.h5 : model used to predict the players. Shootout to Nikolay for creating it !
4. stats/graphics.py : main graphics that are displayed for the predicted players of your video.
5. stats/kpi_formulas.py : additional KPIs that you can use in case you want to display extra information on the app.
6. stats/stats_preprocessing.py : extra processing steps of the Kaggle UCL dataset.

## Usage
### Upload video. 
You can uploaed a < 200 MB. The model will then predict the faces. 
### Display Stats
If predicted, you can select multiple players to show their UCL 21/22 statistics.

## Getting Started
1. Clone the repository:

`git clone https://github.com/your-username/dynamic-players-insights.git`
`cd dynamic-players-insights`

2. Install the required dependencies: pip install -r requirements.txt
