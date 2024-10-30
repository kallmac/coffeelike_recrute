#пока это не правильный админ
import telebot
from telebot import types
import sqlite3

API_TOKEN = '7712920785:AAGLtViAA6H34GcDBBy896TCZX_mwwjM80M' # ЗАМЕНИТЕ НА СВОЙ
bot = telebot.TeleBot(API_TOKEN)

db = sqlite3.connect('everyone.sql')#подключаем бд
c = db.cursor()
#c.execute("CREATE TABLE devs(id int, username text)")
#c.execute("CREATE TABLE admins(id int, username text)")
#c.execute("CREATE TABLE users(id int, username text)")
#c.execute("CREATE TABLE bans(id int, username text)")
#в db уже созданы таблицы devs, admins, users, bans с колонками id и username
#c.execute("INSERT INTO devs VALUES(228432526, 'slilturforever')")
def role(user):

    c.execute('SELECT EXISTS(SELECT status FROM users WHERE tg_username = ?)', (user,))
    if(c.fetchone()[0]):
        return c.fetchone()[0]
    return 'none'
    '''c.execute('SELECT EXISTS(SELECT id FROM users WHERE username = ?)', (user,))
    if(c.fetchone()[0]):
        return 'user'
    c.execute('SELECT EXISTS(SELECT id FROM admins WHERE username = ?)', (user,))
    if(c.fetchone()[0]):
        return 'admin'
    c.execute('SELECT EXISTS(SELECT id FROM devs WHERE username = ?)', (user,))
    if(c.fetchone()[0]):
        return 'dev'
    return 'none'  '''
def adm(message):
    rol = role(message.from_user.username)
    if(rol=='admin' or rol=='dev'):
        return True
    return False
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
    '''c.execute("SELECT username FROM users WHERE username = ?", (message.text,))
    if(c.fetchone()[0]):
        c.execute("SELECT id FROM users WHERE username = ?", (message.text,))
        user_id = c.fetchone()[0]
        c.execute("DELETE FROM users WHERE username = message.text")
        c.execute("INSERT INTO bans VALUES(user_id, message.text)")
        bot.send_message(message.chat.id, "Негодяй забанен")
    else:
        bot.send_message(message.chat.id, "Пользователь не найден в бд")'''
@bot.callback_query_handler(func = lambda callback : callback.data[0:4] == 'ban_')
def ban(callback):
    user = callback.data.split("_")[1]
    c.execute("UPDATE users SET status = 'ban' WHERE tg_username = ?", (user,))
    bot.send_message(callback.message.chat.id, "Пользователь заблокирован!")
    '''c.execute("SELECT * from users WHERE tg_username = ?", (user,))
        tup = c.fetchone()
        tup[3] = 'ban'
        tup[4] = 0
        c.execute(f"INSERT INTO users (id, tg_id, tg_username, status, notif) VALUES (?, ?, ?, ?, ?)", tup)
        c.execute("DELETE FROM users WHERE tg_username = ?", (user,))'''
@bot.callback_query_handler(func = lambda callback : callback.data[0:6] == 'unban_')
def unban(callback):
    user = callback.data.split("_")[1]
    c.execute("UPDATE users SET status = 'user' WHERE tg_username = ?", (user,))
    bot.send_message(callback.message.chat.id, "Пользователь разблокирован!")
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


