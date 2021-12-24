import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from core import get_user_or_error, get_order, get_order_buttons
from menu import get_menu, build_menu
from models import *


def stop_queue(context):
    if 'queue' in context.user_data.keys():
        if context.user_data['queue']:
            context.user_data.update({'queue': False})


def queue(update, context, user, ans=None):
    if update.callback_query:
        query = update.callback_query
        if not ans:
            ans = query.data
    else:
        if not ans:
            ans = update.message.text
    if ans != "@finish_pizzas":
        answer = {list(context.user_data['queue_list'][context.user_data['queue_position']].keys())[0]: ans}
        context.user_data['queue_answers'].append(answer)
    context.user_data['queue_position'] += 1
    if context.user_data['queue_position'] < len(context.user_data['queue_list']):
        current_queue(update, context, user)
    else:
        context.user_data['queue'] = False
        finish_queue(context.user_data['queue_name'], context.user_data['queue_answers'], update, context)
        if context.user_data['queue_finish']:
            text = context.user_data['queue_finish']
            reply_markup = get_menu(tag='main')
            context.bot.send_message(
                                        chat_id=update.effective_chat.id,
                                        text=text,
                                        reply_markup=reply_markup,
                                        parse_mode=telegram.ParseMode.HTML,
                                    )


def current_queue(update, context, user):
    text = list(context.user_data['queue_list'][context.user_data['queue_position']].values())[0]
    try:
        qmenu = context.user_data['queue_list'][context.user_data['queue_position']]['menu']

        if qmenu == 'pizzas':
            pizzas = Pizza.select()
            buttons = []
            for p in pizzas:
                text += f"\n{p.name} - {p.price}р."
                buttons.append(InlineKeyboardButton(f"Добавить {p.name}", callback_data=f'@add_pizza@{p.id}'))
            footer_button = InlineKeyboardButton("Завершить заказ", callback_data="@finish_pizzas")
            reply_markup = InlineKeyboardMarkup(build_menu(buttons=buttons, n_cols=2, footer_buttons=footer_button))

        else:
            reply_markup = get_menu(tag=qmenu)[0]
    except:
        reply_markup = None

    if context.user_data['last_queue_message'] == text:
        return
    context.bot.send_message(
                                chat_id=update.effective_chat.id,
                                text=text,
                                reply_markup=reply_markup,
                                parse_mode=telegram.ParseMode.HTML
                            )
    context.user_data.update({'last_queue_message': text})


def finish_queue(name, answers, update=None, context=None):
    if update.callback_query:
        query = update.callback_query
        user = get_user_or_error(update.callback_query.message.chat.id)
    else:
        user = get_user_or_error(update.message.from_user.id)

    if name == "create_order":
        print(answers)
        order = Order.create(user=user,
                             pizzas=answers[0]['pizzas'],
                             address=answers[1]['address'],
                             phone=answers[2]['phone'])
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=get_order(order, f"<b>Заказ {order.id} успешон создан!</b>\n", f"\nОжидайте решение мененжера."),
            parse_mode=telegram.ParseMode.HTML,
            reply_markup=get_menu('main')
        )

        admins = User.select().where(User.status == 'admin')
        for admin in admins:
            context.bot.send_message(
                chat_id=admin.id,
                text=get_order(order, f"<b>Поступил новый заказ!</b>\n id - <code>{order.id}</code>\n"),
                parse_mode=telegram.ParseMode.HTML,
                reply_markup=get_order_buttons(order)
            )