from gc import callbacks

import telebot
from pyexpat.errors import messages
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, \
    ReplyKeyboardRemove

from config import UsersTable
import os

import pandas as pd

from datetime import datetime, timedelta

# dev
from icecream import ic

#from gptgovno import user_message_ids

# dev

API_TOKEN = '7712920785:AAGLtViAA6H34GcDBBy896TCZX_mwwjM80M' # ЗАМЕНИТЕ НА СВОЙ
bot = telebot.TeleBot(API_TOKEN)



# user

db = UsersTable()

questions = [
    ("Какая вакансия тебя заинтересовала? ✨", ["Бариста", "Повар"]),  # Открытый вопрос
    ("ФИО: 📝", 0),  # Закрытый вопрос
    ("Гражданство: 🌍", 0),  # Открытый вопрос
    ("Город проживания: 🏙️", ["Нижний Новгород", "Киров", "Владимир", "Саратов", "Ижевск"]),
    ("Твой ник в телеграме (в формате @Name123): 📱", 0),
    ("Контактный номер телефона: 📞", 0),
    ("Количество полных лет: 🎂", 0),
    ("Форма обучения: 🎓", ["Очная", "Очно-заочная", "Заочная", "Не обучаюсь"]),
    ("Опыт работы (расскажи о предыдущем опыте работы, где, сколько и кем работал/а): 💼", 0),
    ("Причина ухода с последнего места работы: ❓",
    ["Не подошел ритм работы",
    "Сложно совмещать с учебой",
    "Не устраивала з/п",
    "Проблемы с руководством",
    "Не нравился коллектив",
    "Некомфортная атмосфера",
    "Отсутствие роста в компании",
    "Переезд",
    "Не работал/а ранее",
    "Другое"]),
    ("Желаемый график работы? ⏰", ["5/2", "2/2", "3/2", "2/3"]),
    ("Желаемый уровень заработной платы? 💰", 0),
    ("На какой период ищешь работу? 📅", 0),
    ("Район города, в котором тебе будет удобно работать (можешь указать несколько): 📍", 0),
    ("Это последний вопрос! Как вы узнали о нашей вакансии? 🔍",
     ["hh.ru",
    "Авито",
    "От друзей",
    "Реклама ВК",
    "Реклама в Telegram",
    "В своем учебном заведении",
    "В кофейне Coffee Like",
    "Другое"])
]

excel_file = 'db/applicants.xlsx'

user_answers = {}
user_question_index = {}
user_message_ids_to_del = {}
user_ids = {}
users_is_poll = set()


def notif_to_admin(user):
    notif_admins = db.get_notif()
    for cht_id in notif_admins:
        cht_id = cht_id[0]
        bot.send_message(cht_id, f"Пользователь {user} оставил вакансию бариста")


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

def filter_exel(date: datetime.date, input_file: str):
    output_file = input_file.split('.')[0] + "_" + str(date) + ".xlsx"


    # Чтение Excel файла
    df = pd.read_excel(input_file)

    # Убедитесь, что столбец с датами имеет правильный тип данных
    # Замените 'date_column' на имя вашего столбца с датами
    df['date'] = pd.to_datetime(df['date'], errors='coerce')

    # Фильтрация строк, где дата больше 2 июня 2024 года
    filtered_df = df[df['date'] >= date]

    # Сохранение отфильтрованных данных в новый Excel файл
    filtered_df.to_excel(output_file, index=False)

    return output_file


# user

# all users
@bot.message_handler(func = lambda message : db.is_ban(message.from_user.id))
def ban_message(message):
    bot.send_sticker(message.chat.id, "CAACAgIAAxkBAAENDdZnJJCjQasN787Pv9mEBT7gBZLfxwACR1YAAtTAGEntuLbdzn-UrTYE")
    bot.reply_to(message=message, text="Администрация ограничила вам доступ к данному боту.")
@bot.callback_query_handler(func = lambda callback : db.is_ban(callback.from_user.id))
def ban_callback(callback):
    bot.send_sticker(callback.message.chat.id, "CAACAgIAAxkBAAENDdZnJJCjQasN787Pv9mEBT7gBZLfxwACR1YAAtTAGEntuLbdzn-UrTYE")
    bot.reply_to(message=callback.message, text="Администрация ограничила вам доступ к данному боту.")
