import telebot
from telebot import types


API_TOKEN = '7945741419:AAH1F1zVR4xlLfX6_HHt2V_HoWQO-qVv_zc'  # Замените на ваш токен
bot = telebot.TeleBot(API_TOKEN)

questions = [
    ("Как вас зовут?", 0),
    ("Какой ваш любимый цвет?", ["Красный", "Синий", "Зеленый"]),
    ("Какой ваш любимый фильм?", 0),
    ("Какой ваш любимый вид спорта?", ["Футбол", "Баскетбол", "Теннис"])
]


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, text="Hello")

@bot.message_handler(commands=['xx'])
def replyKeyBoard(message):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    btn1 = types.KeyboardButton(text='Кнопка1')
    btn2 = types.KeyboardButton(text='Кнопка2')
    kb.add(btn1, btn2)
    bot.send_message(chat_id=message.chat.id, reply_markup=kb, text='gg')

@bot.message_handler(func=lambda message: True)
def handle_keyboard_markup(message):



if __name__ == '__main__':
    bot.polling(none_stop=True)
