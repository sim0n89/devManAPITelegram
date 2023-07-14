import telegram
import os
from dotenv import load_dotenv
from os.path import join, dirname
import random
import time
import argparse


def get_images_from_folder():
    images = []
    for address, dirs, files in os.walk("images"):
        for name in files:
            images.append(os.path.join(address, name))
    random.shuffle(images)
    return images


def main():
    dotenv_path = join(dirname(__file__), ".env")
    load_dotenv(dotenv_path)
    try:
        bot_token = os.environ["BOT_TOKEN"]
    except KeyError:
        print("Вы не заполнили TOKEN бота")
        raise SystemExit

    try:
        chat_id = os.environ["CHAT_ID"]
    except KeyError:
        print("Вы не заполнили id канала")
        raise SystemExit

    sleep_time = os.getenv("SLEEP_TIME", default=14400)
    bot = telegram.Bot(token=bot_token)
    parser = argparse.ArgumentParser(
        description="Отправка фото в телеграм"
    )
    parser.add_argument("-f", "--file", help="Путь к файлу")

    args = parser.parse_args()
    if args.file == "all":
        while True:
            images = get_images_from_folder()
            for image in images:
                with open(image, "rb") as file:
                    bot.send_photo(chat_id=chat_id,  photo=file)
                time.sleep(float(sleep_time))
    else:
        if not args.file:
            images = get_images_from_folder()
            file = random.choice(images)
        else:
            file = args.file
            
        try:
            with open(file, "rb") as file:
                bot.send_photo(chat_id=chat_id,  photo=file)
        except FileNotFoundError:
            print("Файл не найден")
        return


if __name__ == "__main__":
    main()
