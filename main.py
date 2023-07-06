import pandas
import requests

from dotenv import load_dotenv
from tkinter import *

import os
import base64

from spotify_client import SpotifyClient

# Loads .env file containing the client id and client secret
load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")


# Creates Spotify API Auth Token
def create_token(c_id, c_secret):
    # Formats token by combining client id and secret
    format_token = c_id + ":" + c_secret
    # Uses encode function to encode the string into bytes
    token_bytes = format_token.encode("utf-8")
    # Applies Base64 encoding to the token_bytes, converting the binary data into text
    bin_to_text = str(base64.b64encode(token_bytes), "utf-8")

    # Headers, Data, and URL required for POST request
    headers = {
        "Authorization": "Basic " + bin_to_text,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {"grant_type": "client_credentials"}

    spotify_url = "https://accounts.spotify.com/api/token"

    response = requests.post(url=spotify_url, headers=headers, data=data)
    json_data = response.json()
    access_token = json_data["access_token"]
    return access_token


# Creates a token and calls spotify client using the token
token = create_token(client_id, client_secret)
get_spot_api = SpotifyClient(token)


# Makes a list based on different data types such as songs, artists, etc. for formatting purposes
def create_list(artist_type):
    result = [f"{idx + 1}. {spotify_type['name']}" for idx, spotify_type in enumerate(artist_type)]
    return result


# Mode 0 == Show Artists Songs
# Mode 1 == Save Song Names
# Mode 2 == Display related Artists
# Makes global variable for the mode so the program knows which information to display based on mode
selected_mode = -1


# Based on the which mode, the screen displays different prompts
def mode():
    global selected_mode
    selected_mode += 1
    if selected_mode == 3:
        selected_mode = 0
    # When the user changes to this mode, an artist can be typed in and their top songs are displayed
    if selected_mode == 0:
        canvas.delete("all")
        main_header()
        sub_header("Enter an Artist to See Popular Songs")
    # When the user changes to this mode, songs can be typed in and saved to be added to a playlist later
    elif selected_mode == 1:
        canvas.delete("all")
        main_header()
        sub_header("Enter artist to see related artists")
    # When the user changes to this mode, an artist can be typed in and a list of similar artists show up
    elif selected_mode == 2:
        canvas.delete("all")
        main_header()
        sub_header("Enter Song Names to Keep Track Of")


def spotify_data():
    # Finds spotify artist as well as their top songs and displays them into a csv file
    height = 275
    if selected_mode == 0:
        # User inputs artist in entry box and the name is received
        user_input = user_entry.get()
        # Calls the spotify client and finds the artist based on the user input
        artist_data = get_spot_api.find_artist(user_input)
        art_id = artist_data["id"]
        songs = get_spot_api.get_artist_songs(art_id)
        song_list = create_list(songs)
        count = 0
        while count < 10:
            songs = canvas.create_text(400, height, text=f"{song_list[count]}", font=("Helvetica", 20, "bold"),
                                       fill="white")
            count += 1
            height += 30
    # Show related artists
    elif selected_mode == 1:
        user_input = user_entry.get()
        artist_data = get_spot_api.find_artist(user_input)
        art_id = artist_data["id"]
        related_artists = get_spot_api.get_related_artists(art_id)
        artist_list = create_list(related_artists)
        count = 0
        while count < 10:
            related_list = canvas.create_text(400, height, text=f"{artist_list[count]}", font=("Helvetica", 20, "bold"),
                                              fill="white")
            count += 1
            height += 30
    else:
        pass
        # Code this to eventually create a spotify playlist that contains the songs that have been entered


# Creates Tkinter GUI Interface
window = Tk()
window.title("Spotify Stats")
window.config(padx=50, pady=50, bg="#1DB954")

canvas = Canvas(width=800, height=600)
canvas.grid(row=0, column=0, columnspan=4, rowspan=4)
canvas.config(bg="#191414", highlightthickness=0)


# Function for displaying header text
def main_header():
    canvas.create_text(400,
                       150,
                       text="Spotify Tracker",
                       font=("Helvetica", 40, "bold"),
                       fill="white")


# Function for displaying sub header text
def sub_header(text_entry):
    canvas.create_text(400,
                       190,
                       text=f"{text_entry} ",
                       font=("Helvetica", 20, "bold"),
                       fill="white")


# Initializes header text that will be altered upon user selection
main_header()
sub_header("Press Mode to Begin")

# Creates entry widget
user_entry = Entry(width=30, font=("Ariel", 15, "bold"), justify=CENTER)
user_entry.grid(row=1, column=0, columnspan=4)

# Enter button to display data
artist_submit_button = Button(text="ENTER", highlightthickness=0, command=spotify_data, justify=CENTER)

# Mode button to change mode
mode_button = Button(text="MODE", highlightthickness=0, command=mode)

# Adds buttons to the screen
mode_button.grid(row=1, column=0, columnspan=2)
artist_submit_button.grid(row=1, column=2, columnspan=2)

window.mainloop()
