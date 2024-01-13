import sys
import json
import configparser
from vkphotos import VKphotos
from yauploader import YaUploader

def read_tokens_from_ini(file_name):
    config = configparser.ConfigParser()
    config.read(file_name)
    return config['TOKENS']['token_vk'], config['TOKENS']['token_ya']

if __name__ == '__main__':
    token_vk, token_ya = read_tokens_from_ini('tokens.ini')
    
    count_photos = int(input('How many photos? (press enter for default = 5)') or 5)

    bar = pyprind.ProgBar(count_photos*2, stream=sys.stdout)

    vk_photos = VKphotos(token_vk).get_photos(count_photos)
    ya_uploader = YaUploader(token_ya)
    ya_uploader.upload_photos(vk_photos)