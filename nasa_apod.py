import requests
from image_helpers import *
from dotenv import load_dotenv
from os.path import join, dirname
import os
import argparse


def get_nasa_images_urls(api_key, quantity):
    response = requests.get(
        'https://api.nasa.gov/planetary/apod', params={'api_key': api_key, "count": quantity})
    response.raise_for_status()
    images = response.json()
    urls = []
    for image in response_data:
        urls.append(image['url'])
    return urls


def main():
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)
    try:
        nasa_api_key = os.environ["NASA_API_KEY"]
    except KeyError:
        nasa_api_key = ''
        print("вы не заполнили API ключ НАСА")
        raise SystemExit

    parser = argparse.ArgumentParser(
        description='Введите максимальное количество фото для сохранения'
    )
    parser.add_argument('-q', '--quantity', help='Количество фото', default=10)
    args = parser.parse_args()
    quantity = args.q
    images_urls = get_nasa_images_urls(nasa_api_key, quantity)
    for i, url in enumerate(images_urls):
        extension = get_image_extension(url)
        save_image(url, f'nasa_apod_{i}.{extension}')


if __name__ == '__main__':
    main()
