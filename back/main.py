import datetime

import requests
import telebot
import logging
import psycopg2

today = datetime.datetime.today().date()

logfile = f"./logs/telegram_bots_{today}.log"

logging.basicConfig(
    level=logging.INFO,
    filename=logfile,
    filemode="a",
    format="%(asctime)s %(levelname)s %(message)s",
)

# указываем токен для доступа к боту
bot = telebot.TeleBot('8009291856:AAFtF0TisGF12wikh_t-AHFoZL739UCIoF0')
start_txt = 'Привет! \n\nТеперь можете работать с ботом "БухгалтерИя".'


@bot.message_handler(commands=['start'])
def start(message):
    # выводим приветственное сообщение
    logging.info(f"Пользователь {message.from_user.username} запустил бота")
    bot.send_message(message.from_user.id, start_txt, parse_mode='Markdown')


@bot.message_handler(commands=['services_list'])
def services_list(message):
    servisec_list="Пока ничего нет"
    logging.info(f"Пользователь {message.from_user.username} запросил список услуг")
    bot.send_message(message.from_user.id, servisec_list, parse_mode='Markdown')


@bot.message_handler(commands=['services_add'])
def service_add(message):
    bot.send_message(message.from_user.id, "Пока ничего нельзя добавить", parse_mode='Markdown')

@bot.message_handler(commands=['services_delete'])
def service_delete(message):
    bot.send_message(message.from_user.id, "Пока ничего нельзя удалить", parse_mode='Markdown')



if __name__ == '__main__':
    logging.info(">>>>>>>>>> Запуск бота <<<<<<<<<<")
    while True:

        # в бесконечном цикле постоянно опрашиваем бота — есть ли новые cообщения
        try:
            bot.polling(none_stop=True, interval=0)
        # если возникла ошибка — сообщаем про исключение и продолжаем работу
        except Exception as e:
            print(f"Ошибка {str(e)}. Попробуйте позже")
