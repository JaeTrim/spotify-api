import random

import requests


# Creates a class that uses Spotify Web API and GET requests to obtain information
# such as artists, songs, and related artists
class SpotifyClient:

    # Constructor initializes token and authorization header
    def __init__(self, token):
        self.token = token
        self.header = {"Authorization": "Bearer " + self.token}

    # Uses the auth token in order to look up a spotify artist
    def find_artist(self, name):
        url = "https://api.spotify.com/v1/search" + f"?q={name}&type=artist&limit=1"
        response = requests.get(url, headers=self.header)
        data = response.json()["artists"]["items"]
        if len(data) == 0:
            raise ValueError("This artist does not exist")
        else:
            return data[0]

    # Uses the auth token to get the top 10 most popular songs from a spotify artist
    def get_artist_songs(self, artist_id):
        url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
        response = requests.get(url=url, headers=self.header)
        data = response.json()["tracks"]
        return data

    # Uses the auth token to get related artists based on the artist inputted
    def get_related_artists(self, artist_id):
        url = f"https://api.spotify.com/v1/artists/{artist_id}/related-artists?country=US"
        response = requests.get(url=url, headers=self.header)
        data = response.json()["artists"]
        return data
