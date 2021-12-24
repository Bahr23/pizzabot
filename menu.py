from typing import Union, List

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from models import *


menus = {
    'main': {
        'type': 'reply',
        'body': [
            {
                'buttons': [
                    KeyboardButton(text="Сделать заказ", callback_data="new_order"),
                    KeyboardButton(text="Мои заказы", callback_data="my_orders"),
                    KeyboardButton(text="Профиль", callback_data="profile"),
                ],
                'header': None,
                'footer': None,
                'n_cols': 1
            }
        ]
    },
}


def get_menu(tag):
    try:
        menu_name = tag.split("#")[1]
    except:
        menu_name = tag
    try:
        menu_page = int(tag.split("#")[2])
    except:
        menu_page = 0

    try:
        cur_menu = menus[menu_name]['body'][menu_page]
    except Exception as e:
        return False

    markup = build_menu(buttons=cur_menu['buttons'],
                        n_cols=cur_menu['n_cols'],
                        header_buttons=cur_menu['header'],
                        footer_buttons=cur_menu['footer'])

    if menus[menu_name]['type'] == 'inline':
        return InlineKeyboardMarkup(markup)
    if menus[menu_name]['type'] == 'reply':
        return ReplyKeyboardMarkup(keyboard=markup, resize_keyboard=True)


def build_menu(buttons, n_cols, header_buttons=None, footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, [header_buttons])
    if footer_buttons:
        menu.append([footer_buttons])
    return menu
