import telegram
import os
from dotenv import load_dotenv
from os.path import join, dirname


def main():
   dotenv_path = join(dirname(__file__), '.env')
   load_dotenv(dotenv_path)
   try:
         bot_token = os.environ["BOT_TOKEN"]
   except KeyError:
         print("Вы не заполнили TOKEN бота")
         raise SystemExit

   bot = telegram.Bot(token=bot_token)
   chat_id = -1001614010027
   # bot.send_message(chat_id=chat_id, text="hello")
   bot.send_photo(chat_id=chat_id,  photo=open('images/spacex0.jpg', 'rb'))


if __name__ == '__main__':
    main()
