import requests
import os
import base64
from get_client import GetClient
from post_client import PostClient
from dotenv import load_dotenv
from tkinter import *
from tkinter.ttk import *
from ttkbootstrap import Style

USER_ID = "jaetrimx"

# Loads .env file containing the client id and client secret
load_dotenv()
client_data = (os.getenv("CLIENT_ID") + ":" + os.getenv("CLIENT_SECRET"))
client_url = os.getenv("temp_url")


# Creates and formats the authorization token and uses POST request to grant access
def create_token(env_data):
    auth_url = "https://accounts.spotify.com/api/token"
    scopes = ["playlist-modify-public", "playlist-modify-private"]
    token_bytes = env_data.encode("utf-8")
    bin_to_text = str(base64.b64encode(token_bytes), "utf-8")
    headers = {
        "Authorization": "Basic " + bin_to_text,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials",
            "scope": " ".join(scopes),
            }
    response = requests.post(url=auth_url, headers=headers, data=data)
    json_data = response.json()
    access_token = json_data["access_token"]
    return access_token


# Initializes the authorization token for later use
token = create_token(client_data)
print(token)

# Creates instances of the GetClient and PostClient
get_spot_api = GetClient(token)
get_post_api = PostClient(token, USER_ID)

"""
Mode 0 == Show Artists Songs
Mode 1 == Save Song Names
Mode 2 == Display related Artists
Makes global variable for the mode so the program knows which information to display based on mode
Based on the which mode, the screen displays different prompts
"""

selected_mode = -1


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
    # When the user changes to this mode, an artist can be typed in and a list of similar artists show up
    elif selected_mode == 1:
        canvas.delete("all")
        main_header()
        sub_header("Enter artist to see related artists")
    # When the user changes to this mode, songs can be typed in and saved to be added to a playlist later
    elif selected_mode == 2:
        canvas.delete("all")
        main_header()
        sub_header("Create a Playlist of Songs from Entered Artist")


# Deals with the main portion of the project, finding artists and
# songs and displaying on the screen based on selected mode
def spotify_data():
    height = 275
    if selected_mode == 0:
        reset_canvas("Enter an Artist to See Popular Songs")
        user_input = user_entry.get()
        artist_data = get_spot_api.find_artist(user_input)
        art_id = artist_data["id"]
        songs = get_spot_api.get_artist_songs(art_id)
        song_list = create_list(songs)
        count = 0
        while count < 10:
            canvas.create_text(400, height, text=f"{song_list[count]}", font=("Helvetica", 16, "normal"),
                               fill="white")
            count += 1
            height += 28
    elif selected_mode == 1:
        reset_canvas("Enter artist to see related artists")
        user_input = user_entry.get()
        artist_data = get_spot_api.find_artist(user_input)
        art_id = artist_data["id"]
        related_artists = get_spot_api.get_related_artists(art_id)
        artist_list = create_list(related_artists)
        count = 0
        while count < 10:
            canvas.create_text(400, height, text=f"{artist_list[count]}",
                               font=("Helvetica", 16, "normal"),
                               fill="white")
            count += 1
            height += 28
    elif selected_mode == 2:
        reset_canvas("Create a Playlist of Songs from Entered Artist")
        get_post_api.create_playlist(user_entry.get())


# Makes a list based on different data types such as songs, artists, etc. for formatting purposes
def create_list(artist_type):
    result = [f"{idx + 1}. {spotify_type['name']}" for idx, spotify_type in enumerate(artist_type)]
    return result


# Resets the canvas text to the proper mode
def reset_canvas(text):
    canvas.delete("all")
    main_header()
    sub_header(f"{text}")


# Creates the GUI Interface using Tkinter and TtkBoostrap
window = Tk()
window.title("Spotify Stats")
window.geometry("900x700")
window.config(padx=50, pady=50)

style = Style(theme="darkly")

canvas = Canvas(width=800, height=600)
canvas.grid(row=0, column=0, columnspan=4, rowspan=4)
canvas.config(bg="#191414", highlightthickness=0)


# Function for displaying header text
def main_header():
    canvas.create_text(400,
                       150,
                       text="Spotify Tracker",
                       font=("Ariel", 40, "bold"),
                       fill="white")


# Function for displaying sub header text
def sub_header(text_entry):
    canvas.create_text(400,
                       190,
                       text=f"{text_entry} ",
                       font=("Trebuchet MS", 20, "bold"),
                       fill="white")


# Initializes header text that will be altered upon user selection
main_header()
sub_header("Press Mode to Begin")

# Creates entry widget
user_entry = Entry(width=30, font=("Ariel", 15, "bold"), justify=CENTER, bootstyle="success")
user_entry.grid(row=1, column=0, columnspan=4)

# Mode and Enter buttons
artist_submit_button = Button(text="Enter", command=spotify_data, bootstyle="success")
artist_submit_button.grid(row=1, column=2, columnspan=2)
mode_button = Button(text="Mode", command=mode, bootstyle="success")
mode_button.grid(row=1, column=0, columnspan=2)

window.mainloop()
