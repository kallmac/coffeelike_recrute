import telebot
from telebot import types
import sqlite3

conn = sqlite3.connect('с_users.sql')
cur = conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS admins (id int auto_increment primary key, tg_id varchar(255), tg_username varchar(255), notif int)')
cur.execute('CREATE TABLE IF NOT EXISTS devs (id int auto_increment primary key, tg_id varchar(255), tg_username varchar(255))')
conn.commit()
cur.close()
conn.close()

