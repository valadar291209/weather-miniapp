from telebot import *
from requests import *
from json import *

API = "1790e4a71cc04e9a943b506ccdeeef78"
bot = telebot.TeleBot('8699366442:AAEVnZNdnFJviVCvbqu_CaH7cRVSBRL1uNI')

delete_words = list()
@bot.message_handler(commands=['start'])
def start_message(message):
    web_app = types.WebAppInfo("https://valadar291209.github.io/weather-miniapp/")
    web_app_button = types.InlineKeyboardButton(text="🌦 Открыть погоду", web_app=web_app)
    keyboard = types.InlineKeyboardMarkup().add(web_app_button)
    bot.send_message(message.chat.id, "Привет! Жми на кнопку, чтобы узнать погоду:", reply_markup=keyboard)

@bot.message_handler(content_types=['web_app_data'])
def handle_web_app_data(message):
    received_data = message.web_app_data.data
    bot.send_message(message.chat.id, f"Бот получил от веб-аппа: {received_data}")

@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data == "get_photo":
        markup = types.InlineKeyboardMarkup(row_width=1)
        file = open("./images.jpg", "rb")
        bot.send_photo(callback.message.chat.id, file, reply_markup=markup)

@bot.message_handler(commands=["enter_banword"])
def main(message):
    word = message.text.split().lower()[-1]
    if word != "/enter_banword":
        delete_words.append(word)
        bot.send_message(message.chat.id, f"Слово '{word}' добавлено в чёрный список")
    else:
        bot.send_message(message.chat.id, "Напиши слово после команды: /enter_banword слово")

@bot.message_handler()
def main(message):
    for word in delete_words:
        if word.lower() in message.text:
            bot.delete_message(message.chat.id, message.chat.id)
            bot.send_message(message.chat.id, f"Нельзя такое говорить, {message.from_user.first_name} {message.from_user.last_name}")
            return
    else:
        if "Салам" in message.text:
            bot.send_message(message.chat.id, f"О, брат, ты тоже татарин?")
        elif "салам" in message.text.lower():
            bot.send_message(message.chat.id, f"Ле ты что здароваешься так как негодяй какой - то, ты давай не это?")
        else:
            markup = types.InlineKeyboardMarkup(row_width=1)
            btn1 = types.InlineKeyboardButton("Перейти на Github", url="https://github.com/valadar291209")
            btn2 = types.InlineKeyboardButton("Кинь смешную картинку", callback_data="get_photo")
            markup.add(btn1, btn2)
            bot.reply_to(message, "Я не понимаю о чём вы, может вас заинтересует это?", reply_markup=markup)

bot.polling(non_stop=True)
