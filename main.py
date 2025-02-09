from typing import List, Tuple, Optional, Union, IO, Callable
from telebot import TeleBot, types
from flask import Flask, request
from dotenv import load_dotenv
from patterns import patterns
from io import BytesIO
from PIL import Image
import requests
import logging
import os


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handlers = [logging.StreamHandler(), logging.FileHandler(f'{logger.name}.log')]

for handler in handlers:
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(logging.Formatter('%(levelname)s | %(name)s | %(asctime)s | %(message)s', datefmt='%Y-%m-%d %H:%M:%S'))
    logger.addHandler(handler)


load_dotenv('.env')
bot_name: str = os.getenv('BOT_NAME')
token: str = os.getenv('BOT_TOKEN')
bot = TeleBot(token, threaded=True)
markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

app = Flask(__name__)
webhook_url = f"https://astrotaroelin.com/{token}"

@app.route(f"/{token}", methods=['POST'])
def receive_update():
    json_str = request.get_data().decode('UTF-8')
    update = types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "!", 200


file_objects = dict()


@bot.message_handler()
def message_reply(msg: types.Message) -> Optional[Callable]:
    global message
    message = msg

    logger.info(f'Message is received: {message.text}')

    try:
        data = find_pattern(message.text)
        filename = data

        if filename == 'start_message.txt':
            return send_start_message()
        elif filename == 'commands_list.txt':
            return send_commands_list()

        files = get_file_objects(filename) if isinstance(filename, tuple) else [get_file_object(filename)]
        for file_object, ext in files:
            send_file_by_name_ext(file_object, ext)

    except Exception:
        error_handling()


def preload_files() -> None:
    for key in patterns.keys():
        if '.txt' in key:
            continue

        try:
            filenames = key if isinstance(key, tuple) else [key]
            for filename in filenames:
                file_objects[filename] = open(f'static/{filename}', 'rb')
                logger.info(f'File {filename} has been preloaded.')

        except FileNotFoundError:
            logger.error(f"File {key} not found. Skipping...")

    with open('start_message.txt', 'r') as start:
        with open('commands_list.txt', 'r') as commands:
            global start_message
            global commands_list
            start_message = start.read()
            commands_list = commands.read()


def close_files() -> None:
    for file_object in file_objects.values():
        if file_object:
            file_object.close()
            logger.info(f"File {file_object.name} has been closed")


def find_pattern(input_text: str) -> Union[bool, List[str]]:
    for key, pattern in patterns.items():
        filenames = key if isinstance(key, tuple) else (key)

        output = match_file(input_text, pattern, filenames)
        if output:
            return output

    return False


def match_file(input_text: str, pattern, filenames: List[str]) -> Union[bool, List[str]]:
    if pattern.match(input_text):
        logger.info(f"Matched file/s: {filenames}")

        return filenames
    return False


def get_file_object(filename: str) -> Optional[Tuple[IO[bytes], str]]:
    file_object = file_objects.get(filename)
    ext = filename.split('.')[-1].lower()

    if file_object:
        file_object.seek(0)

        return file_object, ext

    logger.error(f"File object for {filename} not available.")


def get_file_objects(filenames: tuple) -> List[Tuple[IO[bytes], str]]:
    return [get_file_object(filename) for filename in filenames]


def send_file_by_name_ext(file_object: IO[bytes], ext: str) -> None:
    if ext == 'gif':
        bot.send_animation(message.chat.id, file_object)
    elif ext == 'png':
        bot.send_photo(message.chat.id, file_object)
    else:
        image = Image.open(file_object)

        ext ='jpeg' if ext in ['jpg', 'jfif'] else ext
        image = image.convert('RGB') if image.mode == 'RGBA' else image

        image_data = BytesIO()
        image.save(image_data, format=ext.upper())
        image_data.seek(0)

        bot.send_photo(message.chat.id, image)

    logger.info(f'File {file_object.name.split("/")[-1]} has been sent')


def send_start_message() -> None:
    bot.send_message(message.chat.id, start_message)
    logger.info(f'Start Message has been sent')


def send_commands_list() -> None:
    bot.send_message(message.chat.id, commands_list)
    logger.info(f'Commands List has been sent')


def error_handling() -> None:
    logger.info(f'Incorrect message: {message.text}')

    bot.reply_to(message, 'Type jojo reference or any digit from 0 to 9', reply_markup=markup)
    img, ext = get_file_object('Key_Phrases/wtf-am-i-reading.jpg')

    send_file_by_name_ext(img, ext)


if __name__ == '__main__':
    preload_files()

    # bot.infinity_polling()

    bot.remove_webhook()
    bot.set_webhook(url=webhook_url)
    app.run(host='0.0.0.0', port=8443)

    close_files()
