from telebot import TeleBot, types
from io import BytesIO
from PIL import Image
import logging
import re


data = {
    'README.md': re.compile('.*(s+t+a+r+t|h+e+l+p).*', re.IGNORECASE),

    # Key Phrases

    'your-next-line.png': re.compile(r'.*(a+m+[\W]*i+[\W]*r+e+a+d+i+n|w+h+a+t+[\W]*t+h+e+[\W]*f+u+c+k+|w+t+f'
                                     r'|w+h+a+t+[\W]*a+r+e+[\W]*y+o+u+[\W]*t+a+l+k+i+n+g+[\W]*a+b+o+u+t).*',
                                     re.IGNORECASE),

    ('the-world.png', 'the-world.gif'): re.compile(r'.*(t+h+e+[\W]*w+o+r+l+d+|z+a+[\W]*w+a+r+u+d+o).*', re.IGNORECASE),

    'omg.jpg': re.compile(r'.*(o+m+g|o+(h+)?[\W]*m+y+[\W]*g+o+d+|o+(h+)?[\W]*s+h+i+t[\W]*).*', re.IGNORECASE),

    'dio-hoho.png': re.compile(r'.*(h+o+[\W]*h+o+|o+h+[\W]*h+o+).*', re.IGNORECASE),

    'yare-yare.jpg': re.compile(r'.*(y+a+r+e+[\W]*ya+re+[\W]*(daze|dawa)?|good grief).*', re.IGNORECASE),

    'hayato.jfif': re.compile(r'.*(h+a+y+a+t+o).*', re.IGNORECASE),

    'yaro.jfif': re.compile(r'.*(y+a+r+o).*', re.IGNORECASE),

    'egg.png': re.compile(r'.*(e+a+s+t+e+r+[\W]*|(egg|eggs)).*', re.IGNORECASE),

    'Rohan.jpg': re.compile(r'.*(R+o+h+a+n|K+i+s+h+i+b+e|H+o+w+[\W]*d+o+e+s+[\W]*i+t+[\W]*t+a+s+t+e).*', re.IGNORECASE),

    'wryyy.png': re.compile(r'.*(W+R+YY*).*', re.IGNORECASE),

    'my-reaction-when-I-saw-Josuke8.jpg': re.compile(r'.*((O+I+|H*E+Y+|Y+O+)[\W]*J+O+S+U+K+E).*', re.IGNORECASE),

    'i-see.png': re.compile(r'.*(I+[\W]*see+).*', re.IGNORECASE),

    'rero-rero.jpg': re.compile(r'.*(r+e+r+o|r+e+r+e|l+e+r+o|l+e+r+e).*', re.IGNORECASE),

    'your-underwear-is-showing.gif': re.compile(r'.*(Y+o+u+r*[\W]*U+n+d+e+r+w+e*a*r+([\W]*I+s+)?[\W]*S+h+o+w+i+n+g*'
                                                r'|I+[\W]*C+a+n+[\W]*S+e+e+[\W]*Y+o+u+r*[\W]*U+n+d+e+r+w+e*a*r).*',
                                                re.IGNORECASE),

    'stares.jpg': re.compile(r'.*(s+t+a+r+e+s*|e+y+e+s).*', re.IGNORECASE),

    'yes-i-am.png': re.compile(r'.*(Y+e+s+[\W]*I+[\W]*A+m).*', re.IGNORECASE),

    'you-are-annoying.png': re.compile(r'.*(S+h+u+t+[\W]*(T+h+e+[\W]*F+u+c+k+[\W]*)?U+p+|Y+o+u+[\W]*a+r+e+[\W]*'
                                       r'(d+a+m+n+[\W]*)a+n+n*o+y+i+n+g*|Y+a+k+a+m+a+s+h+i).*', re.IGNORECASE),

    'nigerundayo.jpg': re.compile(r'.*(N+i+g+e+r+u|R+u+n).*', re.IGNORECASE),

    'ambulance.png': re.compile(r'.*(A+m+b+u+l+a+n+c+e).*', re.IGNORECASE),

    'road-roller.jpg': re.compile('.*(R+o+A+d+[\W]*R+o+L+L*e+R).*', re.IGNORECASE),

    'kono-dio-da.avif': re.compile('.*(K+o+n+o+[\W]*D+i+o+[\W]*D+a).*', re.IGNORECASE),

    'tururu.png': re.compile('.*(T+u+r+u+r*u*).*', re.IGNORECASE),

    'lali-ho.jpg': re.compile('.*(L+a+l+i+[\W]*h+o+).*', re.IGNORECASE),


    # Every JoJo

    'Jonathan.png': re.compile(r'.*(J+o+e+s+t+a+r|J+o+n+a+t+h+a+n|J+o+J+o+[\W]*1).*', re.IGNORECASE),

    'Joseph.png': re.compile(r'.*(J+o+s+e+p+h|J+o+J+o+[\W]*2).*', re.IGNORECASE),

    'Jotaro.png': re.compile(r'.*(K+u+j+o|J+o+t+a+r+o|J+o+J+o+[\W]*3).*', re.IGNORECASE),

    'Josuke-4.png': re.compile(r'.*(H+i+g+a+s+h+i+k+a+t+a|J+o+s+u+k+e(?![\W]*8+)|J+o+J+o+[\W]*4).*', re.IGNORECASE),

    'Giorno.jpg': re.compile(r'.*(G+i+o+r+n+o|G+i+o+v+a+n+n+a|J+o+J+o+[\W]*5).*', re.IGNORECASE),

    'Jolyne.png': re.compile(r'.*(J+o+l+y+n|C+u+j+o+h|J+o+J+o+[\W]*6).*', re.IGNORECASE),

    'Johnny.png': re.compile(r'.*(J+o+h*n+y|J+o+J+o+[\W]*7).*', re.IGNORECASE),

    'Josuke-8.jpg': re.compile(r'.*(J+o+s+u+k+e+8*|J+o+J+o+[\W]*8).*', re.IGNORECASE),

    'Jodio.png': re.compile(r'.*(J+o+d+i+o|J+o+J+o+[\W]*9).*', re.IGNORECASE),

    'jojo.jpg': re.compile(r'.*(J+o+J+o+).*', re.IGNORECASE),


    # Every Villain

    'Dio-1.png': re.compile(r'.*(B+r+a+n+d+o(?!3)|D+I+O+1).*', re.IGNORECASE),

    'Kars.png': re.compile(r'.*(K+a+r+s).*', re.IGNORECASE),

    'Dio-3.png': re.compile(r'.*(D+I+O|B+r+a+n+d+o+3).*', re.IGNORECASE),

    'Kira-Yoshikage-1.png': re.compile(r'.*(K+i+r+a(?!2)|Y+o+s+h+i+k+a+g+e(?!2)).*', re.IGNORECASE),

    'Kira-Yoshikage-2.png': re.compile(r'.*(K+o+s+a+k+u|K+a+w+a+j+i+r+i|K+i+r+a+2|Y+o+s+h+i+k+a+g+e+2).*', re.IGNORECASE),

    'Diavolo.jpg': re.compile(r'.*(D+i+a+v+o+l+o).*', re.IGNORECASE),

    'Doppio.jpg': re.compile(r'.*(D+o+p+p*i+o).*', re.IGNORECASE),

    'Pucci.jpg': re.compile(r'.*(P+u+c+c*i).*', re.IGNORECASE),

    'Valentine.png': re.compile(r'.*(F+u+n+n+y|V+a+l+e+n+t+i+n+e).*', re.IGNORECASE),


    # Stands

    'the-world.png': re.compile(r'.*(T+h+e+[\W]*W+o+r+l+d).*', re.IGNORECASE),


    # Responses on Digits

    '0.gif': re.compile(r'.?0.?'), '1.png': re.compile(r'.?1.?'), '2.jpg': re.compile(r'.?2.?'),
    '3.jpg': re.compile(r'.?3.?'), '4.jpg': re.compile(r'.?4.?'), '5.jpg': re.compile(r'.?5.?'),
    '6.jpg': re.compile(r'.?6.?'), '7.png': re.compile(r'.?7.?'), '8.jpg': re.compile(r'.?8.?'),
    '9.png': re.compile(r'.?9.?'),

    # Error Handling

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

    data = find_pattern(message, message.text)

    if data:
        message, filename = data

        if filename != 'README.md':
            if isinstance(filename, tuple):
                files = get_file_objects(message, filename)

                for file in files:
                    message, object, ext = file
                    send_file_by_name_ext(message, object, ext)

            else:
                file = get_file_object(message, filename)

                message, object, ext = file
                send_file_by_name_ext(message, object, ext)

        else:
            return send_start_message(message)

    else:
        return error_handling(message)


def preload_files() -> None:
    # Getting ready all files
    for key in data.keys():
        try:
            if isinstance(key, tuple):
                for filename in key:
                    put_objects(filename)
            else:
                put_objects(key)

        except FileNotFoundError:
            logger.error(f"File {key} not found. Skipping...")

    # Getting ready start message
    with open('README.md', 'r') as readme:
        global start_message
        start_message = readme.read()


def put_objects(filename):
    file_objects[filename] = open(f'static/{filename}', 'rb')
    logger.info(f'File {filename} has been preloaded.')


def close_files() -> None:
    for file_object in file_objects.values():
        if file_object:
            file_object.close()
            logger.info(f"File {file_object.name} has been closed")


def find_pattern(message, input_text):
    for key, pattern in data.items():
        filenames = key if isinstance(key, tuple) else (key)

        output = match_file(message, input_text, pattern, filenames)
        if output:
            return output

    return False


def match_file(message, input_text, pattern, filenames):
    if pattern.match(input_text):
        logger.info(f"Matched file/s: {filenames}")

        return message, filenames
    return False


def get_file_object(message, filename):
    file_object = file_objects.get(filename)
    ext = filename.split('.')[-1].lower()

    if file_object:
        file_object.seek(0)

        return message, file_object, ext
    else:
        logger.error(f"File object for {filename} not available.")


def get_file_objects(message, filenames):
    files = []
    for filename in filenames:
        files.append(get_file_object(message, filename))

    return files


def send_file_by_name_ext(message, file_object, ext):
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


def send_start_message(message):
    bot.send_message(message.chat.id, start_message)
    logger.info(f'Start Message has been sent')

    return True


def error_handling(message):
    logger.info(f'Incorrect message: {message.text}')

    bot.reply_to(message, 'Choose the digit from 0 to 9', reply_markup=markup)
    message, img, ext = get_file_object(message, 'wtf-am-i-reading.jpg')

    return send_file_by_name_ext(message, img, ext)


if __name__ == '__main__':
    preload_files()
    bot.infinity_polling()
    close_files()
