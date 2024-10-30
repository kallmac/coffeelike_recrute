import telebot
from telebot import types
import sqlite3

conn = sqlite3.connect('admins.sql')
cur = conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS admins (id int auto_increment primary key, tg_id varchar(255), tg_username varchar(255), notif int)')
conn.commit()
cur.close()
conn.close()

conn = sqlite3.connect('devs.sql')
cur = conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS devs (id int auto_increment primary key, tg_id varchar(255), tg_username varchar(255))')
conn.commit()
cur.close()
conn.close()

conn = sqlite3.connect('bans.sql')
cur = conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS devs (id int auto_increment primary key, tg_id varchar(255), tg_username varchar(255))')
conn.commit()
cur.close()
conn.close()

