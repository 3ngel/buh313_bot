import datetime

import requests
import telebot
from telebot import types
import logging
import database_records as db
import config as cfg

today = datetime.datetime.today().date()

logfile = f"./logs/telegram_bots_{today}.log"

logging.basicConfig(
    level=logging.INFO,
    filename=logfile,
    filemode="a",
    format="%(asctime)s %(levelname)s %(message)s",
)

# указываем токен для доступа к боту
bot = telebot.TeleBot(cfg.bot_key)
start_txt = 'Привет! \n\nТеперь можете работать с ботом "БухгалтерИя".'


#Отправка сообщения ботом
def send_message(message, text, markup):
    logging.info(f"{text} от пользвоателя {message.chat.username} . Чат {message.chat.id}")
    bot.send_message(message.chat.id, text, reply_markup=markup)


#Редактирование существующего сообщения
def edit_message(message, text, markup):
    logging.info(f"{text} от пользвоателя {message.chat.username} . Чат {message.chat.id}")
    bot.edit_message_text(text, message.chat.id, message.message_id,
                          reply_markup=markup)

#Запуск бота
@bot.message_handler(commands=['start'])
def start(message):
    send_message(message, start_txt, start_menu())


#Набор кнопок для старта
def start_menu():
    markup = types.InlineKeyboardMarkup(row_width=2)
    services = types.InlineKeyboardButton("Услуги", callback_data='services')
    requests = types.InlineKeyboardButton("Заявки", callback_data='requests')
    markup.add(services, requests)
    return markup

#Набор кнопок для "Услуги"
def servises_menu():
    markup = types.InlineKeyboardMarkup(row_width=2)
    services_list = types.InlineKeyboardButton("Список услуг", callback_data='service_list')
    services_add = types.InlineKeyboardButton("Добавить услугу", callback_data='service_add')
    to_start_menu = types.InlineKeyboardButton("Назад", callback_data='to_start_menu')
    markup.add(services_list, services_add, to_start_menu)
    return markup

#Набор кнопок для "Заявки"
def requests_menu():
    markup = types.InlineKeyboardMarkup(row_width=1)
    request_list = types.InlineKeyboardButton("Список заявок", callback_data='request_list')
    to_start_menu = types.InlineKeyboardButton("Назад", callback_data='to_start_menu')
    markup.add(request_list, to_start_menu)
    return markup


#Обработчик нажатых кнопок
@bot.callback_query_handler(func=lambda call: True)
def check_callback_data(call):
    if call.data == "services":
        edit_message(call.message, "Выберите вариант", servises_menu())
    elif call.data == "service_list":
        list = db.get_servises_list()
        markup = types.InlineKeyboardMarkup(row_width=2)
        to_services = types.InlineKeyboardButton("Назад", callback_data='services')
        markup.add(to_services)
        bot.edit_message_text(f"Список \n {list}", call.message.chat.id, call.message.message_id, reply_markup=markup)
    elif call.data == "requests":
        edit_message(call.message, "Выберите вариант", requests_menu())
    elif call.data == "to_start_menu":
        edit_message(call.message, start_txt, start_menu())
    elif  call.data== "request_list":
        markup = types.InlineKeyboardMarkup(row_width=2)
        to_start_menu = types.InlineKeyboardButton("Назад", callback_data='to_start_menu')
        markup.add(to_start_menu)
        edit_message(call.message, "Список пуст", markup)
    else:
        markup = types.InlineKeyboardMarkup(row_width=2)
        to_start_menu = types.InlineKeyboardButton("Назад", callback_data='to_start_menu')
        markup.add(to_start_menu)
        edit_message(call.message, "Список пуст", markup)


@bot.message_handler(content_types="text")
def comands(message):
    text = message.text



if __name__ == '__main__':
    logging.info(">>>>>>>>>> Запуск бота <<<<<<<<<<")
    bot.send_message(cfg.admin_id, "Чтоб не расслаблялся (проверка бота)", parse_mode='Markdown')
    while True:
        # в бесконечном цикле постоянно опрашиваем бота — есть ли новые cообщения
        try:
            bot.polling(none_stop=True, interval=0)
        # если возникла ошибка — сообщаем про исключение и продолжаем работу
        except Exception as e:
            logging.error(f"Ошибка {str(e)}. Попробуйте позже")
