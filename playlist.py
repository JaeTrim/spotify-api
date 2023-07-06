# Format for creating a playlist using POST request

class Playlist:

    def __init__(self, name, play_id):
        self.name = name
        self.id = play_id

    def __str__(self):
        return f"Playlist: {self.name}"
