import time
import requests
import pyprind

class VKphotos:
    Url = 'https://api.vk.com/method/photos.get'

    def __init__(self, token: str, vk_id=None):
        self.token = token
        if vk_id is None:
            vk_id = input('Input VK ID or screen name of the target profile:') or '1517274'
        self.vk_id = vk_id

    def get_photos(self, count_photos):
        params = {
            'owner_id': self.vk_id,
            'access_token': self.token,
            'v': '5.131',
            'album_id': 'profile',
            'rev': 1,
            'extended': 1,
            'count': count_photos
        }

        photos = requests.get(self.Url, params=params).json()['response']['items']
        photos_dict = {}
        
        for photo in photos:
            key = photo['likes']['count']
            sizes = photo['sizes']
            for size in sizes:
                if size['type'] == 'z':
                    url_photo = size['url']
                    break
            if key in photos_dict:
                photos_dict[key] = photos_dict[key] + [[(time.strftime('%Y_%m_%d', time.gmtime(photo['date']))), url_photo]]
            else:
                photos_dict.setdefault(key, [[time.strftime('%Y_%m_%d', time.gmtime(photo['date'])), url_photo]])

        return photos_dict