@bot.message_handler(commands= ['start'])
def start(message):
    print(message.from_user.id, message.from_user.username)
    db.add_user({"id": str(message.from_user.id), "username": message.from_user.username, "status": "user", "notif": 1, "chat_id" : message.chat.id})

    usr_id = message.from_user.id
    db.edit_rol(usr_id, 'user')
    if db.is_ban(usr_id):
        bot.reply_to(message=message, text="Администрация ограничила вам доступ к данному боту.")
    elif db.is_admin(usr_id):
        hi_text_admin = (
            "Приветствую👋\n"
            "Я бот компании Coffee Like!\n"
            "Вы являетесь Админом, поэтому я проведу Вам небольшой экскурс по командам, которые Вам доступны!\n\n"

            "<b><i>Команды:</i></b>\n\n"

            "<i>Анализ:</i>\n"
            "/start — 😊Начало общения со мной\n"
            "/help — 📋Описание всех команд, доступных Вам\n"
            "/get_table — 📑Вам присылается файл xlsx (EXL-таблица),\n"
            "собранная за определённый период времени:\n"
            "неделю, месяц, год или за несколько лет.\n"
            "/notification — 👀Включение/отключение уведомлений\n"
            "о новых отправленных анкетах\n"
            "/status — 📊Выводит ваш нынешний статус пользователя\n\n"

            "<i>Действия с пользователями:</i>\n"
            "/ban — Блокировка пользователя\n"
            "(блокировка администраторов Вам не доступна).\n"
            "/add_user — Добавления пользователя"
        )

        with open('img/startimg1.png', 'rb') as photo:
            bot.send_photo(photo=photo, chat_id=message.chat.id, parse_mode='html', caption=hi_text_admin)
    else:
        ic(usr_id)
        with open('img/startimg1.png', 'rb') as photo:
            bot.send_photo(photo=photo ,chat_id=message.chat.id, caption=
"""
Привет👋

Вас приветствует бот команды Coffee Like!
Здесь вы можете отправить свою анкету и попасть в нашу дружную команду. Если вы хотите работать у нас, но не достигли 18 лет узнайте про Академию Coffee Like.

Доступные вам команды:

/start — 😊Начало общения со мной
/info — 📃информация о вакансиях, которые Вас интересуют
/status — 📊Статус, в котором Вы пребываете
""")
        ic(usr_id)
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton("Академия", callback_data='academy'))
        keyboard.add(InlineKeyboardButton("Информация о работе", callback_data='info_work'))
        keyboard.add(InlineKeyboardButton("Подать анкету", callback_data='poll'))

        msg = bot.send_message(chat_id=message.chat.id, text='О чем вы хотите узнать дальше?', reply_markup=keyboard)
        user_ids[msg.id] =  message.from_user.id
        ic(msg.id)

