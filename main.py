from telebot import TeleBot, types
from io import BytesIO
from PIL import Image
import logging
from patterns import patterns


logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.DEBUG,
    format='%(levelname)s | %(name)s | %(asctime)s | %(message)s',
    datefmt='%H:%M:%S'
)
file_handler = logging.FileHandler(f'{logger.name}.log')
logger.addHandler(file_handler)


bot_name = 'my_digits_bot'
token = open('token.txt').readline()
bot = TeleBot(token, threaded=True)
markup = types.ReplyKeyboardMarkup(resize_keyboard=True)


file_objects = dict()


@bot.message_handler()
def message_reply(msg):
    global message
    message = msg

    logger.info(f'Message is received: {message.text}')

    try:
        data = find_pattern(message.text)
        filename = data

        if filename == 'README.md':
            return send_start_message()

        files = get_file_objects(filename) if isinstance(filename, tuple) else [get_file_object(filename)]
        for file in files:
            object, ext = file
            send_file_by_name_ext(object, ext)

    except Exception:
        error_handling()


def preload_files() -> None:
    # Getting ready all files
    for key in patterns.keys():
        try:
            filenames = key if isinstance(key, tuple) else [key]
            for filename in filenames:
                file_objects[filename] = open(f'static/{filename}', 'rb')
                logger.info(f'File {filename} has been preloaded.')

        except FileNotFoundError:
            logger.error(f"File {key} not found. Skipping...")

    # Getting ready start message
    with open('README.md', 'r') as readme:
        global start_message
        start_message = readme.read()


def close_files() -> None:
    for file_object in file_objects.values():
        if file_object:
            file_object.close()
            logger.info(f"File {file_object.name} has been closed")


def find_pattern(input_text):
    for key, pattern in patterns.items():
        filenames = key if isinstance(key, tuple) else (key)

        output = match_file(input_text, pattern, filenames)
        if output:
            return output

    return False


def match_file(input_text, pattern, filenames):
    if pattern.match(input_text):
        logger.info(f"Matched file/s: {filenames}")

        return filenames
    return False


def get_file_object(filename: str):
    file_object = file_objects.get(filename)
    ext = filename.split('.')[-1].lower()

    if file_object:
        file_object.seek(0)

        return file_object, ext

    logger.error(f"File object for {filename} not available.")


def get_file_objects(filenames):
    return [get_file_object(filename) for filename in filenames]


def send_file_by_name_ext(file_object, ext: str) -> None:
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


def send_start_message():
    bot.send_message(message.chat.id, start_message)
    logger.info(f'Start Message has been sent')


def error_handling():
    logger.info(f'Incorrect message: {message.text}')

    bot.reply_to(message, 'Choose the digit from 0 to 9', reply_markup=markup)
    img, ext = get_file_object('Key_Phrases/wtf-am-i-reading.jpg')

    send_file_by_name_ext(img, ext)


if __name__ == '__main__':
    preload_files()
    bot.infinity_polling()
    close_files()

# Note for the next time coding
# I want to put annotations for every function
