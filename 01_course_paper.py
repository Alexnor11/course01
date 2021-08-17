import requests
import operator
import json

# Чтение token из файла токен VK
with open('token.txt', 'r') as file_vk:
    token = file_vk.read().strip()
# Чтение из файла токен Yandex
with open('token_yandex.txt', 'r') as file_yandex:
    TOKEN_Y = file_yandex.read().strip()

URL = 'https://api.vk.com/method/photos.get'

# Стираем файл log:
file_erase = open('log.json', 'w')
file_erase.close()

for photo in ('457239025', '457239022', '457239021', '457239023', '457239024'):
    params = {
        'owner_id': '668938039',
        'access_token': token,
        'v': '5.131',
        'album_id': 'wall',
        'photo_ids': photo,

    }
    res = requests.get(URL, params=params).json()
    res1 = res['response']['items'][0]['sizes']

    photos_data = {}
    photos_info = {}
    for k in res1:
        height = k.get('height')
        width = k.get('width')
        size_ph = k.get('type')
        url_photo = k.get('url')
        photos_data[height] = [url_photo, size_ph]
        # pprint(photos_sizes)
    sort_photos = sorted(photos_data.items(), key=operator.itemgetter(0))

    # Получение ссылки
    photos_data = sort_photos[len(sort_photos) - 1][1]
    href = photos_data[0]
    size_type = photos_data[1]

    # Работа с Yandex
    API_BASE_URL = 'https://cloud-api.yandex.net/'
    # Передать заголовок

    headers = {
        # 'accept': 'application/json',
        'authorization': f'OAuth {TOKEN_Y}'}  # стандартный способ авторизации

    # 1-й запрос - получение ссылки для загрузки файла
    upload_url = href  # Получаем ссылку
    photo_out = str(photo) + '.jpg'  # имена фото
    r = requests.post(API_BASE_URL + 'v1/disk/resources/upload/', headers=headers, params={
        'path': 'py-43/' + photo_out, 'url': upload_url
    })
    if r.status_code == 202:
        print('###', end='')
    else:
        print('При отправке файла произошла ошибка', r.status_code)

        # Запишем файл лог
    with open('log.json', 'a') as f_log:
        js = {'file_name': photo_out, 'size': size_type}
        json.dump(js, f_log, indent=1)

print('\nФотографии загружены на Яндекс диск')
