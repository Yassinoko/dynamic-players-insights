import os
import requests
import time
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import quote
from selenium import webdriver

# # load key_stats into notebook
# key_stats = pd.read_csv("raw_data/stats/key_stats.csv")
# # create Real Madrid and Man. United list of players
# real_player_list = list(key_stats[key_stats.club == 'Real Madrid'].player_name.unique())
# man_player_list = list(key_stats[key_stats.club == 'Man. United'].player_name.unique())

# def player_name_list_preprocessing(player_list):
#     """ This function takes a list of player names from kaggle dataset and lowers + replaces spaces by dashes"""
#     preprocessed_list = []
#     for player in player_list:
#         player = player.lower()
#         player = player.replace(" ", "-")
#         preprocessed_list.append(player)
#     return preprocessed_list

     
def download_images(player_name):
    # Create a directory to save the images
    player_folder_path = f"./raw_data/faces/{player_name}"
    os.makedirs(player_folder_path, exist_ok=True)

    # Define the URL for Getty Images
    encoded_player_name = quote(player_name)
    url = f"https://www.gettyimages.be/photos/{encoded_player_name}?assettype=image&compositions=headshot&family=editorial&numberofpeople=one&sort=best"

    # Configure the Chrome driver (Make sure you have the correct chromedriver installed)
    driver = webdriver.Chrome()

    try:
        # Access the URL
        driver.get(url)
        time.sleep(5)  # Allow time for the page to load

        # Extract image URLs
        image_elements = driver.find_elements("xpath", '//img[contains(@src, "https://media.gettyimages.com")]')

        # Download and save 30 images
        count = 0
        for img in image_elements:
            img_url = img.get_attribute("src")
            img_data = requests.get(img_url).content
            with open(f"{player_folder_path}/{player_name}_{count}.jpg", "wb") as handler:
                handler.write(img_data)
            count += 1
            if count == 30:
                break

        print(f"Downloaded {count} images of {player_name} from Getty Images.")

    except Exception as e:
        print(f"Failed to retrieve images of {player_name} from Getty Images. Error: {e}")

    finally:
        # Close the browser
        driver.quit()
        

        
""" IMAGE SCRAPING """

# # import key_stats file
# key_stats = pd.read_csv("raw_data/stats/key_stats.csv")

# # create dictionary of team_names keys and player_name values
# team_names = ['Real Madrid', 'Liverpool', 'Man. United', 'Villareal', 'Benfica', 'Bayern', 'Atlético', 'Chelsea']
# team_players_dict = {}
# for team_name in team_names:
#     team_players_dict[team_name] = list(key_stats[key_stats.club == team_name].player_name.unique())

# for team, players in team_players_dict.items():
#     for player in players:
#         download_images(player + ' ' + team)