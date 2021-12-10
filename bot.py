import telebot
import config
from picamera import PiCamera
import random
import time
import logging

bot = telebot.TeleBot(config.TOKEN)

camera = PiCamera()
camera.start_preview()
logging.basicConfig(filename="messages.log", level=logging.INFO)
logging.debug("Server started!")
print('Server started!')

TEXT = """Создатель - TimaMine:
Youtube: https://www.youtube.com/channel/UChQhy-RmpGjefYE53rD7S8w
ВК: https://vk.com/timofyata
Новости о боте и голосования: https://t.me/joinchat/V-c4UXcqPqVmY2Vi"""


@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.chat.id, 'Напиши мне Фото для получения фото')


@bot.message_handler(content_types=['text'])
def process_request(message):
    if message.chat.type != 'private':
        return

    text = message.text.lower()
    if text == 'создатель':
        bot.send_message(message.chat.id, 'Мой создатель TimaMine. Напиши "инфо" для подробностей')
    elif message.text == 'stop':
        bot.send_message(message.chat.id, 'Бот останановлен!')
        camera.stop_preview()
        logging.debug("Server stopped")
        bot.stop_bot()
    elif text == 'рандомное число':
        ran = random.randint(1, 100)
        bot.send_message(message.chat.id, ran)
        logging.info(message)
    elif message.text == '📷':
        capture_photo(message)
    elif text in ['foto', 'photo', 'фото']:
        capture_photo(message)
    elif text == 'инфо':
        bot.send_message(message.chat.id, TEXT)
        logging.info(message)
    else:
        logging.info(message)
        bot.send_message(
            message.chat.id,
            'В моих 58 строках чистого кода на Python у меня нет такой команды')


def capture_photo(message):
    time.sleep(0.1)
    camera.capture('/home/pi/bot/cam1.jpg')
    p = open("cam1.jpg", 'rb')
    bot.send_photo(message.chat.id, p)
    logging.info(message)
    
bot.polling(none_stop=True)