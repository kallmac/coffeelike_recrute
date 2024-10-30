import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, \
    ReplyKeyboardRemove
import pandas as pd
import openpyxl

# dev
from icecream import ic
# dev

# Создаем экземпляр бота
bot = telebot.TeleBot('7945741419:AAH1F1zVR4xlLfX6_HHt2V_HoWQO-qVv_zc')

# Список вопросов
questions = [
    ("Как вас зовут?", 0),  # Открытый вопрос
    ("Какой ваш любимый цвет?", ["Красный", "Синий", "Зеленый"]),  # Закрытый вопрос
    ("Какой ваш любимый фильм?", 0),  # Открытый вопрос
    ("Какой ваш любимый вид спорта?", ["Футбол", "Баскетбол", "Теннис"]),  # Закрытый вопрос
]

# Словарь для хранения ответов пользователей
user_answers = {}

# Словарь для хранения текущего вопроса пользователя
user_question_index = {}


# Функция для создания инлайн-клавиатуры
def create_inline_keyboard(current_index, total_questions):
    keyboard = InlineKeyboardMarkup()
    if current_index > 0:
        keyboard.add(InlineKeyboardButton("Назад", callback_data='back'))
    if current_index < total_questions - 1:
        keyboard.add(InlineKeyboardButton("Вперед", callback_data='forward'))
    return keyboard


# Функция для создания клавиатуры с вариантами ответов
def create_reply_keyboard(options):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    for option in options:
        keyboard.add(KeyboardButton(option))
    return keyboard


@bot.message_handler(commands=['start'])
def start_quiz(message):
    user_id = message.from_user.id
    user_answers[user_id] = {}
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
        bot.send_message(user_id, "Навигация:", reply_markup=inline_keyboard)
    else:
        bot.send_message(user_id, "Спасибо за участие! Ваши ответы: " + str(user_answers[user_id]))
        user_answ = list(user_answers[user_id].values())
        df = pd.DataFrame(user_answ)
        # Сохранение в Excel файл
        df.to_excel('D:/Project/pyCharm/coffeelike_recrute/bot/db/applicants.xlsx', index=False)
        del user_answers[user_id]
        del user_question_index[user_id]


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


@bot.message_handler(func=lambda message: message.from_user.id in user_question_index)
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
        bot.delete_message(chat_id=user_id, message_id=message.message_id - 1)
        ask_question(user_id)
    elif message.text in answer_options:  # Закрытый вопрос
        # Сохраняем ответ
        user_answers[user_id][questions[user_question_index[user_id]][0]] = message.text

        user_question_index[user_id] += 1

        # Удаляем клавиатуру после получения ответа
        bot.send_message(user_id, "Спасибо за ваш ответ!", reply_markup=ReplyKeyboardRemove())
        bot.delete_message(chat_id=user_id, message_id=message.message_id - 1)
        ask_question(user_id)


# Запуск бота
bot.polling()
