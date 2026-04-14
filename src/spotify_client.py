from configurator import Configurator
import spotipy
from spotipy.oauth2 import SpotifyOAuth

from models.song_model import SongModel

class SpotifyClient:
    def __init__(self):
        config = Configurator().settings
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id = config.client_id,
            client_secret = config.client_secret,
            redirect_uri = config.redirect_uri,
            scope = config.scope
        ))
        
    def __fetch_liked_tracks(self):
        results = self.sp.current_user_saved_tracks(limit=50)
        tracks = results['items']
        while results['next']:
            results = self.sp.next(results)
            tracks.extend(results['items'])
        return tracks

    def get_all_liked_tracks(self):
        songs = []
        for item in self.__fetch_liked_tracks():
            songs.append(item['track'])
        return songs
    
    def remove_tracks_from_liked(self, tracks_to_remove):
        self.sp.current_user_saved_tracks_delete(tracks=tracks_to_remove)