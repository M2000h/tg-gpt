from speech import synthesize, recognize
from requests.exceptions import SSLError
from multiprocessing import Process
from telebot.types import Message
from gpt import generate_answer
from environs import Env
from const import *
import telebot
import logging
import time

telebot.apihelper.MAX_RETRIES = 100

env = Env()
env.read_env(".env")

log_format = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(format=log_format, level=logging.INFO)

bot = telebot.TeleBot(env.str("BOT_TOKEN"), threaded=True, num_threads=20, parse_mode="MARKDOWN")

users_status = {}
users_messages = {}


def send_message(cid: int, text: str) -> None:
	"""
	Safe way to send message throw network errors
	:param cid: chat id
	:type cid: int
	:param text: message text
	:type text: str
	"""
	while True:
		try:
			bot.send_message(cid, text)
			return
		except SSLError:
			continue


def send_action(cid: int, action: str) -> None:
	"""
	Set bot current action like "typing" or "record_audio"
	:param cid: chat id
	:type cid: int
	:param action: "typing" or "record_audio"
	:type action: str
	"""
	while True:
		bot.send_chat_action(cid, action)
		time.sleep(5)


def send_voice(text: str, cid: int) -> None:
	"""
	Sends voice message
	:param text: text for synthesize and send
	:type text: str
	:param cid: chat id
	:type cid: int
	"""
	synthesize(text, "test.mp3")
	audio = open('test.mp3', 'rb')
	bot.send_voice(cid, audio)


def get_answer(cid: int, text: str) -> str:
	"""
	Generate answer from GPT
	:param cid: chat id
	:type cid: str
	:param text: user's last message text
	:type text: str
	:return: answer from GPR
	:rtype: str
	"""
	if not users_messages.get(cid):
		users_messages[cid] = []
	users_messages[cid].append({"role": "user", "content": text})
	answer = generate_answer(users_messages[cid])
	users_messages[cid].append({"role": "assistant", "content": answer})
	return answer


@bot.message_handler(commands=['start', 'help'])
def command_help(message: Message) -> None:
	"""
	/start ans /help command handler
	:param message: message object
	:type message: Message
	"""
	send_message(message.chat.id, HELLO_TEXT)


@bot.message_handler(commands=['clean'])
def command_clean(message: Message) -> None:
	"""
	/clean command handler. Cleans user's messages history.
	:param message: message object
	:type message: Message
	"""
	users_messages[message.chat.id] = []
	send_message(message.chat.id, "История очищена.")


@bot.message_handler(commands=['auto'])
def command_auto(message: Message) -> None:
	"""
	/auto command handler. Set auto mode for bot answering.
	:param message: message object
	:type message: Message
	"""
	users_status[message.chat.id] = 'auto'
	send_message(message.chat.id, "Теперь отвечаю текстом на текст и голосом на голос")


@bot.message_handler(commands=['text'])
def command_text(message: Message) -> None:
	"""
	/text command handler. Set text mode for bot answering.
	:param message: message object
	:type message: Message
	"""
	users_status[message.chat.id] = 'text'
	send_message(message.chat.id, "Теперь отвечаю всегда текстом")


@bot.message_handler(commands=['voice'])
def command_voice(message: Message):
	"""
	/voice command handler. Set voice mode for bot answering.
	:param message: message object
	:type message: Message
	"""
	users_status[message.chat.id] = 'voice'
	send_message(message.chat.id, "Теперь отвечаю всегда голосом")


@bot.message_handler(content_types=['text'])
def handle_text(message: Message) -> None:
	"""
	Message main handler. Getting message from user, and sends answer (text or audio depends on mode)
	:param message: user's message
	:type message: Message
	"""
	logging.info(
		f'{message.from_user.first_name} {message.from_user.last_name} ({message.from_user.username}): {message.text}')
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
def handle_voice(message: Message) -> None:
	"""
	Voice message main handler. Getting message from user, and sends answer (text or audio depends on mode)
	:param message: user's voice message
	:type message: Message
	"""
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
	"""
	Time for OpenVPN starts
	"""
	time.sleep(5)
	bot.polling(True, timeout=5)
