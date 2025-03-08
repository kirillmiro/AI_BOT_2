import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from config import TOKEN
from logic import get_class

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, '''Привет! Отправь мне картинку собаки, и я скажу, настоящая эта картинка или сгенерированна AI.''')


@bot.message_handler(content_types=['photo'])
def get_photo(message):
    if not message.photo:
        return bot.send_message(message.chat.id, 'Это не картинка')

    file_info = bot.get_file(message.photo[-1].file_id)
    print('file_id: ', file_info)
    file_name = file_info.file_path.split('/')[-1]
    print('file_name: ', file_name)

    downloaded_file = bot.download_file(file_info.file_path)
    with open(file_name, 'wb') as new_file:
        new_file.write(downloaded_file)

    result = get_class(image_path=file_name)
    bot.send_message(message.chat.id, f'{result}')


bot.infinity_polling()