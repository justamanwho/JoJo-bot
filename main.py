from telebot import TeleBot, types
from PIL import Image

token = open('token.txt').readline()
bot_name = 'my_digits_bot'
markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
bot = TeleBot(token)


digits, str_digits = [i for i in range(10)], [str(i) for i in range(10)]


def error_handling(message):
    img = Image.open(f'digits-photos/wtf-am-i-reading.jpg')

    bot.reply_to(message, 'Choose the digit from 0 to 9', reply_markup=markup)
    bot.send_photo(message.chat.id, img)


@bot.message_handler()
def message_reply(message):
    text = message.text
    if text in str_digits:
        try:
            img = Image.open(f'digits-photos/{text}.png')
        except FileNotFoundError:
            try:
                img = Image.open(f'digits-photos/{text}.jpg')
            except FileNotFoundError:
                return error_handling(message)

        bot.send_photo(message.chat.id, img)

    elif len(text) == 2 and '/' == text[0] and text[1] in str_digits:
        try:
            img = Image.open(f'digits-photos/{text[1]}.png')
        except FileNotFoundError:
            try:
                img = Image.open(f'digits-photos/{text[1]}.jpg')
            except FileNotFoundError:
                return error_handling(message)

        bot.send_photo(message.chat.id, img)
    else:
        error_handling(message)


if __name__ == '__main__':
    bot.infinity_polling()