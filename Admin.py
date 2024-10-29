import telebot
from telebot import types
import sqlite3

API_TOKEN = '7712920785:AAGLtViAA6H34GcDBBy896TCZX_mwwjM80M' # ЗАМЕНИТЕ НА СВОЙ
bot = telebot.TeleBot(API_TOKEN)

db = sqlite3.connect('users.db')#подключаем бд
c = db.cursor()
#c.execute("CREATE TABLE devs(id text, username text)")
#c.execute("CREATE TABLE admins(id text, username text)")
#c.execute("CREATE TABLE users(id text, username text)")
#c.execute("CREATE TABLE bans(id text, username text)")
# в db уже созданы таблицы devs, admins, users, bans с колонками id и username
def adm(message):
    # проверка на admin или dev
    isadm = False
    if(message.from_user.username == 'drus1k0'):
        isadm = True
    user_id = str(message.from_user.id)
    c.execute("SELECT id FROM admins WHERE id = user_id")
    if(len(c.fetchall())):
        isadm = True #admin
    c.execute("SELECT id FROM devs WHERE id = user_id")
    if (len(c.fetchall())):
        isadm = True #dev
    return isadm
#уведомления
global is_push
is_push = True
#получение таблицы
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
    kb = types.InlineKeyboardMarkup(row_width=2)
    on = types.InlineKeyboardButton(text='Вкл', callback_data='on')
    off = types.InlineKeyboardButton(text='Выкл', callback_data='off')
    kb.add(on,off)
    bot.send_message(message.chat.id, "Уведомления", reply_markup=kb)
@bot.callback_query_handler(func = lambda x : x.message.text == "Уведомления")#если нажали на кнопку
def change_push(callback):
    if(callback.data == 'on'):
        is_push = 1
        bot.send_message(callback.message.chat.id, "Уведомления включены!")
    else:
        is_push = 0
        bot.send_message(callback.message.chat.id, "Уведомления выключены!")
@bot.message_handler(commands = ['ban'], func = adm) #ну бан
def ban(message):
    sent = bot.send_message(message.chat.id, "Кого банить?")
    bot.register_next_step_handler(sent, baned) #ждём ответа
def baned(message):
    c.execute("SELECT username FROM users WHERE username = message.text")
    if(c.fetchall().size()):
        c.execute("SELECT id FROM users WHERE username = message.text")
        user_id = c.fetchone()[0]
        c.execute("DELETE FROM users WHERE username = message.textt")
        c.execute("INSERT INTO bans VALUES(user_id, message.text)")
        bot.send_message(message.chat.id, "Негодяй забанен")
    else:
        bot.send_message(message.chat.id, "Пользователь не найден в бд")

#def add_admin(message):
bot.polling()
db.commit()
db.close()


'''
/get_table --- спросить у пользователя кнопками, за какой срок нужно отсосать и отправляем xls файл
/notification --- включить/отключить уведомления об новых отправленных анкетах
/add_admin ---
/add_dev ---
/ban 
'''

