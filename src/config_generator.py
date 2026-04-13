import os

from configurator import Configurator


class ConfigGenerator():
    config = Configurator().settings
    @staticmethod
    def create_sldl_config():
        path='sldl.conf'
        if os.path.exists(path):
            return False

        content = f"""username = 
password = 

[wishlist]
input = ./songs.txt
input-type = list
pref-format = flac
path = {ConfigGenerator.config.folder_path}
"""

        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True
