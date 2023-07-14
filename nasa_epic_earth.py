import os
from image_helpers import *
import argparse


def get_data_nasa_epic(api_key, quantity=10):
    response = requests.get(
        "https://api.nasa.gov/EPIC/api/natural/images", params={"api_key": api_key, "count": quantity})
    response.raise_for_status()
    images = response.json()
    for image in images:
        date = image["date"].split(" ")[0].replace("-", "/")
        image_link = f"https://api.nasa.gov/EPIC/archive/natural/{date}/png/{image['image']}.png"
        save_image(image_link, f"{image['image']}.png", {"api_key": api_key})


def main():
    try:
        nasa_api_key = os.environ["NASA_API_KEY"]
    except KeyError:
        nasa_api_key = ""
        print("Вы не заполнили API ключ НАСА")
        raise SystemExit

    parser = argparse.ArgumentParser(
        description="ведите максимальное количество фото для сохранения"
    )
    parser.add_argument("-q", "--quantity", help="Количество фото", default=10)
    args = parser.parse_args()
    quantity = args.q
    get_data_nasa_epic(nasa_api_key, quantity)


if __name__ == "__main__":
    main()
