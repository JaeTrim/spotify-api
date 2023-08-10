"""
This class is a current work in progress, trying to figure out how to use POST requests and proper scope
and authorization to create playlists on a user's spotify account
"""


import json

import requests

from playlist import Playlist

"""
PostClient handles the POST requests for the Spotify Web API, using a user's spotify id as well
as the authorization token in order to create playlists and add recommended tracks
"""


class PostClient:

    # Constructor initializes token and user_id
    def __init__(self, token, user_id):
        self.token = token
        self.user_id = user_id

    # Using a POST request, a playlist is created on the user's spotify account
    def create_playlist(self, playlist_name):
        header = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}"
        }
        url = f"https://api.spotify.com/v1/users/{self.user_id}/playlists"
        json_data = {
            "name": playlist_name,
            "description": "Recommended Songs",
            "public": True
        }
        response = requests.post(url=url, data=json.dumps(json_data), headers=header)
        response_json = response.json()
        print(response_json)
        # return response_json["id"]
