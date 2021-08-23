from pprint import pprint
import requests
import operator
import json

# Чтение token из файла VK
with open('token.txt', 'r') as file_vk:
    token_vk = file_vk.read().strip()
# Чтение токен из файла Yandex
with open('token_yandex.txt', 'r') as file_yandex:
    token_y = file_yandex.read().strip()
# Сделать запрос у пользователя


class VkUser:
    url = 'https://api.vk.com/method/'

    def __init__(self, owner_id, token, version):
        """Авторизация vk"""
        self.params = {
            'owner_id': owner_id,
            'access_token': token,
            'v': version
        }

    def get_data(self):
        """Получить данные с VK"""
        url = self.url + 'photos.get'
        photo_params = {
            'album_id': 'profile',
            # 'photo_ids': photo_ids,
            'count': '5',
        }
        # print(numbers)
        req = requests.get(url, params={**self.params, **photo_params}).json()
        return req['response']['items']

    def get_url_photo(self):
        """Получить ссылки на фотографии максимального размера"""
        req = self.get_data()
        photo_info_all = {}
        for val in req:
            photo_data = {}
            photo_info = {}
            photo_date = val.get('date')
            photo_id = val.get('id')
            # photo_info['photo_id'] = photo_id
            photo_sizes = val.get('sizes')
            # pprint(photo_id)
            for data in photo_sizes:
                height = data.get('height')
                width = data.get('width')
                photo_type = data.get('type')
                url_photo = data.get('url')
                # Получаем площадь разрешения фото:
                photo_data[height * width] = [url_photo, photo_type]
            # Сортируем фото по площади фото:
            sort_list = sorted(photo_data.items(), key=operator.itemgetter(0))
            # Выбираю ссылки на фотографии максимального размера:
            photos_data = sort_list[len(sort_list) - 1][1]
            url_photo_max = photos_data[0]
            size_type = photos_data[1]
            # return size_type, url_photo_max
            # pprint(size_type)
            # pprint(url_photo_max)

            # Словарь параметров фото:
            photo_info['photo_id'] = photo_id
            photo_info['url_photo'] = url_photo_max
            photo_info['size_type'] = size_type
            # pprint(photo_info)
            return photo_info

    def record_data(self):
        """Записать данные о загруженных фотографиях"""
        pass


class YaUploader:
    def __init__(self, token: str):
        self.API_BASE_URL = 'https://cloud-api.yandex.net/'
        self.token = token
        self.headers = {'Authorization': token}

    def upload(self, file_url, file_path):
        """Метод загружает файлов на яндекс диск"""
        # Создание папки на Яндекс диске:
        requests.put(self.API_BASE_URL + 'v1/disk/resources/', headers=self.headers, params={
            'path': 'photo_vk'
        })
        loading = requests.post(self.API_BASE_URL + 'v1/disk/resources/upload/', headers=self.headers, params={
            'path': 'photo_vk/' + str(file_path) + '.jpg',
            'url': file_url
        })
        if loading.status_code == 202:
            print('###', end='')


if __name__ == '__main__':
    """Получить путь к загружаемому файлу и токен от пользователя"""
    vk_client = VkUser('552934290', token_vk, '5.131')
    up_loader = YaUploader(token_y)
    photo = vk_client.get_url_photo()
    # print(photo['photo_id'])
    up_loader.upload(photo['url_photo'], photo['photo_id'])