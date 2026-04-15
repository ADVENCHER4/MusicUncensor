import configparser
import os

from models.settings_model import SettingsModel
from utils import CONFIG_PATH

class Configurator:
    _instance = None
    _initialized = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        self.settings = self.read_settings()
        self._initialized = True
    
    def create_empty_config(self):
        config = configparser.ConfigParser(allow_no_value=True)
        config.set('DEFAULT', '; spotify or yandex')
        config.set('DEFAULT', 'MODE', 'spotify')
        config['SPOTIFY'] = {
            'CLIENT_ID': '',
            'CLIENT_SECRET': '',
            'REDIRECT_URI': 'https://127.0.0.1/callback',
            'SCOPE': 'user-library-read user-library-modify playlist-modify-private playlist-modify-public'
        }
        config['OS'] = {
            'FOLDER_PATH': './songs'
        }
        with open(CONFIG_PATH, 'w') as configfile:
            config.write(configfile)
        raise ConfigNotFoundException
            
    def read_settings(self):
        if not os.path.exists(CONFIG_PATH):
            self.create_empty_config()
            return
        
        config = configparser.ConfigParser()
        config.read(CONFIG_PATH)
        
        return SettingsModel(config)
    
class ConfigNotFoundException(Exception):
    pass
