import datetime

import requests
import telebot
from telebot import types
import logging
import database_records as db
import config as cfg
import re

today = datetime.datetime.today().date()

logfile = f"./logs/telegram_bots_{today}.log"

logging.basicConfig(
    level=logging.INFO,
    filename=logfile,
    filemode="a",
    format="%(asctime)s %(levelname)s %(message)s",
)

# class Messages:
#
#
#
#
# class Services:
#     def __init__(self, service_name):
#         self.service_name = service_name
#
#     def

class Menu:
    def zero_button():
        return types.InlineKeyboardMarkup(row_width=2)

    # Набор кнопок для старта
    def start():
        markup = types.InlineKeyboardMarkup(row_width=2)
        services = types.InlineKeyboardButton("Услуги", callback_data='services')
        requests = types.InlineKeyboardButton("Заявки", callback_data='requests')
        markup.add(services, requests)
        return markup

    def to_start():
        markup = types.InlineKeyboardMarkup(row_width=2)
        to_start_menu = types.InlineKeyboardButton("\U00002B05 Назад", callback_data='to_start_menu')
        markup.add(to_start_menu)
        return markup

    # Набор кнопок для "Услуги"
    def servises():
        markup = types.InlineKeyboardMarkup(row_width=2)
        services_list = types.InlineKeyboardButton("\U0001F4C3 Список услуг", callback_data='service_list')
        services_add = types.InlineKeyboardButton("\U0000270D Добавить услугу", callback_data='service_add')
        service_edit = types.InlineKeyboardButton("\U0000270F Редактировать услугу", callback_data='service_edit')
        service_delete = types.InlineKeyboardButton("\U0001F5D1 Удалить услугу", callback_data='service_delete')
        to_start_menu = types.InlineKeyboardButton("\U00002B05 Назад", callback_data='to_start_menu')
        markup.add(services_list, services_add, service_edit, service_delete, to_start_menu)
        return markup

    def to_service():
        markup = types.InlineKeyboardMarkup(row_width=2)
        to_services = types.InlineKeyboardButton("Назад", callback_data='services')
        markup.add(to_services)
        return markup

    # Набор кнопок для "Заявки"
    def requests():
        markup = types.InlineKeyboardMarkup(row_width=1)
        request_list = types.InlineKeyboardButton("Список заявок", callback_data='request_list')
        to_start_menu = types.InlineKeyboardButton("\U00002B05 Назад", callback_data='to_start_menu')
        markup.add(request_list, to_start_menu)
        return markup


class Services:
    class add:
        def name(message):
            service_add_list['service_name'] = message.text
            add = bot.send_message(message.chat.id, "Введите стоимость")
            bot.register_next_step_handler(add, Services.add.price)
        def price(message):
            # bot.register_next_step_handler(send_message(message, "Неверный формат цены", zero_button()), service_price)
            service_add_list['service_price'] = message.text
            markup = Menu.zero_button()
            services_buh = types.InlineKeyboardButton("Бухгалтерия", callback_data='buh')
            services_law = types.InlineKeyboardButton("Юриспруденция", callback_data="law")
            markup.add(services_buh, services_law)
            send_message(message, "Выберите вид услуги", markup)
        def save(name, price, type):
            return db.add_service(name, int(price), type)
    class edit:
        def name(message):
            if message.text == "Отмена":
                send_message(message, "Список доступных услуг", Menu.servises())
            service_edit['name'] = message.text
            if db.get_service(message.text) != "":
                markup = Menu.servises()
                service_edit_name = types.InlineKeyboardButton("Название", callback_data="service_edit_name")
                service_edit_price = types.InlineKeyboardButton("Цена", callback_data="service_edit_price")
                markup.add(service_edit_name, service_edit_price)
                send_message(message, "Выберите что изменить", markup)
            else:
                edit = bot.send_message(call.message.chat.id, " Услуга не найдена \n Введите название услуги или напишите \"Отмена\"")
                bot.register_next_step_handler(edit, Services.edit.name)

        def save(message):
            if db.edit_service(service_edit['name'], service_edit['type'], message.text):
                send_message(message, "\U00002705 Изменнения успешно сохранены", Menu.to_service())
            else:
                send_message(message, '\U0001F625 Возникли ошибки при сохранении изменений', Menu.to_service())
    class delete:
        def name(message):
            name_delete = message.text
            if name_delete == "Отмена":
                send_message(message, "Меню услуги", Menu.servises())
                return
            service = db.get_service(name_delete)
            if service != "":
                delete = bot.send_message(message.chat.id,
                                          f"Вы уверенны, что хотите удалить следующую услугу (напишите Да)? \n {service}")
                bot.register_next_step_handler(delete, Services.delete.save, message.text)
            else:
                delete = bot.send_message(message.chat.id,
                                          "Услуга не найдена \n Введите название услуги или напишите \"Отмена\"")
                bot.register_next_step_handler(delete, Services.delete.name)

        def save(message, name):
            if message.text == "Да":
                if db.delete_service(name):
                    send_message(message, "\U00002705 Услуга удалена", Menu.to_service())
                else:
                    send_message(message, '\U0001F625 Возникли ошибки при удалении', Menu.to_service())
            else:
                send_message(message, "Выберите вариант", Menu.servises())


service_add_list={
    'service_name':'',
    'service_price':''
}
service_edit = {
    'type':'',
    'name':''
}

#regex
price_regex = "[0-9]"

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
    send_message(message, start_txt, Menu.start())

#Обработчик нажатых кнопок
@bot.callback_query_handler(func=lambda call: True)
def check_callback_data(call):
    if call.data == "services":
        edit_message(call.message, "Выберите вариант", Menu.servises())
    elif call.data == "service_list":
        list = db.get_servises_list()
        edit_message(call.message, f"Список \n {list}", Menu.to_service())
    elif call.data=="service_add":
        add = bot.send_message(call.message.chat.id, "Введите название услуги")
        bot.register_next_step_handler(add, Services.add.name)
    elif call.data == "requests":
        edit_message(call.message, "Выберите вариант", Menu.requests())
    elif call.data == "to_start_menu":
        edit_message(call.message, start_txt, Menu.start())
    elif call.data in ("buh", "law"):
        name = service_add_list['service_name']
        price = service_add_list['service_price']
        if Services.add.save(name, price, call.data):
            send_message(call.message, "\U00002705 Услуга добавлена", Menu.to_service())
        else:
            send_message(call.message, "\U0001F625 Ошибка добавления услуги", Menu.to_service())
    elif call.data == "service_edit":
        edit = bot.send_message(call.message.chat.id, "Введите название услуги")
        bot.register_next_step_handler(edit, Services.edit.name)
    elif call.data in ("service_edit_name", "service_edit_price"):
        service_edit["type"] = "name" if call.data=="service_edit_name" else "price"
        edit = bot.send_message(call.message.chat.id, "Введите новое значение")
        bot.register_next_step_handler(edit, Services.edit.save)
    elif call.data == "service_delete":
        delete = bot.send_message(call.message.chat.id, "Введите название услуги")
        bot.register_next_step_handler(delete, Services.delete.name)
    elif  call.data== "request_list":
        edit_message(call.message, "Список пуст", Menu.to_start())
    else:
        edit_message(call.message, "Список пуст", Menu.to_start())


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
