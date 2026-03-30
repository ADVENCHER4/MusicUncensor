import re

class SongModel:
    def __init__(self, title, artist, album):
        self.title = title
        self.artist = artist
        self.album = album

    def get_artist_str(self):
        return ', '.join(self.artist).replace('-', ' ')
    
    def get_song_str(self):
        return f'{self.title.replace('-', ' ')} - {self.get_artist_str()} ({self.album.replace('-', ' ')})'
    
    def get_search_str(self):
        return f'{self.title} - {self.artist[0]}'
    
    def get_file_name(self):
        return re.sub(r'[\\/:*?"<>|]', ' ', self.title.replace('-', ' '))
