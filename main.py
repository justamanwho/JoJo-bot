from telebot import TeleBot, types
from PIL import Image
import re


token = open('token.txt').readline()
bot_name = 'my_digits_bot'
markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
bot = TeleBot(token)


digits, str_digits = [i for i in range(10)], [str(i) for i in range(10)]


def error_handling(message):
    bot.reply_to(message, 'Choose the digit from 0 to 9', reply_markup=markup)

    return send_photo_by_name_extention(message, 'wtf-am-i-reading', 'jpg')


def wtf_reading(text, message):
    pattern = re.compile(
        r'(am\s*i\s*reading|what\s*the\s*fuck|wtf)\s*(am\s*i\s*reading)?[\s,?]*|'
        r'(am\s*i\s*reading)?\s*(what\s*the\s*fuck|wtf)[\s,?]*|'
        r'(what\s*are\s*you\s*talking\s*about)',
        re.IGNORECASE
    )

    if pattern.match(text):
        # change func name
        return send_photo_by_name_extention(message, 'your_next_line', 'png')

    return False


# make gif load faster
def the_world(text, message):
    # make it re
    message_possibilities = ['the world', 'za warudo', 'the world!', 'za warudo!']

    if text.lower() in message_possibilities:
        send_photo_by_name_extention(message, 'jojo-the-world', 'gif')
        return True

    return False


def omg(text, message):
    pattern = re.compile(
        r'\s*(omg|oh[\W]*my[\W]*god|oh[\W]*shit[\W]*)\s*!?',
        re.IGNORECASE
    )

    if pattern.match(text):
        return send_photo_by_name_extention(message, 'omg', 'jpg')

    return False



def yare_yare(text, message):
    pattern = re.compile(r'(yare+\s*?yare+\s?|daze)', re.IGNORECASE)

    if pattern.match(text):
        return send_photo_by_name_extention(message, 'yare-yare', 'jpg')

    return False


def send_photo_by_name(message, name):
    extensions = ['jpg', 'png', 'gif']

    for ext in extensions:
        try:
            return send_photo_by_name_extention(message, name, ext)
        except FileNotFoundError:
            continue

    return error_handling(message)


def send_photo_by_name_extention(message, name, ext):
    img = Image.open(f'static/{name}.{ext}')

    if ext == 'gif':
        with open(f'static/{name}.{ext}', 'rb') as gif_file:
            return bot.send_animation(message.chat.id, gif_file)
    else:
        return bot.send_photo(message.chat.id, img)


@bot.message_handler()
def message_reply(message):
    text = message.text
    if text in str_digits:
        send_photo_by_name(message, text)

    elif len(text) == 2 and text[1] in str_digits:
        send_photo_by_name(message, text[1])

    elif wtf_reading(message.text, message):
        return

    elif the_world(message.text, message):
        return

    elif omg(message.text, message):
        return

    elif yare_yare(message.text, message):
        return

    else:
        error_handling(message)


if __name__ == '__main__':
    bot.infinity_polling()
