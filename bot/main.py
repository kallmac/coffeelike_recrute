import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, \
    ReplyKeyboardRemove

from config import UsersTable
import os

from icecream import ic

# dev
# dev

API_TOKEN = '7945741419:AAH1F1zVR4xlLfX6_HHt2V_HoWQO-qVv_zc' # ЗАМЕНИТЕ НА СВОЙ
bot = telebot.TeleBot(API_TOKEN)

questions = [
    ("Как вас зовут?", 0),  # Открытый вопрос
    ("Какой ваш любимый цвет?", ["Красный", "Синий", "Зеленый"]),  # Закрытый вопрос
    ("Какой ваш любимый фильм?", 0),  # Открытый вопрос
    ("Какой ваш любимый вид спорта?", ["Футбол", "Баскетбол", "Теннис"]),  # Закрытый вопрос
]

user_answers = {}
user_question_index = {}

db = UsersTable()



@bot.message_handler(commands= ['start'])
def start(message):
    print(message.from_user.id, message.from_user.username)
    db.add_user({"id": str(message.from_user.id), "username": message.from_user.username, "status": "user", "notif": 1})
@bot.message_handler(commands = ['get_table'], func= lambda message: db.is_admin(message.from_user.id))
def get_table(message):
    ic(message.from_user.id)
    kb = InlineKeyboardMarkup(row_width=3)
    week = InlineKeyboardButton(text='Месяц', callback_data='week')
    mounth = InlineKeyboardButton(text='Неделя', callback_data='mounth')
    year = InlineKeyboardButton(text='Год', callback_data='year')
    kb.add(week, mounth, year)
    bot.send_message(message.chat.id, "Таблицу за какой срок ты хочешь?", reply_markup=kb) #спрашиваем период

@bot.callback_query_handler(func = lambda callback: callback.message.text == "Таблицу за какой срок ты хочешь?") #если нажали на кнопку
def table(callback):
    week_table = os.read('D:/Project/pyCharm/coffeelike_recrute/bot/db', 'rb')
    bot.send_document(callback.message.chat.id, week_table)

@bot.message_handler(commands=['notification'], func= lambda message: db.is_admin(message.from_user.id)) #уведомления
def pushes(message):
    usr_id = message.from_user.id
    is_push = db.is_notif(usr_id)
    kb = InlineKeyboardMarkup(row_width=1)
    esc = InlineKeyboardButton(text='Отмена', callback_data='esc')
    change = InlineKeyboardButton(text='Да', callback_data='change')
    kb.add(change, esc)
    if is_push:
        bot.send_message(message.chat.id, "Сейчас уведомления включены. Желаете выключить?", reply_markup=kb)
    else:
        bot.send_message(message.chat.id, "Сейчас уведомления выключены. Желаете выключить?", reply_markup=kb)

@bot.callback_query_handler(func = lambda callback : callback.data == 'esc')#если нажали на кнопку
def change_push(callback):
    bot.delete_message(callback.message.chat.id, callback.message.id)

@bot.callback_query_handler(func = lambda callback : callback.data == 'change')#если нажали на кнопку
def change_push(callback):
    usr_id = callback.from_user.id
    is_push = db.is_notif(usr_id)

    bot.delete_message(callback.message.chat.id, callback.message.id)
    if is_push==False :
        is_push = True
        bot.send_message(callback.message.chat.id, 'Уведомления включены!')
    else:
        is_push = False
        bot.send_message(callback.message.chat.id, 'Уведомления выключены!')


@bot.message_handler(commands = ['ban'], func = lambda message: db.is_admin(message.from_user.id) or db.is_dev(message.from_user.id)) #ну бан
def ban(message):
    sent = bot.send_message(message.chat.id, "Кого банить?")
    bot.register_next_step_handler(sent, baned) #ждём ответа
def baned(message):
    usr_id = db.get_id(message.text)
    is_push = db.is_notif(usr_id)

    role = db.get_role(usr_id)
    if role == None:
        bot.send_message(message.chat.id, "Пользователь не найден в базе данных")
        return
    if(role == 'user'):
        kb = InlineKeyboardMarkup(row_width=1)
        esc = InlineKeyboardButton(text='Отмена', callback_data='esc')
        ban = InlineKeyboardButton(text='Да', callback_data=f'ban_{message.text}')
        kb.add(ban,esc)
        bot.send_message(message.chat.id, "Забанить?", reply_markup=kb)
    elif(role == 'ban'):
        kb = InlineKeyboardMarkup(row_width=1)
        esc = InlineKeyboardButton(text='Отмена', callback_data='esc')
        unban = InlineKeyboardButton(text='Да', callback_data=f'unban_{message.text}')
        kb.add(unban, esc)
        bot.send_message(message.chat.id, "Пользователь забанен. Желаете разбанить?", reply_markup=kb)
    elif(role == 'admin' or role == 'dev'):
        bot.send_message(message.chat.id, "Пользователь является админом, вы не можете его заблокировать")
    else:
        bot.send_message(message.chat.id, "Пользователь не найден в базе данных")


@bot.callback_query_handler(func = lambda callback : callback.data.split('_')[0] == 'ban')
def ban(callback):
    usr_id = callback.from_user.id
    is_push = db.is_notif(usr_id)
    db.edit_rol(usr_id=usr_id, role='ban')
    bot.send_message(callback.message.chat.id, "Пользователь заблокирован!")


@bot.callback_query_handler(func = lambda callback : callback.data.split('_')[0] == 'unban')
def unban(callback):
    usr_id = callback.from_user.id
    is_push = db.is_notif(usr_id)
    db.edit_rol(usr_id=usr_id, role='user')
    bot.send_message(callback.message.chat.id, "Пользователь разблокирован!")
# о да сейчас я буду писать deva

@bot.message_handler(commands = ['add_admin'], func = lambda message : db.is_dev(message.from_user.id))
def add_admin(message):
    sent = bot.send_message(message.chat.id, "Кого сделать админом?")
    bot.register_next_step_handler(sent, baned)  # ждём ответа

def get_admin(message):
    username = message.text
    usr_id = db.get_id(message.text)
    db.add_user({"id":usr_id, "username":message.text, "status":"admin", "notif":1})
    db.edit_rol(usr_id, "admin")
    bot.send_message(message.chat.id, f"Пользователь {username} стал администратором")

@bot.message_handler(commands = ['add_dev'], func = lambda message : db.is_dev(message.from_user.id))
def add_dev(message):
    sent = bot.send_message(message.chat.id, "Кого сделать супер-админом?")
    bot.register_next_step_handler(sent, baned)  # ждём ответа

def get_dev(message):
    username = message.text
    usr_id = db.get_id(message.text)
    db.add_user({"id":usr_id, "username":message.text, "status":"dev", "notif":1})
    db.edit_rol(usr_id, "dev")
    bot.send_message(message.chat.id, f"Пользователь {username} стал супер-администратором")

def notif_to_admin(user):

bot.polling(none_stop=True)