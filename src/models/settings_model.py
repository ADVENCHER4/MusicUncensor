class SettingsModel:
    def __init__(self, config):
        self.mode = config['DEFAULT']['MODE']
        self.client_id = config['SPOTIFY']['CLIENT_ID']
        self.client_secret = config['SPOTIFY']['CLIENT_SECRET']
        self.redirect_uri = config['SPOTIFY']['REDIRECT_URI']
        self.scope = config['SPOTIFY']['SCOPE']
        self.folder_path = config['OS']['FOLDER_PATH']
    