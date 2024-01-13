import requests
import os
import json

class YaUploader:
    host = 'https://cloud-api.yandex.net:443'

    def __init__(self, token: str):
        self.token = token
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'OAuth {self.token}'
        }

    def create_folder(self):
        url = f'{self.host}/v1/disk/resources'
        params = {'path': 'VK', 'overwrite': True}
        response = requests.put(url, params=params, headers=self.headers).json()

    def sent_file(self, file_name, url_photo):
        with open(f'{file_name}.jpg', 'wb') as file:
            img = requests.get(url_photo)
            file.write(img.content)

        url = f'{self.host}/v1/disk/resources/upload'
        params = {'path': 'VK/'+ f'{file_name}.jpg', 'overwrite': True}
        resp = requests.get(url, params=params, headers=self.headers).json()['href']

        response = requests.put(resp, data=open(f'{file_name}.jpg', 'rb'))

        os.remove(f'{file_name}.jpg')

    def upload_photos(self, photos_dict):
        self.create_folder()

        photos_log = []
        for likes, photos in photos_dict.items():
            for photo in photos:
                if len(photos) > 1:
                    file_name = str(likes) + ' ' + photo[0]
                else:
                    file_name = str(likes)
                self.sent_file(file_name, photo[1])
                photo_log = {'file_name': f'{file_name}.jpg', 'size': 'z'}
                photos_log.append(photo_log)

        save_to_json(photos_log, 'photos.json')

def save_to_json(data, file_name):
    with open(file_name, 'w') as file:
        json.dump(data, file, indent=4)