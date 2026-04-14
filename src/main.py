import logging

from config_generator import ConfigGenerator
from configurator import ConfigNotFoundException
from download_manager import DownloadManager
from models.download_mode_model import DownloadMode
from utils import CONFIG_PATH


def main():
    logging.basicConfig(
        level=logging.INFO,
        filename='app.log',
        encoding='utf-8',
        filemode='a',
        format='{asctime} {levelname} - {message}',
        style='{',
        datefmt='%Y-%m-%d %H:%M'
    )
    try:
        manager = DownloadManager()
    except ConfigNotFoundException:
        print(f'Был создан файл настроек {CONFIG_PATH}. Внесите в него свои данные и запустите приложение снова')
        return

    while True:
        answer = input(f'Что вы хотите сделать? (1 - получить треки; 2 - скачать треки; 3 - обновить плейлист избранного; 4 - выйти) ')
        if answer == '1':
            mode_answer = input(f'Какой формат вы хотите? (1 - по умолчанию; 2 - для sldl) ')
            if mode_answer == '2':
                mode = DownloadMode.SLDL
                if ConfigGenerator.create_sldl_config():
                    print('Создан конфиг файл для sldl')
            else: 
                mode = DownloadMode.DEFAULT

            manager.get_songs_list(mode)
            return
        elif answer == '2':
            manager.parse_songs_file()
            manager.download_songs()
        elif answer == '3':
            manager.remove_local_songs_from_favorite()
        elif answer == '4':
            return
        else:
            print('Неверный ввод')
            return
    
if __name__ == '__main__':
    main()
    