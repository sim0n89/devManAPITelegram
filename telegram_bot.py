import telegram
import os
from dotenv import load_dotenv
from os.path import join, dirname
import random
import time


def get_images_from_folder():
      images = []
      for address, dirs, files in os.walk('images'):
            for name in files:
                  images.append(os.path.join(address, name))
      random.shuffle(images)
      return images


def main():
      dotenv_path = join(dirname(__file__), '.env')
      load_dotenv(dotenv_path)
      try:
            bot_token = os.environ["BOT_TOKEN"]
      except KeyError:
            print("Вы не заполнили TOKEN бота")
            raise SystemExit
      
      try:
            chat_id = os.environ["CHAT_ID"]
      except KeyError:
            print("Вы заполнили id канала")
            raise SystemExit
      
      try:
            sleep_time = os.environ["SLEEP_TIME"]
      except KeyError:
            sleep_time = 14400 # 4 часа
      
      bot = telegram.Bot(token=bot_token)
      while True:
            images = get_images_from_folder()
            for image in images:
                  bot.send_photo(chat_id=chat_id,  photo=open(image, 'rb'))
                  time.sleep(sleep_time)

if __name__ == '__main__':
      main()
