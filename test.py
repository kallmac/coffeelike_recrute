import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

API_TOKEN = '7945741419:AAH1F1zVR4xlLfX6_HHt2V_HoWQO-qVv_zc' # ЗАМЕНИТЕ НА СВОЙ
bot = telebot.TeleBot(API_TOKEN)

questions = [
    ("Как вас зовут?", 0),
    ("Какой ваш любимый цвет?", ["Красный", "Синий", "Зеленый"]),
    ("Какой ваш любимый фильм?", 0),
    ("Какой ваш любимый вид спорта?", ["Футбол", "Баскетбол", "Теннис"])
]

is_poll = False
current_question_index = 0
user_responses = {}

keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
button_left = KeyboardButton('<=')
button_right = KeyboardButton('=>')
keyboard.add(button_left, button_right)


@bot.message_handler(commands=['poll'])
def poll_command(message):
    global is_poll
    global current_question_index
    is_poll = True
    current_question_index = 0
    user_responses[message.from_user.id] = []
    bot.send_message(message.chat.id, reply_markup=keyboard, text='Вопросами можно управлять')
    ask_question(message.chat.id)

@bot.message_handler(func=lambda message: True)
def handle_admin_message(message):
    global current_question_index
    if message.text == '<=':
        if current_question_index > 0:
            current_question_index-=1
    elif message.text == '=>':
        if current_question_index < len(questions)-1:
            current_question_index+=1

def ask_question(chat_id):
    global current_question_index
    if current_question_index < len(questions):
        question, answers = questions[current_question_index]
        if answers == 0:
            bot.send_message(chat_id, question)
        else:
            markup = InlineKeyboardMarkup()
            for answer in answers:
                button = InlineKeyboardButton(answer, callback_data=f"answer_{current_question_index}_{answer}")
                markup.add(button)
            bot.send_message(chat_id, question, reply_markup=markup)
    else:
        global is_poll
        is_poll = False
        bot.send_message(chat_id, "Опрос завершен. Спасибо за участие!")
        current_question_index = 0


@bot.message_handler(func=lambda message: is_poll)
def handle_text_response(message):
    global current_question_index
    if message.from_user.id in user_responses and current_question_index < len(questions) and questions[current_question_index][1] == 0:
        response = message.text
        user_responses[message.from_user.id].append((questions[current_question_index][0], response))
        bot.send_message(message.chat.id, f"Спасибо за ваш ответ: {response}")
        current_question_index += 1
        ask_question(message.chat.id)

@bot.callback_query_handler(func=lambda call: is_poll)
def handle_query(call):
    global current_question_index
    if call.data.startswith("answer_"):
        _, question_index, answer = call.data.split("_")
        question_index = int(question_index)
        if call.from_user.id not in user_responses:
            user_responses[call.from_user.id] = []
        user_responses[call.from_user.id].append((questions[question_index][0], answer))
        # bot.answer_callback_query(call.id, f"Вы выбрали: {answer}")
        bot.send_message(call.message.chat.id, f"Спасибо за ваш ответ: {answer}", reply_markup=None)
        current_question_index += 1
        ask_question(call.message.chat.id)
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
        bot.edit_message_text(chat_id=call.message.chat.id, parse_mode='Markdown', message_id=call.message.message_id, text=questions[question_index][0] + "\n*✅Ваш ответ:* " + answer)

bot.polling()
