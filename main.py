from telebot import TeleBot, types
from PIL import Image

token = open('token.txt').readline()
bot_name = 'my_digits_bot'
markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
bot = TeleBot(token)


digits, str_digits = [i for i in range(10)], [str(i) for i in range(10)]


@bot.message_handler(commands=str_digits)
def message_reply(message):
    text = message.text
    if text in str_digits:
        try:
            img = Image.open(f'digits-photos/{text}.png')
        except FileNotFoundError:
            img = Image.open(f'digits-photos/{text}.jpg')
        bot.send_photo(message.chat.id, img)

    elif text in str_digits and len(text) == 2 and '/' == text[0]:
        try:
            img = Image.open(f'digits-photos/{text[1]}.png')
        except FileNotFoundError:
            img = Image.open(f'digits-photos/{text[1]}.jpg')

        bot.send_photo(message.chat.id, img)

    else:
        img = Image.open(f'digits-photos/wtf-am-i-reading.jpg')

        bot.reply_to(message, 'Choose the digit from 0 to 9', reply_markup=markup)
        bot.send_photo(message.chat.id, img)






if __name__ == '__main__':
    bot.infinity_polling()