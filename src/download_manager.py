import logging
from configurator import Configurator
from donwloader import Downloader
import os
from models.download_mode_model import DownloadMode
from models.song_model import SongModel
from spotify_client import SpotifyClient
import time
from utils import BANLIST_FILE, FILE, SLEEP_TIME, is_cyrillic, print_list

class DownloadManager():
    def __init__(self):
        self.sp = SpotifyClient()
        self.downloader = Downloader()
        self.songs_list = []
        self.config = Configurator().settings
        self.logger = logging.getLogger(__name__);
    
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
        
        downloaded_songs = [file.split('.')[0] for file in os.listdir(self.config.folder_path) if os.path.isfile(os.path.join(self.config.folder_path, file))]
        self.songs_list = [song for song in self.songs_list if song.get_file_name() not in downloaded_songs]
        
    def __put_songs_list_to_file(self, mode):
        with open(FILE, 'w', -1, 'utf-8') as file:
            if mode == DownloadMode.DEFAULT:
                file.write('\n'.join([song.get_song_str() for song in self.songs_list]))
            elif mode == DownloadMode.SLDL:
                file.write('\n'.join([song.get_sldl_song_str() for song in self.songs_list]))
        
    def get_songs_list(self, mode):
        liked_songs = self.sp.get_all_liked_tracks()
            
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

       
    # todo: remove songs from favorite