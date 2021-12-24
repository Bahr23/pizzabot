import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from menu import get_menu, build_menu
from models import *
from core import *
from queuesystem import stop_queue, queue, current_queue


def start(update, context):
    stop_queue(context)
    user = get_user_or_error(id=update.message.from_user.id)
    if user:

        text = f"{user.name}, привет!"
    else:
        if update.message.from_user.username:
            username = update.message.from_user.username
        else:
            username = 'none'
        user = User.create(
            id=update.message.from_user.id,
            status='user',
            name=update.message.from_user.first_name,
            username=username
        )
        text = f"{user.name}, вы успешно зарегистрировались!"
    menu = get_menu("main")
    context.bot.send_message(chat_id=update.effective_chat.id, text=text, reply_markup=get_menu('main'))


def help(update, context):
    stop_queue(context)
    user = get_user_or_error(id=update.message.from_user.id)
    if user:
        text = '<b>Список комманд:</b>\n' \
               '<code>/profile</code> - посмотреть свой профиль\n' \
               '<code>/createorder</code> - создать заказ\n' \
               '<code>/myorders</code> - посмотреть свои заказы\n'

        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=text,
                                 reply_markup=get_menu('main'),
                                 parse_mode=telegram.ParseMode.HTML)
    else:
        start(update, context)


def profile(update, context):
    stop_queue(context)
    user = get_user_or_error(id=update.message.from_user.id)
    if user:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=get_profile(user),
            parse_mode=telegram.ParseMode.HTML
        )
    else:
        start(update, context)


def all_messages(update, context):
    user = get_user_or_error(id=update.message.from_user.id)
    if user:
        if 'queue' in context.user_data.keys():
            if context.user_data['queue']:
                queue(update, context, user, )
                return
        context.user_data.update({'last_message': update.message.text})

        text = f"{user.name}, я не знаю как на это ответить."
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text,
            parse_mode=telegram.ParseMode.HTML,
            reply_markup=get_menu('main')
        )
    else:
        start(update, context)


def create_order(update, context):
    stop_queue(context)
    user = get_user_or_error(id=update.message.from_user.id)

    if user:
        queue_list = [
            {'pizza': 'Выберите пиццу:', 'menu': 'pizzas'},
            {'address': 'Укажите ваш адрес'},
            {'phone': 'Укажите ваш телефон'},
        ]

        context.user_data.update({
            'queue': True,
            'queue_name': 'create_order',
            'queue_finish': 'Заказ успешно создан и отправлен на проверку.',
            'queue_list': queue_list,
            'queue_position': 0,
            'queue_answers': [],
            'queue_docs': '',
            'last_queue_message': ''})

        current_queue(update, context, user)
    else:
        start(update, context)


def my_orders(update, context):
    stop_queue(context)
    user = get_user_or_error(id=update.message.from_user.id)

    if user:
        if user.orders:
            text = "<b>Ваши заказы:</b>\n"
            buttons = []
            for order in user.orders:
                text += f"Заказ {order.id}\n"
                buttons.append(InlineKeyboardButton(f"Заказ {order.id}", callback_data=f'@order@{order.id}'))
            reply_markup = InlineKeyboardMarkup(build_menu(buttons, n_cols=1))
        else:
            text = "У вас еще нет заказов."
            reply_markup = None
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text,
            parse_mode=telegram.ParseMode.HTML,
            reply_markup=reply_markup
        )
    else:
        start(update, context)
