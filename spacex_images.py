import requests
from image_helpers import save_image
import argparse

def fetch_spacex_last_launch(url):
    spacex_response = requests.get(url)
    spacex_response.raise_for_status()
    spasex_data = spacex_response.json()
    spasex_images = spasex_data['links']['flickr']['original']
    if spasex_images:
        for i, image_url in enumerate(spasex_images):
            save_image(image_url, f'spacex{i}.jpg')
    else:
        print("фото запуска отсутствуют")


def main():
    parser = argparse.ArgumentParser(
        description='Введите id запуска чтобы получить его фото'
    )
    parser.add_argument('-id', '--id', help='идентификатор запуска')
    args = parser.parse_args()
    if not args.id:
        spasex_url = 'https://api.spacexdata.com/v5/launches/latest'
    else:
        spasex_url = f'https://api.spacexdata.com/v5/launches/{args.id}'
        
    fetch_spacex_last_launch(spasex_url)
    

if __name__ == '__main__':
    main()
