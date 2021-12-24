import logging

from telegram import Bot
from telegram.ext import Updater

from command_handler import command_handler
from settings import *


def main():

    bot = Bot(token=TOKEN)
    print(bot)

    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    command_handler(dispatcher)

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
    updater.start_polling()


if __name__ == "__main__":
    main()
