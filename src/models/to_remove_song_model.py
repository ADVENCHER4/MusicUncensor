from models.song_model import SongModel


class ToRemoveSongModel(SongModel):
    def __init__(self, id, title, artist, album):
        self.id = id
        super().__init__(title, artist, album)
        
    @staticmethod
    def to_model(song):
        return ToRemoveSongModel(song['id'], song['name'], [artist['name'] for artist in song['artists']], song['album']['name'])