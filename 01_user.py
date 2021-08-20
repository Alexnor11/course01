import requests
import operator
import json

# Чтение token из файла токен VK
with open('token.txt', 'r') as file_vk:
    token = file_vk.read().strip()
# Если не введен, то используется по умолчанию: "Не знаю как сделать проверку на неправильный id"
owner_id = input('Введите id от Vk: ')
if owner_id == '':
    owner_id = '552934290'

TOKEN_Y = input('Введите токен Яндекс диска: ')
if TOKEN_Y == '':
    # Чтение токен из файла Yandex
    with open('token_yandex.txt', 'r') as file_yandex:
        TOKEN_Y = file_yandex.read().strip()

while True:
    album_id = input('Введите идентификатор альбома: "wall" или "profile": ')
    if album_id != 'wall' and album_id != 'profile':
        print('Вы ввели что-то другое.')
    else:
        break

# numb_photos = input('Введите количество фотографий: ')
# for photo in ('457239025', '457239022', '457239021', '457239023', '457239024'):


URL = 'https://api.vk.com/method/photos.get'

# Стираем файл log:
file_erase = open('log.json', 'w')
file_erase.close()

params = {
    'owner_id': owner_id,
    'access_token': token,
    'v': '5.131',
    'album_id': album_id,
    # 'photo_ids': photo,
    'count': '5',

}

res = requests.get(URL, params).json()
res1 = res['response']['items']

for photo in res1:
    photos_data = {}
    photos_info = {}
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
    href = photos_data[0]
    size_type = photos_data[1]

    # Работа с Yandex
    API_BASE_URL = 'https://cloud-api.yandex.net/'
    # Передать заголовок

    headers = {
        # 'accept': 'application/json',
        'authorization': f'OAuth {TOKEN_Y}'}  # стандартный способ авторизации

    upload_url = href  # Получаем ссылку
    photo_out = str(photo_id) + '.jpg'  # имена фото
    # Создание папки на Яндекс диске:
    create = requests.put(API_BASE_URL + 'v1/disk/resources/', headers=headers, params={
        'path': 'photo_vk'
    })
    # Загрузка фотографий на Яндекс диск
    r = requests.post(API_BASE_URL + 'v1/disk/resources/upload/', headers=headers, params={
        'path': 'photo_vk/' + photo_out, 'url': upload_url
    })

    if r.status_code == 202:
        print('###', end='')
    else:
        print('При отправке файла произошла ошибка', r.status_code)

        # Запишем файл лог
    with open('log.json', 'a') as f_log:
        js = {'file_name': photo_out, 'size': size_type}
        json.dump(js, f_log, indent=1)

if r.status_code == 202:
    print(f'\nФайлы загружены на Яндекс диск!')
