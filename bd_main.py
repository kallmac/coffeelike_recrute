import telebot
from telebot import types
import sqlite3

conn = sqlite3.connect('everyone.sql')
cur = conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS everyone (id int auto_increment primary key, tg_id varchar(255), tg_username varchar(255), status varchar(255), notif int)')
conn.commit()
cur.close()
conn.close()

