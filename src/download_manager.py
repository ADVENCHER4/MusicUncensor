import logging
from configurator import Configurator
from downloader import Downloader
import os
from models.download_mode_model import DownloadMode
from models.song_model import SongModel
from models.to_remove_song_model import ToRemoveSongModel
from tag_service import TagService
from spotify_client import SpotifyClient
import time
from utils import BANLIST_FILE, FILE, SLEEP_TIME, is_cyrillic, print_list
from yandex_client import YandexClient

class DownloadManager():
    def __init__(self):
        self.downloader = Downloader()
        self.songs_list = []
        self.config = Configurator().settings
        self.logger = logging.getLogger(__name__);
        if self.config.mode == 'spotify':
            self.client = SpotifyClient()
        elif self.config.mode == 'yandex':
            self.client = YandexClient()
        else:
            raise ModeNotSetException
    
    def __filter_songs(self, liked_songs):
        if not os.path.exists(BANLIST_FILE):
            open(BANLIST_FILE, 'a', -1, 'utf-8').close()
            return

        with open(BANLIST_FILE, 'r', -1, 'utf-8') as file:
            banlist = file.readlines()
            
        banlist = [text.removesuffix('\n') for text in banlist]
        for song in liked_songs:
            if is_cyrillic(song.title) or is_cyrillic(song.get_artist_str()):
                if not any(text in song.get_song_str() for text in banlist):
                    self.songs_list.append(song)
    
    def __remove_downloaded_tracks(self):
        if not os.path.exists(self.config.folder_path):
            return

        downloaded_songs = self.__get_local_songs()

        new_song_list = []
        for song in self.songs_list:
            should_add = True
            for downloaded_song in downloaded_songs:
                if song == downloaded_song:
                    should_add = False
            
            if should_add:
                new_song_list.append(song)
        self.songs_list = new_song_list
        
    def __put_songs_list_to_file(self, mode):
        with open(FILE, 'w', -1, 'utf-8') as file:
            if mode == DownloadMode.DEFAULT:
                file.write('\n'.join([song.get_song_str() for song in self.songs_list]))
            elif mode == DownloadMode.SLDL:
                file.write('\n'.join([song.get_sldl_song_str() for song in self.songs_list]))
                
    def __get_local_songs(self):
        downloaded_songs = []
        for file in os.listdir(self.config.folder_path):
            path = os.path.join(self.config.folder_path, file)
            if os.path.isfile(path):
                downloaded_songs.append(TagService.read(path))
        
        return downloaded_songs
        
    def get_songs_list(self, mode):
        liked_songs = [SongModel.to_model(song) for song in self.client.get_all_liked_tracks()]
            
        self.__filter_songs(liked_songs)        
        self.__remove_downloaded_tracks()
        print_list([song.get_song_str() for song in self.songs_list])       
                
        print(f'Список треков можно изменить в файле ({FILE})')
        self.__put_songs_list_to_file(mode)
            
    def parse_songs_file(self):
        with open(FILE, 'r', -1, 'utf-8') as file:
                for song in file.readlines():
                    song = song.removesuffix('\n')
                    [name, second] = song.split('-')
                    name = name.strip()
                    artists = [artist.strip() for artist in second.strip().split('(')[0].split(',')]
                    album = second.strip().split('(')[1][:-1].strip()
                    self.songs_list.append(SongModel(name, artists, album))
        self.__remove_downloaded_tracks()
        self.__put_songs_list_to_file(DownloadMode.DEFAULT)
                    
    def download_songs(self):
        error_downloads = []
        success_downloads = 0
        for song in self.songs_list:
            if self.downloader.download_song(song):
                success_downloads += 1
                print(f'Удалось скачать {song.title}')
                self.logger.info(f'Successfully downloaded song {song.title}')
            else:
                error_downloads.append(song)
                print(f'Не удалось скачать {song.title}')
                self.logger.warning(f'Error downloading song {song.title}')
            time.sleep(SLEEP_TIME)
            
        self.logger.info(f'Successfully downloaded {success_downloads}')
        print(f'Загрузка завершена. Успешно: {success_downloads}, неуспешно: {len(error_downloads)} ({(success_downloads / len(self.songs_list) * 100)}%)')
        if len(error_downloads):
            songs = [song.get_song_str() for song in error_downloads]
            print('Не удалось скачать:')
            print_list(songs)
            print(f'Этот список хранится в файле ({FILE})')
            with open(FILE, 'w', -1, 'utf-8') as file:
                    file.write('\n'.join(songs))

    def remove_local_songs_from_favorite(self):
        if not os.path.exists(self.config.folder_path):
            return
        downloaded_songs = self.__get_local_songs()
        full_songs_list = [ToRemoveSongModel.to_model(song) for song in self.client.get_all_liked_tracks()]
        remove_songs_list = []
        for song in full_songs_list:
            should_add = False
            for downloaded_song in downloaded_songs:
                if song == downloaded_song:
                    should_add = True
            
            if should_add:
                remove_songs_list.append(song.id)
                
        try: 
            for i in range(0, len(remove_songs_list), 40):
                self.client.remove_tracks_from_liked(remove_songs_list[i:i+40])
            print('Локальные треки успешно удалены из избранных')
        except Exception as e:
            print('Не удалось удалить локальные треки из избранных')
            self.logger.error(f'Error removing tracks from favorite')
            self.logger.exception(e)
            
class ModeNotSetException(Exception):
    pass