from telegram.ext import CommandHandler, MessageHandler, Filters, CallbackQueryHandler

from admin_commands import admin, getorder, getuser, adminhelp
from buttons_commands import buttons
from user_commands import *


def command_handler(dispatcher):
    # Buttons
    dispatcher.add_handler(CallbackQueryHandler(buttons))

    # User commands
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help))

    dispatcher.add_handler(CommandHandler("profile", profile))
    dispatcher.add_handler(MessageHandler(Filters.regex("Профиль"), profile))

    dispatcher.add_handler(CommandHandler("createorder", create_order))
    dispatcher.add_handler(MessageHandler(Filters.regex("Сделать заказ"), create_order))

    dispatcher.add_handler(CommandHandler("myorders", my_orders))
    dispatcher.add_handler(MessageHandler(Filters.regex("Мои заказы"), my_orders))

    # Admin commands
    dispatcher.add_handler(CommandHandler("adminhelp", adminhelp))
    dispatcher.add_handler(CommandHandler("admin", admin))
    dispatcher.add_handler(CommandHandler("getorder", getorder))
    dispatcher.add_handler(CommandHandler("getuser", getuser))

    # Utils
    dispatcher.add_handler(MessageHandler(Filters.text, all_messages))