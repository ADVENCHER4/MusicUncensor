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

from utils import LOAD_PAGE_TIME, RETRIES_COUNT, SLEEP_TIME, BASE_URL, HEADERS

class Downloader:   
    def __init__(self):
        self.config = Configurator().settings        
        self.logger = logging.getLogger(__name__)
        op = webdriver.ChromeOptions()
        op.add_argument('headless')
        self.driver = webdriver.Chrome(options=op)

    def __del__(self):
        self.driver.quit()
        
    def __get_song_handler(self, song):
        encoded = quote(song.get_search_str())
        self.driver.get(f"{BASE_URL}/search/{encoded}")
        time.sleep(LOAD_PAGE_TIME)
        link = self.driver.find_elements(By.XPATH, "//a[contains(@href, '/handler/')]")[0]
        return link.get_attribute('href')

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
        
        if not os.path.exists(self.config.folder_path):
            os.mkdir(self.config.folder_path)

        with urllib.request.urlopen(req) as response, open(f'{self.config.folder_path}/{file_name}', 'wb') as f:
            f.write(response.read())
                
    def __get_cover_url(self, url):
        self.driver.get(url)
        time.sleep(LOAD_PAGE_TIME)  
        img = self.driver.find_element(By.TAG_NAME, "img")
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
        retries = RETRIES_COUNT
        while retries > 0:
            try:  
                handler_url = self.__get_song_handler(song)        
                opener = urllib.request.build_opener(NoRedirect)
                req = urllib.request.Request(handler_url, headers=HEADERS)
                try:
                    opener.open(req)
                except urllib.error.HTTPError as e:
                    location = e.headers.get('location')
                song_page = self.__get_page(f"{BASE_URL}{location}")
                song_link = song_page.find(id='hiddenDownload')
                if song_link is None:
                    song_link = song_page.find('a', class_='btn btn-light w-75 mr-3')
                song_url = song_link.get('href')
                cover_url = self.__get_cover_url(f"{BASE_URL}{location}")
                
                self.__download_file(song_url, f'{song.get_file_name()}.mp3')
                time.sleep(SLEEP_TIME)
                self.__download_file(cover_url, 'cover.jpg')
                
                self.__edit_song_info(song)
                
                return True
            except Exception as e:
                self.logger.error(f'Attempt to download {song.title} failed. {retries} attempts remain')
                self.logger.exception(e)
                retries -= 1

        return False

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None