@bot.callback_query_handler(func = lambda callback: callback.data in ['academy', 'poll', 'info_work'])
def new_step(callback):
    if callback.data == 'academy':
        message_text = (
        "*Академия бариста* — обучение в течение 4 дней, где ребята знакомятся с оборудованием и учатся варить эспрессо и классические напитки. ☕️✨\n\n"
        "*В программе обучения:*\n"
        "- <b>День 1: <i>Введение в мир кофе.</i></b>🌍☕️  \n"
        "  - История кофе и его сорта.  \n"
        "  - Знакомство с оборудованием: кофемашины, кофемолки и аксессуары.  \n\n"
        "- <b>День 2: <i>Основы приготовления эспрессо.</i></b> 🎓☕️  \n"
        "  - Техника помола и дозировки.  \n"
        "  - Практика: варим идеальный эспрессо!  \n\n"
        "- <b>День 3: <i>Классические кофейные напитки.</i></b> 🍵❤️  \n"
        "  - Приготовление капучино, латте и американо.  \n"
        "  - Искусство латте-арта: создаем красивые узоры на поверхности напитка. 🎨✨  \n\n"
        "- <b>День 4: <i>Углубленное изучение и практика.</i></b> 🔍💪  \n"
        "  - Советы по обслуживанию оборудования.  \n"
        "  - Итоговая практика: готовим напитки на скорость и качество.  \n\n"
        "По окончании курса вы получите сертификат и сможете уверенно работать в кофейне <b>Coffee Like</b>! 🎓🏆"
    )
        bot.reply_to(message=callback.message, text=message_text, parse_mode = "HTML")
    elif callback.data == 'poll':
        ic(callback.message.id)
        user_id = user_ids[callback.message.id]
        user_answers[user_id] = {}
        user_answers[user_id]["username"] = "@" + db.get_user(user_id)['username']
        current_date = datetime.now().date()
        user_answers[user_id]["date"] = current_date
        user_question_index[user_id] = 0  # Начинаем с первого вопроса
        users_is_poll[user_id] = 1
        ask_question(user_id)

    elif callback.data == 'info_work':
        message_text = (
            "*1. Срок работы бариста:*\n"
        "   В среднем 10 месяцев. ☕️📅✨\n\n"
        "*2. Возможности роста:*\n"
        "   Бариста могут развиваться внутри сети кофеен, а также переходить в другие отделы компании. "
        "Есть сотрудники, работающие уже 3-4 года. 🚀🌟\n\n"
        "*3. График работы:*\n"
        "   Гибкий, с различными вариантами смен, включая:\n"
        "   - 5/2 (реже); 📅\n"
        "   - 2/2, 2/3, 3/2; 🔄\n"
        "   - Полный рабочий день по 12 часов; ⏰\n"
        "   - Утренние смены (с 8:00/9:00/10:00 до 14:00) и вечерние смены (с 14:00 до 22:00). 🌅🌆\n\n"
        "*4. Оплата труда:*\n"
        "   - Стажер — 150 рублей в час; 💵\n"
        "   - После аттестации — 200 рублей в час; 💰\n"
        "   - Возможность увеличить ставку с дополнительной мотивацией от 1% до 3% от продаж. 📈"

        )
        bot.reply_to(message=callback.message, text=message_text, parse_mode = "Markdown")


@bot.message_handler(func = lambda message:message.text == 'гойда'[0:len(message.text)])
def goida(message):
    bot.send_message(message.chat.id, 'гойда'[len(message.text):5])


# all users




# admin

@bot.message_handler(commands = ['get_table'], func= lambda message: db.is_admin(message.from_user.id))
def get_table(message):
    ic(message.from_user.id)
    kb = InlineKeyboardMarkup(row_width=3)
    week = InlineKeyboardButton(text='Месяц', callback_data='week')
    mounth = InlineKeyboardButton(text='Неделя', callback_data='mounth')
    year = InlineKeyboardButton(text='Год', callback_data='year')
    all_data = InlineKeyboardButton(text='Все', callback_data='all')

    kb.add(week, mounth, year, all_data)
    bot.send_message(message.chat.id, "Таблицу за какой срок ты хочешь?", reply_markup=kb) #спрашиваем период

@bot.callback_query_handler(func = lambda callback: callback.message.text == "Таблицу за какой срок ты хочешь?") #если нажали на кнопку
def table(callback):
    date_to_days = {'week': 7, 'mounth' : 30, 'year': 365}
    if callback.data != 0:
        with open('db/applicants.xlsx', 'rb') as file:
            bot.send_document(chat_id=callback.message.chat.id, document=file)

    else:
        new_date = datetime.now().date() - timedelta(days=date_to_days[callback.data])
        filter_file = filter_exel(input_file='db/applicants.xlsx', date=date_to_days)
        with open(filter_file, 'rb') as file:
            bot.send_document(chat_id=callback.from_chat.id, document=file)
        try:
            os.remove(filter_file)
            print(f"Файл {filter_file} успешно удален.")
        except Exception as e:
            print(f"Ошибка при удалении файла: {e}")

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
    db.edit_notif(usr_id=usr_id,a=is_push)

@bot.message_handler(commands = ['ban'], func = lambda message: db.is_admin(message.from_user.id) or db.is_dev(message.from_user.id)) #ну бан
def ban(message):
    sent = bot.send_message(message.chat.id, "Кого банить?")
    bot.register_next_step_handler(sent, baned) #ждём ответа


