import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, \
    ReplyKeyboardRemove

from config import UsersTable
import os


import pandas as pd

# dev
from icecream import ic
# dev

API_TOKEN = '7945741419:AAH1F1zVR4xlLfX6_HHt2V_HoWQO-qVv_zc' # ЗАМЕНИТЕ НА СВОЙ
bot = telebot.TeleBot(API_TOKEN)



# user

def add_row_to_excel(file_path, new_row):
    if not os.path.exists(file_path):

        df = pd.DataFrame(columns=new_row.keys())
        df.to_excel(file_path, index=False, engine='openpyxl')


    df = pd.read_excel(file_path, engine='openpyxl')

    # Создаем DataFrame из новой строки (словаря)
    new_data = pd.DataFrame([new_row])

    # Добавляем новую строку к существующему DataFrame
    df = pd.concat([df, new_data], ignore_index=True)

    # Сохраняем обновленный DataFrame обратно в Excel файл
    df.to_excel(file_path, index=False, engine='openpyxl')



questions = [
    ("Как вас зовут?", 0),  # Открытый вопрос
    ("Какой ваш любимый цвет?", ["Красный", "Синий", "Зеленый"]),  # Закрытый вопрос
    ("Какой ваш любимый фильм?", 0),  # Открытый вопрос
    ("Какой ваш любимый вид спорта?", ["Футбол", "Баскетбол", "Теннис"]),  # Закрытый вопрос
]

excel_file = 'db/applicants.xlsx'

user_answers = {}
user_question_index = {}
user_message_ids = {}

# user

# all users



# all users

db = UsersTable()

@bot.message_handler(commands= ['start'])
def start(message):
    print(message.from_user.id, message.from_user.username)
    db.add_user({"id": str(message.from_user.id), "username": message.from_user.username, "status": "user", "notif": 1})


# admin

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
    if is_push == False:
        is_push = True
        bot.send_message(callback.message.chat.id, 'Уведомления включены!')
    else:
        is_push = False
        bot.send_message(callback.message.chat.id, 'Уведомления выключены!')
    db.is_notif(usr_id, is_push)

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
    elif role == 'ban':
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

# admin

# user

def create_inline_keyboard(current_index, total_questions):
    keyboard = InlineKeyboardMarkup()
    if current_index > 0:
        keyboard.add(InlineKeyboardButton("Назад", callback_data='back'))
    if current_index < total_questions - 1:
        keyboard.add(InlineKeyboardButton("Вперед", callback_data='forward'))
    return keyboard

def create_reply_keyboard(options):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    for option in options:
        keyboard.add(KeyboardButton(option))
    return keyboard

@bot.message_handler(commands=['poll'], func = lambda message: not db.is_admin(message.from_user.id))
def start_quiz(message):
    user_id = message.from_user.id
    user_answers[user_id] = {}
    user_answers[user_id]["username"] = message.from_user.username
    user_question_index[user_id] = 0  # Начинаем с первого вопроса
    ask_question(user_id)

def ask_question(user_id):
    question_index = user_question_index[user_id]
    if question_index < len(questions):
        question, answer_options = questions[question_index]

        # Отправляем вопрос
        if answer_options == 0:  # Открытый вопрос
            if questions[question_index][0] in  user_answers[user_id].keys():
                bot.send_message(user_id, question + f"\n*Ваш предыдущий ответ: *{user_answers[user_id][questions[question_index][0]]}", parse_mode='Markdown')
            else:
                bot.send_message(user_id, question)

        else:  # Закрытый вопрос

            ic(questions[question_index][0])
            ic(user_answers[user_id].keys())

            reply_keyboard = create_reply_keyboard(answer_options)
            if questions[question_index][0] in  user_answers[user_id].keys():
                bot.send_message(user_id, question + f"\n*Ваш предыдущий ответ: *{user_answers[user_id][questions[question_index][0]]}", reply_markup=reply_keyboard, parse_mode='Markdown')
            else:
                bot.send_message(user_id, question, reply_markup=reply_keyboard)

        # Добавляем инлайн-кнопки в отдельном сообщении
        inline_keyboard = create_inline_keyboard(question_index, len(questions))
        msg = bot.send_message(user_id, "Навигация:", reply_markup=inline_keyboard)
        user_message_ids[user_id] = msg.message_id
    else:
        bot.send_message(user_id, "Спасибо за участие! Ваши ответы: " + str(user_answers[user_id]))
        add_row_to_excel(file_path=excel_file, new_row=user_answers[user_id])
        del user_answers[user_id]
        del user_question_index[user_id]
        del user_message_ids[user_id]

@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    user_id = call.from_user.id
    question_index = user_question_index[user_id]

    if call.data == 'back':
        if question_index > 0:
            user_question_index[user_id] -= 1
            ask_question(user_id)
    elif call.data == 'forward':
        if question_index < len(questions) - 1:
            user_question_index[user_id] += 1
            ask_question(user_id)


@bot.message_handler(func=lambda message: message.from_user.id in user_question_index and not db.is_admin(message.from_user.id))
def handle_response(message):
    user_id = message.from_user.id
    """
    if user_id not in user_question_index:
        return  # Если пользователь не начал опрос, игнорируем
    """
    question_index = user_question_index[user_id]
    question, answer_options = questions[question_index]

    if answer_options == 0:  # Открытый вопрос
        # Сохраняем ответ
        user_answers[user_id][questions[user_question_index[user_id]][0]] = message.text
        user_question_index[user_id] += 1
        if user_id in user_message_ids:
            try:
                bot.delete_message(chat_id=user_id, message_id=user_message_ids[user_id])
            except Exception as e:
                print(f"Ошибка при удалении сообщения: {e}")
        ask_question(user_id)
    elif message.text in answer_options:  # Закрытый вопрос
        # Сохраняем ответ
        user_answers[user_id][questions[user_question_index[user_id]][0]] = message.text

        user_question_index[user_id] += 1

        # Удаляем клавиатуру после получения ответа
        bot.send_message(user_id, "Спасибо за ваш ответ!", reply_markup=ReplyKeyboardRemove())
        if user_id in user_message_ids:
            try:
                bot.delete_message(chat_id=user_id, message_id=user_message_ids[user_id])
            except Exception as e:
                print(f"Ошибка при удалении сообщения: {e}")
        ask_question(user_id)

# user

bot.polling(none_stop=True)