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

numb_photos = 5


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
            'album_id': 'wall',
            # 'photo_ids': photo_ids,
            'count': numb_photos,
        }
        # print(numbers)
        req = requests.get(url, params={**self.params, **photo_params}).json()
        return req['response']['items']

    def get_url_photo(self):
        """Получить ссылки на фотографии максимального размера"""
        req = self.get_data()
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
            # url_photo_max = sort_list[0][1]
            photos_data = sort_list[len(sort_list) - 1][1]
            url_photo_max = photos_data[0]
            size_type = photos_data[1]

            
			"""Вот эти переменные я перенес в словарь, теперь не 
			знаю как их перенести в класс YaUploader
			Мне нужно взять ссылки и в качестве названия файла яндекс
			решил использовать id фото, потому, что лайков у меня нет, и дата
			тоже повторяется, (у меня новый аккаунт)"""
			# Словарь photo_info c необходимыми параметрами:
            photo_info['photo_id'] = photo_id
            photo_info['url_photo'] = url_photo_max
            photo_info['size_type'] = size_type
            pprint(photo_info)

    def record_data(self):
        """Записать данные о загруженных фотографиях"""
        pass


class YaUploader:
    def __init__(self, token: str):
        # self.file_url = file_url
        # self.file_path = file_path
        self.API_BASE_URL = 'https://cloud-api.yandex.net/'
        self.token = token
        self.headers = {'Authorization': token}

    def upload(self, file_path, file_url):
        """Метод загружает файлы по списку file_list на яндекс диск"""
        # 1-й запрос - получение ссылки для загрузки файла
        r = requests.post(self.API_BASE_URL + 'v1/disk/resources/upload/', headers=self.headers, params={
            'path': 'py_43' + file_path,
            'url': file_url
        })


vk_client = VkUser('668938039', token_vk, '5.131')

if __name__ == '__main__':
    """Получить путь к загружаемому файлу и токен от пользователя"""
    uploader = YaUploader(token_y)
    vk_client.get_url_photo()

# Перебираю id фотографий из vk
# for ids in ('457239025', '457239022', '457239021', '457239023', '457239024'):
#     vk_client.get_data(ids)


"""*Мне еще не понятно, можно ли так использовать метот get_url_photo() так? 
Мне как то хотелось задачи разделить на более мелкие методы. Но никак не могу понять
как можно взаимодействовть между методами.

Логически я понимаю, что с использованием ООП, код должен быть лучше, но 
у меня он получается, как то даже громозким по сравнению с первым вариантом"""