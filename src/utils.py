SLEEP_TIME = 0.5
LOAD_PAGE_TIME = 3
BASE_URL = 'https://muzsky.net'
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36"
}
FILE = './songs.txt'
BANLIST_FILE = './banlist.txt'
CONFIG_PATH = './config.cfg'
RETRIES_COUNT = 3

def is_cyrillic(text, alphabet=set('абвгдеёжзийклмнопрстуфхцчшщъыьэюя')):
    return not alphabet.isdisjoint(text.lower())

def print_list(list):
    for i in range(len(list)):
        print(f'{i + 1}. {list[i]}')