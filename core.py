from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from menu import build_menu
from models import *


def get_user_or_error(id):
    try:
        user = User.get(id=id)
        if not user.id:
            raise DoesNotExist
        return user
    except DoesNotExist:
        return False


def get_profile(user):
    if user:
        try:
            orders_count = len(user.orders)
            text = f"<b>Профиль</b>\nid: {user.id}\nИмя: {user.name}\nКол-во заказов: {orders_count}"
            return text
        except:
            return False
    else:
        return False


def get_order(order, header='', footer=''):
    if order:
        try:
            text = header
            text += f"<i>Статус - {order.status}\n</i>"
            text += "\nСостав:\n"
            fullprice = 0

            pizzas_id = order.pizzas.split(',')[:-1]
            for id in pizzas_id:
                pizza = Pizza.get(id=int(id))
                fullprice += pizza.price
                text += f"{pizza.name} - {pizza.price}р.\n"
            text += f"Итоговая стоимость - {fullprice}р.\n" \
                f"\nАдрес - {order.address}\n" \
                f"Телефон - {order.phone}\n"
            text += footer
            return text
        except:
            return False
    else:
        return False


def get_order_buttons(order):
    buttons = []
    if order.status == 'В обработке':
        buttons.append(InlineKeyboardButton('Подтвердить заказ', callback_data=f"@confirm@{order.id}"))
    if order.status == 'Принят':
        buttons.append(InlineKeyboardButton('Завершить заказ', callback_data=f"@complete@{order.id}"))
    buttons.append(InlineKeyboardButton('Удалить заказ', callback_data=f"@delete@{order.id}"))
    return InlineKeyboardMarkup(build_menu(buttons, n_cols=1))