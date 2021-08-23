from pprint import pprint
import requests
import operator
import json

# Стираем файл log:
file_erase = open('log.json', 'w')
file_erase.close()


class VkUser:
    url = 'https://api.vk.com/method/'

    def __init__(self, token, version):
        """Авторизация vk"""
        # Запрос vk id у пользователя:
        while True:
            owner_id = input('Введите id от Vk: ')
            if owner_id == '':
                print('Вы ничего не ввели!')
            else:
                break

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
        try:
            req['response']['items']
        except KeyError:
            # print('Введен не верный id от VK пользователя!')
            exit('Введен не верный id от VK пользователя!')
        return req

    def get_url_photo(self):
        """Получить ссылки на фотографии максимального размера"""
        req = self.get_data()
        photo_info_all = []
        for photo in req['response']['items']:
            photos_data = {}
            photo_info = {}
            photo_id = photo.get('id')
            photo_sizes = photo.get('sizes')
            for k in photo_sizes:
                height = k.get('height')
                width = k.get('width')
                size_ph = k.get('type')
                url_photo = k.get('url')
                photos_data[height] = [url_photo, size_ph]
                # pprint(photos_sizes)
            sort_photos = sorted(photos_data.items(), key=operator.itemgetter(0))

            # Получение ссылки
            photos_data = sort_photos[len(sort_photos) - 1][1]
            url_photo_max = photos_data[0]
            size_type = photos_data[1]

            # Словарь параметров фото:
            photo_info['photo_id'] = photo_id
            photo_info['url_photo'] = url_photo_max
            photo_info['size_type'] = size_type

            photo_info_all.append(photo_info)
        return photo_info_all


class YaUploader:
    def __init__(self, token: str):
        self.API_BASE_URL = 'https://cloud-api.yandex.net/'
        self.token = token
        self.headers = {'Authorization': token}

    def upload(self, file_url, photo_id):
        """Метод загружает файлов на яндекс диск"""
        # Создание папки на Яндекс диске:
        requests.put(self.API_BASE_URL + 'v1/disk/resources/', headers=self.headers, params={
            'path': 'photo_vk'
        })

        loading = requests.post(self.API_BASE_URL + 'v1/disk/resources/upload/', headers=self.headers, params={
            'path': 'photo_vk/' + str(photo_id) + '.jpg',
            'url': file_url
        })
        if loading.status_code == 202:
            print('###', end='')
        elif loading.status_code != 202:
            exit(f' Ошибка: {loading.status_code}, Возможно введен не верный токен от Яндекс Диск!')

    def get_data_upload(self):
        photos = vk_client.get_url_photo()
        for photo in photos:
            file_url = photo['url_photo']
            photo_id = photo['photo_id']
            size_type = photo['size_type']
            up_loader.upload(file_url, photo_id)

            # Запишем файл лог
            with open('log.json', 'a') as f_log:
                js = {'file_name': photo_id, 'size': size_type}
                json.dump(js, f_log, indent=1)

        print(f'\nФайлы загружены на Яндекс диск!')


# Чтение token из файла токен VK (Запрос у пользователя отключен)
def reading_token_vk():
    with open('token.txt', 'r') as file_vk:
        token_vk = file_vk.read().strip()
        return token_vk


# Запись в файл токена введенного от пользователя:
def reading_token_y():
    while True:
        token_y = input('Введите токен Яндекс диска: ')
        if token_y == '':
            print('Токен не может быть пустым!')
        else:
            break
    with open('token_yandex.txt', 'w') as file_yandex:
        file_yandex.write(token_y)

    # Чтение токен из файла Yandex
    with open('token_yandex.txt', 'r') as file_yandex:
        token_y = file_yandex.read().strip()
        return token_y


if __name__ == '__main__':
    """Получить путь к загружаемому файлу и токен от пользователя"""
    vk_client = VkUser(reading_token_vk(), '5.131')
    up_loader = YaUploader(reading_token_y())
    up_loader.get_data_upload()

