import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import config as cfg


def send_email(email_to, subject, message):
    msg = MIMEMultipart()  # Создаем сообщение
    msg['From'] = cfg.email_address  # Адресат
    msg['To'] = email_to  # Получатель
    msg['Subject'] = subject
    body = message
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP_SSL('smtp.yandex.ru', 465)
    try:
        # server.ehlo()
        # server.starttls()
        # server.ehlo()
        server.login(cfg.email_address, cfg.email_password)
        server.send_message(msg)
    finally:
        server.quit()
