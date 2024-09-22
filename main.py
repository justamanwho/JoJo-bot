from telebot import TeleBot, types
from PIL import Image
import re
from io import BytesIO
import logging


data = {
    'your-next-line.png': re.compile(r'.*(a+m+[\W]*i+[\W]*r+e+a+d+i+n+(g+)?|w+h+a+t+[\W]*t+h+e+[\W]*f+u+c+k+|w+t+f+)[\W]*'
                                     r'(a+m+[\W]*i+[\W]*r+e+a+d+i+n+(g+)?)?[\W,?]*|'
                                     r'(a+m+[\W]*i+[\W]*r+e+a+d+i+n+(g+)?)?\s*(w+h+a+t+[\W]*t+h+e[\W]*f+u+c+k+|w+t+f)'
                                     r'[\W,?]*|(w+h+a+t+[\W]*a+r+e+[\W]*y+o+u+[\W]*t+a+l+k+i+n+g+[\W]*a+b+o+u+t).*',
                                     re.IGNORECASE),

    'the-world.gif': re.compile(r'.*(t+h+e+[\W]*w+o+r+l+d+|z+a+[\W]*w+a+r+u+d+o).*', re.IGNORECASE),

    'omg.jpg': re.compile(r'.*(o+m+g|o+(h+)?[\W]*m+y+[\W]*g+o+d+|o+(h+)?[\W]*s+h+i+t[\W]*).*', re.IGNORECASE),

    'dio-hoho.png': re.compile(r'.*(h+o+[\W]*h+o+|o+h+[\W]*h+o+).*', re.IGNORECASE),

    'yare-yare.jpg': re.compile(r'.*(y+a+r+e+[\W]*ya+re+[\W]*(daze|dawa)?|good grief).*', re.IGNORECASE),

    'hayato.jfif': re.compile(r'.*(h+a+y+a+t+o).*', re.IGNORECASE),

    'yaro.jfif': re.compile(r'.*(y+a+r+o).*', re.IGNORECASE),

    'egg.png': re.compile(r'.*(e+a+s+t+e+r+[\W]*|(egg|eggs)).*', re.IGNORECASE),

    'jojo.jpg': re.compile(r'.*(J+o+J+o+).*', re.IGNORECASE),

    'Jonathan.png': re.compile(r'.*(J+o+e+s+t+a+r|J+o+n+a+t+h+a+n|J+o+J+o+[\W]1).*', re.IGNORECASE),

    'Joseph.png': re.compile(r'.*(J+o+s+e+p+h|J+o+J+o+[\W]2).*', re.IGNORECASE),

    'Jotaro.png': re.compile(r'.*(K+u+j+o|J+o+t+a+r+o|J+o+J+o+[\W]3).*', re.IGNORECASE),

    'Josuke-4.png': re.compile(r'.*(H+i+g+a+s+h+i+k+a+t+a|J+o+s+u+k+e|J+o+J+o+[\W]4).*', re.IGNORECASE),

    'Giorno.jpg': re.compile(r'.*(G+i+o+r+n+o|G+i+o+v+a+n+n+a|J+o+J+o+[\W]5).*', re.IGNORECASE),

    'Jolyne.png': re.compile(r'.*(J+o+l+y+n|C+u+j+o+h|J+o+J+o+[\W]6).*', re.IGNORECASE),

    'Johnny.png': re.compile(r'.*(J+o+h*n+y|J+o+J+o+[\W]7).*', re.IGNORECASE),

    'Josuke-8.jpg': re.compile(r'.*(J+o+J+o+[\W]8).*', re.IGNORECASE),

    'Jodio.png': re.compile(r'.*(J+o+d+i+o|J+o+J+o+[\W]9).*', re.IGNORECASE),

    '0.gif': re.compile(r'.?0.?'), '1.png': re.compile(r'.?1.?'), '2.jpg': re.compile(r'.?2.?'),
    '3.jpg': re.compile(r'.?3.?'), '4.jpg': re.compile(r'.?4.?'), '5.jpg': re.compile(r'.?5.?'),
    '6.jpg': re.compile(r'.?6.?'), '7.png': re.compile(r'.?7.?'), '8.jpg': re.compile(r'.?8.?'),
    '9.png': re.compile(r'.?9.?'),

    'wtf-am-i-reading.jpg': re.compile(r'.*(j+u+s+t+[\W]*g+i+v+e+[\W]*m+e+[\W]*J+o+s+u+k+e).*', re.IGNORECASE)
}

file_objects = dict()


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


@bot.message_handler()
def message_reply(message):
    logger.info(f'Message is received: {message.text}')

    data = match_file(message, message.text)
    if data:
        message, filename = data
        file_object = get_file_object(message, filename)

        message, file, ext = file_object
        return send_by_name_ext(message, file, ext)

    return error_handling(message)


def preload_files() -> None:
    for filename in data.keys():
        try:
            file_objects[filename] = open(f'static/{filename}', 'rb')
            logger.info(f'File {filename} has been preloaded.')
        except FileNotFoundError:
            logger.error(f"File {filename} not found. Skipping...")


def close_files() -> None:
    for file_object in file_objects.values():
        if file_object:
            file_object.close()
            logger.info(f"File {file_object.name} has been closed")


def match_file(message, input_text):
    for filename, pattern in data.items():
        if pattern.match(input_text):
            logger.info(f"Matched file: {filename}")

            return message, filename
    return False


def get_file_object(message, filename):
    file_object = file_objects.get(filename)
    ext = filename.split('.')[-1].lower()

    if file_object:
        file_object.seek(0)

        return message, file_object, ext
    else:
        logger.error(f"File object for {filename} not available.")


def send_by_name_ext(message, file_object, ext):
    if ext == 'gif':
        return bot.send_animation(message.chat.id, file_object)
    else:
        image = Image.open(file_object)

        ext ='jpeg' if ext in ['jpg', 'jfif'] else ext
        image = image.convert('RGB') if image.mode == 'RGBA' else image

        image_data = BytesIO()
        image.save(image_data, format=ext.upper())
        image_data.seek(0)

        bot.send_photo(message.chat.id, image)

        logger.info(f'Image {file_object.name} has been sent')
        return True


def error_handling(message):
    logger.info(f'Incorrect message: {message.text}')

    bot.reply_to(message, 'Choose the digit from 0 to 9', reply_markup=markup)
    message, img, ext = get_file_object(message, 'wtf-am-i-reading.jpg')

    return send_by_name_ext(message, img, ext)


if __name__ == '__main__':
    preload_files()
    bot.infinity_polling()
    close_files()
