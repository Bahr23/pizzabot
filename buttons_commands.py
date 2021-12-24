import telegram

from core import get_user_or_error, get_order
from menu import get_menu
from queuesystem import queue
from models import *


def buttons(update, context):
    query = update.callback_query
    user = get_user_or_error(update.callback_query.from_user.id)
    data = query.data.split('@')[1:]
    if user:
        if 'queue' in context.user_data.keys():
            if context.user_data['queue']:
                if context.user_data['queue_name'] == "create_order":
                    if data[0] == "add_pizza":
                        if context.user_data['queue_position'] == 0:
                            if not context.user_data['queue_answers']:
                                context.user_data['queue_answers'].append({'pizzas': f'{data[1]},'})
                            else:
                                context.user_data['queue_answers'][0]['pizzas'] += f"{data[1]},"
                            pizza = Pizza.get(id=int(data[1]))
                            context.bot.send_message(
                                chat_id=update.effective_chat.id,
                                text=f"{pizza.name} добавлена в заказ.",
                            )
                    if data[0] == "finish_pizzas":
                        queue(update, context, user)
                        return

        if data[0] == 'order':
            order = Order.get(id=int(data[1]))
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=get_order(order, f'<b>Заказ {order.id}</b>\n'),
                parse_mode=telegram.ParseMode.HTML,
            )
        if data[0] == 'confirm':
            order = Order.get(id=int(data[1]))
            order.status = 'Принят'
            order.save()
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Вы успешно приняли заказ!',
                parse_mode=telegram.ParseMode.HTML,
            )
            context.bot.send_message(
                chat_id=order.user.id,
                text=f'Заказ {order.id} принят и скоро прибудет к вам!',
                parse_mode=telegram.ParseMode.HTML,
            )
        if data[0] == 'complete':
            order = Order.get(id=int(data[1]))
            order.status = 'Завершен'
            order.save()
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Вы успешно завершили заказ!',
                parse_mode=telegram.ParseMode.HTML,
            )
            context.bot.send_message(
                chat_id=order.user.id,
                text=f'Заказ {order.id} завершен!',
                parse_mode=telegram.ParseMode.HTML,
            )
        if data[0] == 'delete':
            order = Order.get(id=int(data[1]))
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Вы успешно удалил заказ!',
                parse_mode=telegram.ParseMode.HTML,
            )
            context.bot.send_message(
                chat_id=order.user.id,
                text=f'Заказ {order.id} удален!',
                parse_mode=telegram.ParseMode.HTML,
            )
            order.delete_instance()