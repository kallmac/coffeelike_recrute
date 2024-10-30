import sqlite3

# Подключаемся к базе данных
conn = sqlite3.connect('everyone.sql')
cur = conn.cursor()

# Создаем таблицу users
cur.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tg_id TEXT,
        tg_username TEXT,
        status TEXT,
        notif INTEGER
    )
''')
# Сохраняем изменения и закрываем соединение
conn.commit()
cur.close()
conn.close()


