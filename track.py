# Format for adding track to playlist for POST request

class Track:

    def __init__(self, name, track_id, artist):
        self.name = name
        self.id = track_id
        self.artist = artist

    def spotify_url(self):
        return f"spotify:track:{self.id}"

    def __str__(self):
        return self.name + " by " + self.artist
