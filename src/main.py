import logging

from download_manager import DownloadManager


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="{asctime} {levelname} - {message}",
        style="{",
        datefmt="%Y-%m-%d %H:%M",
        handlers=[
            logging.FileHandler("app.log")
        ]
    )
    manager = DownloadManager()
    while True:
        answer = input(f'Что вы хотите сделать? (1 - получить треки; 2 - скачать треки; 3 - обновить плейлист избранного; 4 - выйти) ')
        if answer == '1':
            manager.get_songs_list()
        elif answer == '2':
            manager.parse_songs_file()
            manager.download_songs()
        elif answer == '3':
            pass
        elif answer == '4':
            return
        else:
            print('Неверный ввод')
            return
    
if __name__ == '__main__':
    main()
    