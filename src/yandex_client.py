import json
from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.command import Command
from webdriver_manager.chrome import ChromeDriverManager
from yandex_music import Client

class YandexClient:
    def __init__(self):
        token = self.__get_token()
        client = Client(token).init()
        client.users_likes_tracks()[0].fetch_track().download('example.mp3')
        self.client = Client(token).init()
        
    def __is_active(self, driver):
        try:
            driver.execute(Command.GET_ALL_COOKIES)
            return True
        except Exception:
            return False


    def __get_token(self, ):
        chrome_options = Options()
        chrome_options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(
            service=service,
            options=chrome_options
        )
        driver.get(
            "https://oauth.yandex.ru/authorize?response_type=token&client_id=23cabbbdc6cd418abb4b39c32c41195d"
        )
        token = None

        while token is None and self.__is_active(driver):
            sleep(1)
            try:
                logs_raw = driver.get_log("performance")
            except Exception:
                continue

            for lr in logs_raw:
                log = json.loads(lr["message"])["message"]
                url_fragment = log.get('params', {}).get('frame', {}).get('urlFragment')

                if url_fragment and "access_token" in url_fragment:
                    token = url_fragment.split('&')[0].split('=')[1]
                    break

        driver.quit()
        return token

    def get_all_liked_tracks(self):
        likes = self.client.users_likes_tracks()
        tracks = likes.fetch_tracks()

        result = []

        for track in tracks:
            song_dict = {
                'id': str(track.id),
                'name': track.title,
                'artists': [{'name': artist.name} for artist in track.artists],
                'album': {
                    'name': track.albums[0].title if track.albums else ""
                }
            }

            result.append(song_dict)

        return result
    
    def remove_tracks_from_liked(self, tracks_to_remove):
        self.client.users_likes_tracks_remove(tracks_to_remove)