def baned(message):
    usr_id = db.get_id(message.text)

    role = db.get_role(usr_id)
    if role is None:
        bot.send_message(message.chat.id, "Пользователь не найден в базе данных")
        return
    if role == 'user':
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
    elif role == 'admin' or role == 'dev':
        bot.send_message(message.chat.id, "Пользователь является админом, вы не можете его заблокировать")
    else:
        bot.send_message(message.chat.id, "Пользователь не найден в базе данных")


@bot.callback_query_handler(func = lambda callback : callback.data.split('_')[0] == 'ban')
def ban(callback):
    usr_id = db.get_id(callback.data.split('_')[1])
    ic(usr_id)
    db.edit_rol(usr_id=usr_id, role='ban')
    bot.send_message(callback.message.chat.id, "Пользователь заблокирован!")


@bot.callback_query_handler(func = lambda callback : callback.data.split('_')[0] == 'unban')
def unban(callback):
    usr_id = db.get_id(callback.data.split('_')[1])
    db.edit_rol(usr_id=usr_id, role='user')
    bot.send_message(callback.message.chat.id, "Пользователь разблокирован!")



@bot.message_handler(commands=['agree'], func=lambda message: db.is_admin(message.from_user.id) or db.is_dev(message.from_user.id))
def accept(message):
    sent = bot.send_message(message.chat.id, "Кого одобряем?")
    bot.register_next_step_handler(sent, accepted)  # ждём ответа

def accepted(message):
    usr_id = db.get_id(message.text)  # Предполагаем, что пользователь вводит ID или имя
    role = db.get_role(usr_id)
    # Здесь можно добавить логику для проверки, существует ли пользователь
    if role:  # Предполагаем, что есть такая функция
        bot.send_message(message.chat.id, "Пользователь найден. Информация отправлена.")
        bot.send_message(db.get_user(usr_id)["chat_id"], "Ваша заявка была одобрена, с вами свяжутся позже.")
    else:
        bot.send_message(message.chat.id, "Пользователь не найден.")


@bot.message_handler(commands = ['add_admin'], func= lambda message: db.is_dev(message.from_user.id))
def add_admin(message):
    sent = bot.send_message(message.chat.id, "Кого?")
    bot.register_next_step_handler(sent, admin)

def admin(message):
    username = message.text[1:]
    id = db.get_id(username)
    role = db.get_role(id)
    if not role:
        bot.send_message(message.chat.id, "Нет в бд")
        return
    db.edit_rol(id, 'admin')
    db.edit_notif(id, True)
    bot.send_message(message.chat.id, "теперь админ")

@bot.message_handler(commands = ['add_dev'], func= lambda message: db.is_dev(message.from_user.id))
def add_dev(message):
    sent = bot.send_message(message.chat.id, "Кого?")
    bot.register_next_step_handler(sent, dev)

def dev(message):
    username = message.from_user.username[1:]
    id = message.from_user.id
    role = db.get_role(id)
    if not role:
        bot.send_message(message.chat.id, "Нет в бд")
        return
    db.edit_rol(id, 'dev')
    db.edit_notif(id, True)
    bot.send_message(message.chat.id, "теперь супер-админ")


# admin

# user

def create_inline_keyboard(current_index, total_questions):
    keyboard = InlineKeyboardMarkup()
    back = InlineKeyboardButton("⏪", callback_data='back')
    forward = InlineKeyboardButton("⏩", callback_data='forward')
    if current_index == 0:
        keyboard.add(back)
    elif current_index == total_questions - 1:
        keyboard.add(forward)
    else:
        keyboard.add(back, forward)
    return keyboard

def create_reply_keyboard(options):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    for option in options:
        keyboard.add(KeyboardButton(option))
    return keyboard

@bot.message_handler(commands=['poll'], func = lambda message: not db.is_admin(message.from_user.id) and message.from_user.id in users_is_poll)
def start_quiz(message):
    ic(message.from_user.username)
    user_id = message.from_user.id
    user_answers[user_id] = {}
    user_answers[user_id]["username"] = "@" + message.from_user.username
    current_date = datetime.now().date()
    user_answers[user_id]["date"] = current_date
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
        msg = bot.send_message(user_id, "*Навигация по вопросам*", parse_mode='Markdown', reply_markup=inline_keyboard)
        user_message_ids_to_del[user_id] = msg.message_id
    else:
        count = 1
        answers = ""
        for i in questions:
            answers += f"{count}. {i[0]}: ___{user_answers[user_id][i[0]]}___\n"
            count += 1
        bot.send_message(user_id, "*Опрос пройден.*\nВот все ваши ответы:" + answers, parse_mode='markdown')
        add_row_to_excel(file_path=excel_file, new_row=user_answers[user_id])
        users_is_poll.remove(user_id)
        del user_answers[user_id]
        del user_question_index[user_id]
        del user_message_ids_to_del[user_id]

