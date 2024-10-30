import telebot
from telebot import types

API_TOKEN = '7945741419:AAH1F1zVR4xlLfX6_HHt2V_HoWQO-qVv_zc'  # Замените на ваш токен
bot = telebot.TeleBot(API_TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, text="HIIII")


if __name__ == '__main__':
    bot.polling(none_stop=True)
