import logging
import os

from configurator import Configurator
from mutagen import File
from mutagen.easyid3 import EasyID3
from mutagen.flac import FLAC
from mutagen.mp4 import MP4, MP4Cover

from models.song_model import SongModel
class TagService:
    config = Configurator().settings
    logger = logging.getLogger(__name__)

    @staticmethod
    def read(file_path):
        audio = File(file_path)

        if audio is None:
            TagService.logger.error(f'Cannot check type of the {file_path}')
            return

        name = audio.__class__.__name__

        if name == 'MP3':
            audio = EasyID3(file_path)

            title = audio.get('title', [''])[0]
            album = audio.get('album', [''])[0]
            artists = audio.get('artist', [])

        elif name == 'MP4':
            title = audio.get('\xa9nam', [''])[0]
            album = audio.get('\xa9alb', [''])[0]
            artists = audio.get('\xa9ART', [])

        elif name == 'FLAC':
            title = audio.get('title', [''])[0]
            album = audio.get('album', [''])[0]
            artists = audio.get('artist', [])

        else:
            TagService.logger.error(f'Cannot check type of the {file_path}')
            return
        
        artists = [x.strip() for x in artists[0].split(',') if x.strip()]

        return SongModel(title, artists, album)

    @staticmethod
    def write(song):
        file_path = f'{TagService.config.folder_path}/{song.get_file_name()}.mp3'
        audio = File(file_path)

        if audio is None:
            TagService.logger.error(f'Cannot check type of the {song}')

        name = audio.__class__.__name__

        if name == 'MP3':
            audio = EasyID3(file_path)

            audio['title'] = [song.title]
            audio['artist'] = song.artists
            audio['album'] = [song.album]

        elif name == 'MP4':
            audio = MP4(file_path)

            audio['\xa9nam'] = [song.title]
            audio['\xa9ART'] = song.artists
            audio['\xa9alb'] = [song.album]
            with open(f'{TagService.config.folder_path}/cover.jpg', 'rb') as img:
                cover = MP4Cover(img.read(), imageformat=MP4Cover.FORMAT_JPEG)
            audio['covr'] = [cover]
            os.remove(f'{TagService.config.folder_path}/cover.jpg')

        elif name == 'FLAC':
            audio = FLAC(file_path)
            audio['title'] = [song.title]
            audio['artist'] = song.artists
            audio['album'] = [song.album]

        else:
            TagService.logger.error(f'Cannot check type of the {song}')

        audio.save()