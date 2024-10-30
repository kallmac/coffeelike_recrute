#пока это не правильный админ
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, \
    ReplyKeyboardRemove
from telebot import types
import sqlite3

from config import UsersTable


# dev
from icecream import ic
# dev
API_TOKEN = '7712920785:AAGLtViAA6H34GcDBBy896TCZX_mwwjM80M' # ЗАМЕНИТЕ НА СВОЙ
bot = telebot.TeleBot(API_TOKEN)

db = sqlite3.connect('everyone.sql', check_same_thread=False)#подключаем бд
c = db.cursor()

questions = [
    ("Как вас зовут?", 0),  # Открытый вопрос
    ("Какой ваш любимый цвет?", ["Красный", "Синий", "Зеленый"]),  # Закрытый вопрос
    ("Какой ваш любимый фильм?", 0),  # Открытый вопрос
    ("Какой ваш любимый вид спорта?", ["Футбол", "Баскетбол", "Теннис"]),  # Закрытый вопрос
]

user_answers = {}
user_question_index = {}



def role(user):
    c.execute('SELECT EXISTS(SELECT status FROM users WHERE tg_username = ?)', (user,))
    if(c.fetchone()[0]):
        return c.fetchone()[0]
    return 'none'

def adm(message):
    rol = role(message.from_user.username)
    if(rol=='admin' or rol=='dev'):
        return True
    return False
#уведомления


@bot.message_handler(commands = ['get_table'], func=adm)
def get_table(message):
    kb = types.InlineKeyboardMarkup(row_width=3)
    week = types.InlineKeyboardButton(text='Месяц', callback_data='week')
    mounth = types.InlineKeyboardButton(text='Неделя', callback_data='mounth')
    year = types.InlineKeyboardButton(text='Год', callback_data='year')
    kb.add(week, mounth, year)
    bot.send_message(message.chat.id, "Таблицу за какой срок ты хочешь?", reply_markup=kb) #спрашиваем период

@bot.callback_query_handler(func = lambda callback: callback.message.text == "Таблицу за какой срок ты хочешь?") #если нажали на кнопку
def table(callback):

    #тут надо таблички из excelя загрузить
    if(callback.data == 'week'):
        week_table = read('week_table.xslx', 'rb') #хз чё писать
        bot.send_document(callback.message.chat.id, week_table)
    elif(callback.data == 'mounth'):
        mounth_table = read('mounth_table.xslx', 'rb')#хз чё писать
        bot.send_document(callback.message.chat.id, mounth_table)
    else:
        year_table = read('year_table.xslx', 'rb') #хз чё писать
        bot.send_document(callback.message.chat.id, year_table)

@bot.message_handler(commands=['notification'],  func = adm) #уведомления
def pushes(message):
    kb = types.InlineKeyboardMarkup(row_width=1)
    esc = types.InlineKeyboardButton(text='Отмена', callback_data='esc')
    change = types.InlineKeyboardButton(text='Да', callback_data='change')
    kb.add(change, esc)
    if(is_push):
        bot.send_message(message.chat.id, "Сейчас уведомления включены. Желаете выключить?", reply_markup=kb)
    else:
        bot.send_message(message.chat.id, "Сейчас уведомления выключены. Желаете выключить?", reply_markup=kb)

@bot.callback_query_handler(func = lambda callback : callback.data == 'esc')#если нажали на кнопку
def change_push(callback):
    bot.delete_message(callback.message.chat.id, callback.message.id)

@bot.callback_query_handler(func = lambda callback : callback.data == 'change')#если нажали на кнопку
def change_push(callback):
    global is_push
    bot.delete_message(callback.message.chat.id, callback.message.id)
    if(is_push==False):
        is_push = True
        bot.send_message(callback.message.chat.id, 'Уведомления включены!')
    else:
        is_push = False
        bot.send_message(callback.message.chat.id, 'Уведомления выключены!')

@bot.message_handler(commands = ['ban'], func = adm) #ну бан
def ban(message):
    sent = bot.send_message(message.chat.id, "Кого банить?")
    bot.register_next_step_handler(sent, baned) #ждём ответа
def baned(message):
    rol = role(message.text)
    if(rol == 'user'):
        kb = types.InlineKeyboardMarkup(row_width=1)
        esc = types.InlineKeyboardButton(text='Отмена', callback_data='esc')
        ban = types.InlineKeyboardButton(text='Да', callback_data=f'ban_{message.text}')
        kb.add(ban,esc)
        bot.send_message(message.chat.id, "Забанить?", reply_markup=kb)
    elif(rol=='ban'):
        kb = types.InlineKeyboardMarkup(row_width=1)
        esc = types.InlineKeyboardButton(text='Отмена', callback_data='esc')
        unban = types.InlineKeyboardButton(text='Да', callback_data=f'unban_{message.text}')
        kb.add(unban, esc)
        bot.send_message(message.chat.id, "Пользователь забанен. Желаете разбанить?", reply_markup=kb)
    elif(rol=='admin' or rol=='dev'):
        bot.send_message(message.chat.id, "Пользователь является админом, вы не можете его заблокировать")
    else:
        bot.send_message(message.chat.id, "Пользователь не найден в базе данных")

@bot.callback_query_handler(func = lambda callback : callback.data[0:4] == 'ban_')
def ban(callback):
    user = callback.data.split("_")[1]
    c.execute("UPDATE users SET status = 'ban' WHERE tg_username = ?", (user,))
    bot.send_message(callback.message.chat.id, "Пользователь заблокирован!")

@bot.callback_query_handler(func = lambda callback : callback.data[0:6] == 'unban_')
def unban(callback):
    user = callback.data.split("_")[1]
    c.execute("UPDATE users SET status = 'user' WHERE tg_username = ?", (user,))
    bot.send_message(callback.message.chat.id, "Пользователь разблокирован!")
#def add_admin(message):
bot.polling()
db.commit()
db.close()

