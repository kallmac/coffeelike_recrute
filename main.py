import telebot
from telebot import types

API_TOKEN = '7945741419:AAH1F1zVR4xlLfX6_HHt2V_HoWQO-qVv_zc'  # Замените на ваш токен
bot = telebot.TeleBot(API_TOKEN)

# Словарь для хранения ответов пользователя
user_data = {}

# Список вопросов
questions = [
    ["Где вы живете?", ['Евразия', 'Aфрика', 'Австралия']],
    ["Как вас зовут?", 0],
    ["Сколько вам лет?", 0],
]

# Индекс текущего вопроса
current_question_index = {}


@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    user_data[user_id] = {}
    current_question_index[user_id] = 0

    if questions[current_question_index[user_id]][1] == 0:
        bot.send_message(user_id, questions[current_question_index[user_id]][0])
    else:
        question = questions[current_question_index[user_id]][0]
        answers = questions[current_question_index[user_id]][1]
        markup = types.InlineKeyboardMarkup(row_width=len(answers))
        for i in answers:
            j = types.InlineKeyboardButton(i, callback_data=i)
            markup.add(j)

        bot.send_message(message.chat.id, text=question, reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_answer(message):
    user_id = message.chat.id
    
    if user_id in current_question_index:
        print('fsgdsf')
        if questions[current_question_index[user_id]][1] == 0:
            user_data[user_id][questions[current_question_index[user_id]][0]] = message.text

        # Переходим к следующему вопросу
        current_question_index[user_id] += 1

        if current_question_index[user_id] < len(questions):
            bot.send_message(user_id, questions[current_question_index[user_id]][0])
        else:
            bot.send_message(user_id, "Спасибо за ваши ответы!")
            # Здесь можно обработать или сохранить данные
            print(user_data[user_id])  # Выводим данные в консоль
            # Удаляем данные пользователя, если не нужно хранить
            del user_data[user_id]
            del current_question_index[user_id]

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.message:
        user_data[call.message.chat.id][questions[current_question_index[call.message.chat.id]][0]] = call.data
        print(call.data)
        print(user_data)
    return 0

if __name__ == '__main__':
    bot.polling(none_stop=True)