'''import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

API_TOKEN = '7945741419:AAH1F1zVR4xlLfX6_HHt2V_HoWQO-qVv_zc' # ЗАМЕНИТЕ НА СВОЙ
bot = telebot.TeleBot(API_TOKEN)

questions = [
    ("Как вас зовут?", 0),
    ("Какой ваш любимый цвет?", ["Красный", "Синий", "Зеленый"]),
    ("Какой ваш любимый фильм?", 0),
    ("Какой ваш любимый вид спорта?", ["Футбол", "Баскетбол", "Теннис"])
]
ispoll = False
current_question_index = 0
user_responses = {}

@bot.message_handler(commands=['poll'])
def poll_command(message):
    global ispoll
    global current_question_index
    ispoll = True
    current_question_index = 0
    user_responses[message.from_user.id] = []
    ask_question(message.chat.id)

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
        global ispoll
        ispoll = False
        bot.send_message(chat_id, "Опрос завершен. Спасибо за участие!")
        current_question_index = 0

@bot.message_handler(func=lambda message: True)
def handle_text_response(message):
    if ispoll:
        global current_question_index
        if message.from_user.id in user_responses and current_question_index < len(questions) and questions[current_question_index][1] == 0:
            response = message.text
            user_responses[message.from_user.id].append((questions[current_question_index][0], response))
            bot.send_message(message.chat.id, f"Спасибо за ваш ответ: {response}")
            current_question_index += 1
            ask_question(message.chat.id)

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    global current_question_index
    if call.data.startswith("answer_"):
        _, question_index, answer = call.data.split("_")
        question_index = int(question_index)
        if call.from_user.id not in user_responses:
            user_responses[call.from_user.id] = []
        user_responses[call.from_user.id].append((questions[question_index][0], answer))
        bot.answer_callback_query(call.id, f"Вы выбрали: {answer}")
        bot.send_message(call.message.chat.id, f"Спасибо за ваш ответ: {answer}", reply_markup=None)
        current_question_index += 1
        ask_question(call.message.chat.id)
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
        bot.edit_message_text(chat_id=call.message.chat.id, parse_mode='Markdown', message_id=call.message.message_id, text=questions[question_index][0] + "\n*✅Ваш ответ:* " + answer)
bot.polling()
'''
'''import telebot
from telebot import types

#eshkere01
bot  = telebot.TeleBot("7712920785:AAGLtViAA6H34GcDBBy896TCZX_mwwjM80M")
@bot.message_handler(commands = ['start'])
def start(message):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    b1 = types.KeyboardButton(text='М')
    b2 = types.KeyboardButton(text='Ж')
    kb.add(b1,b2)
    sent = bot.send_message(message.chat.id, 'МЖ?', reply_markup=kb)
    bot.register_next_step_handler(sent, review)
def review(message):
    sent = bot.send_message(message.chat.id, 'А теперь напиши свой возраст в полных годиках...')
    bot.register_next_step_handler(sent, old)
def old(message):
    if(int(message.text)>=30):
        bot.send_message(message.chat.id, 'слишком стар')
    else:
        bot.send_message(message.chat.id, 'зелен')
bot.polling()'''
'''@bot.message_handler(commands = ['start'])
def start(message):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    b1 = types.KeyboardButton(text = 'Кнопка1')
    b2 = types.KeyboardButton(text = 'Кнопка2')
    kb.add(b1,b2)
    bot.send_message(message.chat.id, "Ну что ты братишка 52?", reply_markup=kb)
@bot.message_handler(commands = ['happyend'])
def end(message):
    kb = types.InlineKeyboardMarkup()
    b1 = types.InlineKeyboardButton(text = 'goida', callback_data='b1')
    b2 = types.InlineKeyboardButton(text = 'гойда', callback_data='b2')
    kb.add(b1,b2)
    bot.send_message(message.chat.id, "ты должен сделать правильный выбор", reply_markup = kb)
@bot.callback_query_handler(func = lambda callback: callback.data)
def check_button(callback):
    if(callback.data == 'b1'):
        bot.send_message(callback.message.chat.id, "zov")
    else:
        bot.send_message(callback.message.chat.id, "матушкааааа земля")'''

'''@bot.message_handler(commands = ['start'])
def start(message):
    bot.send_message(message.chat.id, "<i>Ну что ты братишка</i> <b>52</b>? вот мои теги:\n/start\n/happyend\nid", parse_mode='HTML')
@bot.message_handler(commands = ['happyend'])
def end(message):
    bot.send_message(message.chat.id, "хаха я вычислю тебя по ip: " + str(message.from_user.first_name) + " " + str(message.from_user.last_name))
@bot.message_handler(func = lambda message: message.text=='id')
def id(message):
    bot.reply_to(message, "да да я и твой id знаю: " + str(message.from_user.username))
@bot.message_handler(func = lambda message: message.text == "белгород")
def bel(message):
    file = open('bomba.jpg', 'rb')
    bot.send_photo(message.chat.id, file, 'ГОЙДА')
'''


#@bot.message_handler(chat_types = ['private'])
#@bot.message_handler(content_types = ['photo'])
#message.chat.type
'''
commands
chat_types
content_types
regexp
func
Можно это писать через запятую и будет типа &&
А можно писать в 2 строчки и будет ||
'''

