import requests
from pathlib import Path
from pprint import pprint
from dotenv import load_dotenv
import os
from os.path import join, dirname, splitext
from urllib import parse


def save_image(url, name, params=None):
    path = Path("images")
    path.mkdir(exist_ok=True)
    file_path = path / name
    response = requests.get(url, params=params)
    response.raise_for_status()
    with open(file_path, 'wb') as file:
        file.write(response.content)


def fetch_spacex_last_launch(url):
    spacex_response = requests.get(url)
    spacex_response.raise_for_status()
    spasex_data = spacex_response.json()
    spasex_images = spasex_data['links']['flickr']['original']
    for i, image_url in enumerate(spasex_images):
        save_image(image_url, f'spacex{i}.jpg')


def get_image_extension(url):
    path = parse.urlparse(url)
    return splitext(path.path.rstrip("/").split("/")[-1])[-1]


def get_nasa_images_urls(api_key):
    response = requests.get(
        'https://api.nasa.gov/planetary/apod', params={'api_key': api_key, "count": 50})
    response.raise_for_status()
    response_data = response.json()
    urls = []
    for image in response_data:
        urls.append(image['url'])
    return urls


def get_data_nasa_epic(api_key):
    response = requests.get(
        'https://api.nasa.gov/EPIC/api/natural/images', params={'api_key': api_key, "count": 50})
    response.raise_for_status()
    response_data = response.json()
    for image in response_data:
        date = image['date'].split(' ')[0].replace('-', '/')
        image_link = f"https://api.nasa.gov/EPIC/archive/natural/{date}/png/{image['image']}.png"
        save_image(image_link, f"{image['image']}.png", {"api_key": api_key})


def main():
    spasex_url = 'https://api.spacexdata.com/v5/launches/5eb87d47ffd86e000604b38a'
    fetch_spacex_last_launch(spasex_url)

    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)
    try:
        nasa_api_key = os.environ["NASA_API_KEY"]
    except KeyError:
        nasa_api_key = ''
        print("вы не заполнили API ключ НАСА")
    images_urls = get_nasa_images_urls(nasa_api_key)
    for i, url in enumerate(images_urls):
        extension = get_image_extension(url)
        save_image(url, f'nasa_apod_{i}.{extension}')

    get_data_nasa_epic(nasa_api_key)


if __name__ == '__main__':
    main()
