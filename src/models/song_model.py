import re

class SongModel:
    def __init__(self, title, artist, album):
        self.title = title
        self.artist = artist
        self.album = album
        
    def __eq__(self, value):
        return self.title == value.title and self.album == value.album and sorted(self.artist) == sorted(value.artist)

    def get_artist_str(self):
        return ', '.join(self.artist)
    
    def get_song_str(self):
        return f'{self.title} - {self.get_artist_str()} ({self.album})'
    
    def get_sldl_song_str(self):
        return f'{self.get_artist_str()} - {self.title}'
    
    def get_search_str(self):
        return f'{self.title} - {self.artist[0]}'
    
    def get_file_name(self):
        return re.sub(r'[\\/:*?"<>|]', ' ', ' '.join(self.title.replace('-', ' ').split()))
