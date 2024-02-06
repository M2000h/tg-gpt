import logging
import time
from multiprocessing import Process
from requests.exceptions import SSLError

import telebot
from environs import Env

from const import *
from gpt import generate_answer
from speech import synthesize, recognize

telebot.apihelper.MAX_RETRIES = 100

env = Env()
env.read_env(".env")

log_format = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(format=log_format, level=logging.INFO)

bot = telebot.TeleBot(env.str("BOT_TOKEN"), threaded=True, num_threads=20, parse_mode="MARKDOWN")

users_status = {}
users_messages = {}


def check_user(bot_handler):
    def wrapper_function(message):
        if message.chat.id not in users_messages.keys():
            users_messages[message.chat.id] = []
            users_status[message.chat.id] = 'auto'
        return bot_handler(message)

    return wrapper_function


def send_action(cid, action):
    while True:
        bot.send_chat_action(cid, action)
        time.sleep(5)


def send_message(cid, text):
    while True:
        try:
            bot.send_message(cid, text)
            break
        except SSLError:
            continue


def send_voice(answer, cid):
    synthesize(answer, "test.mp3")
    audio = open('test.mp3', 'rb')
    bot.send_voice(cid, audio)


def get_answer(cid, text):
    while True:
        try:
            users_messages[cid].append({"role": "user", "content": text})
            answer = generate_answer(users_messages[cid])
            users_messages[cid].append({"role": "assistant", "content": answer})
            return answer
        except Exception:
            time.sleep(1)


@bot.message_handler(commands=['start', 'help'])
@check_user
def command_help(message):
    send_message(message.chat.id, HELLO_TEXT)


@bot.message_handler(commands=['clean'])
def command_clean(message):
    users_messages[message.chat.id] = []
    send_message(message.chat.id, "История очищена.")


@bot.message_handler(commands=['auto'])
@check_user
def command_auto(message):
    users_status[message.chat.id] = 'auto'
    send_message(message.chat.id, "Теперь отвечаю текстом на текст и голосом на голос")


@bot.message_handler(commands=['text'])
@check_user
def command_text(message):
    users_status[message.chat.id] = 'text'
    send_message(message.chat.id, "Теперь отвечаю всегда текстом")


@bot.message_handler(commands=['voice'])
@check_user
def command_voice(message):
    users_status[message.chat.id] = 'voice'
    send_message(message.chat.id, "Теперь отвечаю всегда голосом")


@bot.message_handler(content_types=['text'])
@check_user
def handle_text(message):
    logging.info(f'{message.chat.id}: {message.text}')
    if message.text[0] == "/":
        return
    t1 = Process(target=send_action,
                 args=(message.chat.id, 'record_audio' if users_status.get(message.chat.id) == 'voice' else 'typing'))
    t1.start()
    answer = get_answer(message.chat.id, message.text)
    logging.info(f'{message.chat.id}: {answer[:10]}')
    t1.terminate()
    if users_status.get(message.chat.id) == 'voice':
        send_voice(answer, message.chat.id)
    else:
        send_message(message.chat.id, answer)


@bot.message_handler(content_types=['voice'])
@check_user
def handle_voice(message):
    t1 = Process(target=send_action,
                 args=(message.chat.id, 'typing' if users_status.get(message.chat.id) == 'text' else 'record_audio'))
    t1.start()

    file_info = bot.get_file(message.voice.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open("test.ogg", 'wb') as new_file:
        new_file.write(downloaded_file)

    text = recognize("test.ogg")
    logging.info(f'{message.chat.id}: {text}')

    answer = get_answer(message.chat.id, text)
    logging.info(f'{message.chat.id}: {answer[:10]}')
    t1.terminate()
    if users_status.get(message.chat.id) == 'text':
        send_message(message.chat.id, answer)
    else:
        send_voice(answer, message.chat.id)


if __name__ == '__main__':
    while True:
        try:
            bot.polling()
        except Exception as e:
            logging.error(e)
