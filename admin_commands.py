import telegram

from core import get_user_or_error, get_order, get_profile, get_order_buttons
from queuesystem import stop_queue
from settings import *
from user_commands import start
from models import *


def adminhelp(update, context):
    stop_queue(context)
    user = get_user_or_error(id=update.message.from_user.id)
    if user:
        if user.status == 'admin':
            text = '<b>Список комманд:</b>\n' \
                   '<code>/admin</code> - переключение между статусом пользователя/админа\n' \
                   '<code>/getorder</code> - управление заказом\n' \
                   '<code>/getuser</code> - посмотреть профиль пользователя\n'
            context.bot.send_message(chat_id=update.effective_chat.id, text=text, parse_mode=telegram.ParseMode.HTML)
    else:
        start(update, context)


def admin(update, context):
    stop_queue(context)
    user = get_user_or_error(id=update.message.from_user.id)
    if user:
        try:
            if context.args[0] == ADMIN_PASSWORD:
                user.status = 'admin'
                user.save()
                text = "Вы изменили ваш статус на admin."
                context.bot.send_message(chat_id=update.effective_chat.id, text=text)
            else:
                raise Exception
        except:
            user.status = 'user'
            user.save()
            start(update, context)
    else:
        start(update, context)


def getorder(update, context):
    stop_queue(context)
    user = get_user_or_error(id=update.message.from_user.id)
    if user:
        if user.status == 'admin':
            try:
                order = Order.get(id=int(context.args[0]))
                if not order:
                    raise
                text = get_order(order, f'<b>Заказ {order.id}</b>\n')
                reply_markup = get_order_buttons(order)
                context.bot.send_message(chat_id=update.effective_chat.id,
                                         text=text,
                                         reply_markup=reply_markup,
                                         parse_mode=telegram.ParseMode.HTML)
            except:
                text = "Используйте /get_order order_id или заказ не найден."
                context.bot.send_message(chat_id=update.effective_chat.id,
                                         text=text,
                                         parse_mode=telegram.ParseMode.HTML)
    else:
        start(update, context)


def getuser(update, context):
    stop_queue(context)
    user = get_user_or_error(id=update.message.from_user.id)
    if user:
        if user.status == 'admin':
            try:
                find_user = User.get(id=int(context.args[0]))
                if not find_user:
                    raise
                text = get_profile(find_user)
            except:
                text = "Используйте /get_user user_id или заказ не найден."
            context.bot.send_message(chat_id=update.effective_chat.id, text=text, parse_mode=telegram.ParseMode.HTML)
    else:
        start(update, context)
