import requests
import random
import os
from dotenv import load_dotenv


def download_random_comic_and_get_name_with_title():
    last_num_comic = requests.get('http://xkcd.com/info.0.json').json()['num']
    random_number = random.randint(1, last_num_comic + 1)

    url = 'http://xkcd.com/{}/info.0.json'.format(random_number)
    response = requests.get(url).json()
    comic_link = response['img']
    comic_title = response['alt']
    comic_image = requests.get(comic_link)
    comic_image.raise_for_status()

    chunks_of_link = comic_link.split('/')
    name = chunks_of_link[len(chunks_of_link) - 1]

    with open(name, 'wb') as file:
        file.write(comic_image.content)

    return name, comic_title


def get_server_address():
    url = 'https://api.vk.com/method/photos.getWallUploadServer'
    params = {
                'group_id': os.getenv('GROUP_ID'),
                'access_token': os.getenv('ACCESS_TOKEN'),
                'v': '5.61',
    }
    response = requests.get(url, params=params)
    response.raise_for_status()

    server_address = response.json()['response']['upload_url']

    return server_address


def upload_comic_to_server(server_address, comic_name):
    image_file_descriptor = open(comic_name, 'rb')

    files = {'photo': image_file_descriptor}

    response = requests.post(server_address, files=files)
    response.raise_for_status()

    image_file_descriptor.close()

    server_info = response.json()

    return server_info


def save_comic(server_info):
    url = 'https://api.vk.com/method/photos.saveWallPhoto'
    params = {
                'group_id': os.getenv('GROUP_ID'),
                'photo': server_info['photo'],
                'server': server_info['server'],
                'hash': server_info['hash'],
                'access_token': os.getenv('ACCESS_TOKEN'),
                'v': '5.61',
    }
    response = requests.post(url, params=params)
    response.raise_for_status()

    comic_information = response.json()['response'][0]
    return comic_information


def post_comic(saved_comic_info, comic_title):

    url = 'https://api.vk.com/method/wall.post'

    owner_id = saved_comic_info['owner_id']
    media_id = saved_comic_info['id']
    attachments = 'photo{}_{}'.format(owner_id, media_id)

    params = {
        'owner_id': '-' + os.getenv('GROUP_ID'),
        'from_group': 1,
        'attachments': attachments,
        'message': comic_title,
        'access_token': os.getenv('ACCESS_TOKEN'),
        'v': '5.61',
    }

    response = requests.post(url, params=params)
    response.raise_for_status()


def main():
    load_dotenv()
    comic_info = download_random_comic_and_get_name_with_title()
    comic_name = comic_info[0]
    comic_title = comic_info[1]
    server_address = get_server_address()
    server_info = upload_comic_to_server(server_address, comic_name)
    info_about_saved_comic = save_comic(server_info)
    post_comic(info_about_saved_comic, comic_title)

    os.remove(comic_name)


if __name__ == '__main__':
    main()
