import bs4
import gzip
import logging
import os
import time
import urllib.request

from configurator import Configurator
from mutagen.mp4 import MP4, MP4Cover
from selenium import webdriver
from selenium.webdriver.common.by import By
from urllib.parse import quote

from utils import LOAD_PAGE_TIME, SLEEP_TIME, BASE_URL, HEADERS

class Downloader:   
    def __init__(self):
        self.config = Configurator().settings        
        self.logger = logging.getLogger(__name__);

    def __get_page(self, url):
        req = urllib.request.Request(url, headers=HEADERS)
        response = urllib.request.urlopen(req)
        data = response.read()

        try:
            text = gzip.decompress(data).decode('utf-8')
        except OSError:
            text = data.decode('utf-8')
            
        return bs4.BeautifulSoup(text, 'html.parser')
    
    def __download_file(self, url, file_name):
            req = urllib.request.Request(url, headers=HEADERS)
            
            if not os.path.exists(self.config.folder_pathLself.config.folder_path):
                os.mkdir(self.config.folder_path)

            with urllib.request.urlopen(req) as response, open(f'{self.config.folder_path}/{file_name}', 'wb') as f:
                f.write(response.read())
                
    def __get_cover_url(self, url):
        op = webdriver.ChromeOptions()
        op.add_argument('headless')
        driver = webdriver.Chrome(options=op)
        driver.get(url)
        time.sleep(LOAD_PAGE_TIME)  
        img = driver.find_element(By.TAG_NAME, "img")
        cover_url = img.get_attribute("src")
        return cover_url
    
    def __edit_song_info(self, song):
        file_path = f'{self.config.folder_path}/{song.get_file_name()}.mp3'
        audio = MP4(file_path)

        audio['\xa9nam'] = [song.title]
        audio['\xa9ART'] = [song.get_artist_str()]
        audio['\xa9alb'] = [song.album]

        with open(f'{self.config.folder_path}/cover.jpg', 'rb') as img:
            cover = MP4Cover(img.read(), imageformat=MP4Cover.FORMAT_JPEG)
            
        audio['covr'] = [cover]
        audio.save()
        os.remove(f'{self.config.folder_path}/cover.jpg')

    def download_song(self, song):
        try:
            encoded = quote(song.get_search_str())
            search_page = self.__get_page(f"{BASE_URL}/search/{encoded}")
            song_handler = search_page.find_all('td')[2].a.get('href')
            
            handler_url = f"{BASE_URL}{song_handler}"
            opener = urllib.request.build_opener(NoRedirect)
            req = urllib.request.Request(handler_url, headers=HEADERS)
            try:
                opener.open(req)
            except urllib.error.HTTPError as e:
                location = e.headers.get('location')
            song_page = self.__get_page(f"{BASE_URL}{location}")
            song_url = song_page.find(id='hiddenDownload').get('href')
            cover_url = self.__get_cover_url(f"{BASE_URL}{location}")
            
            self.__download_file(song_url, f'{song.get_file_name()}.mp3')
            time.sleep(SLEEP_TIME)
            self.__download_file(cover_url, 'cover.jpg')
            
            self.__edit_song_info(song)
            
            return True
        except Exception as e:
            self.logger.exception(e)
            return False

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None