@bot.callback_query_handler(func=lambda call: call.data in ['back', 'forward'])
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
        if user_id in user_message_ids_to_del:
            try:
                bot.delete_message(chat_id=user_id, message_id=user_message_ids_to_del[user_id])
            except Exception as e:
                print(f"Ошибка при удалении сообщения: {e}")
        ask_question(user_id)
    elif message.text in answer_options:  # Закрытый вопрос
        # Сохраняем ответ
        user_answers[user_id][questions[user_question_index[user_id]][0]] = message.text

        user_question_index[user_id] += 1

        # Удаляем клавиатуру после получения ответа
        bot.send_message(user_id, "Спасибо за ваш ответ!", reply_markup=ReplyKeyboardRemove())
        if user_id in user_message_ids_to_del:
            try:
                bot.delete_message(chat_id=user_id, message_id=user_message_ids_to_del[user_id])
            except Exception as e:
                print(f"Ошибка при удалении сообщения: {e}")
        ask_question(user_id)

# user
@bot.message_handler(commands = ['goida'])
def goydu(message) -> None:
    text = '''ГОЙДА ГОЙДА ГОЙДА
ГОЙДА ГОЙДА ГОЙДА
ГОЙДА
ГОЙДА
ГОЙДА
ГОЙДА
ГОЙДА
ГОЙДА
ГОЙДА
ГОЙДА

ГОЙДА ГОЙДА ГОЙДА
ГОЙДА ГОЙДА ГОЙДА
ГОЙДА                ГОЙДА
ГОЙДА                ГОЙДА
ГОЙДА                ГОЙДА
ГОЙДА                ГОЙДА
ГОЙДА ГОЙДА ГОЙДА
ГОЙДА ГОЙДА ГОЙДА

               ГОЙДА

ГОЙДА                ГОЙДА
ГОЙДА                ГОЙДА
ГОЙДА               ГОЙДА! 
ГОЙДА              ГОЙДА!! 
ГОЙДА            ГОЙДА!!!! 
ГОЙДА          ГОЙДА!!!!!! 
ГОЙДА ГОЙДА ГОЙДА
ГОЙДА ГОЙДА ГОЙДА

   ГОЙДА ГОЙДА ГОЙДА
   ГОЙДА ГОЙДА ГОЙДА
   ГОЙДА                ГОЙДА
   ГОЙДА                ГОЙДА
   ГОЙДА                ГОЙДА
   ГОЙДА                ГОЙДА
   ГОЙДА                ГОЙДА
ГОЙДА!!! ГОЙДА!!! ГОЙДА!!!
ГОЙДА!!! ГОЙДА!!! ГОЙДА!!! 
ГОЙДА                          ГОЙДА
ГОЙДА                          ГОЙДА

     ГОЙДА ГОПДА ГОЙДА
    ГОЙДА ГОЙДА!!ГОЙДА
   ГОЙДА                  ГОЙДА
  ГОЙДА                   ГОЙДА
ГОЙДА!! ГОЙДА!! ГОЙДА
ГОЙДА!! ГОЙДА!!! ГОЙДА
ГОЙДА                      ГОЙДА
ГОЙДА                      ГОЙДА
ГОЙДА                      ГОЙДА
ГОЙДА                      ГОЙДА
🍑🍆💦😏🔥🍒🍭🍬🍸🍹🍷🍾💋💃🕺🍌🍈'''
    # Пасхалка с множеством "гойд", составляющих большую "гойду"
    bot.send_message(message.chat.id, text)
@bot.message_handler(func = lambda message : True)
def nepon(message):
    bot.send_sticker(message.chat.id, "CAACAgIAAxkBAAENDdRnJJApB2xNeugkIVf9JGr91IGilAACGVUAAopuGUkC4emTeHFA6zYE")
bot.polling(none_stop=True)