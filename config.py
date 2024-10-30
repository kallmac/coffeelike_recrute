import sqlite3

conn = sqlite3.connect('everyone.sql')
cur = conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS everyone (id int auto_increment primary key, tg_id varchar(255), tg_username varchar(255), status varchar(255), notif int)')
conn.commit()
cur.close()
conn.close()

class UsersTable:
    def get_user(usr_id: int, self) -> dict:
        conn = sqlite3.connect('everyone.sql')
        cur = conn.cursor()
        cur.execute('SELECT * FROM everyone WHERE tg_id == usr_id')
        user_info = cur.fetchone() # массив с данными об 1 пользователе
        conn.commit()
        cur.close()
        conn.close()

        user_dict = {'id': user_info[1],
             'username': user_info[2],
             'status': user_info[3],
             'notif': user_info[4]}
        return user_dict # возвращает словарь с инфой о пользователе

    def is_admin(usr_id, self) -> bool:
        pass

    def is_ban(usr_id, self) -> bool:
        pass

    def is_dev(usr_id, self) -> bool:
        pass

    def is_user(usr_id, self) -> bool:
        pass

    def add_user(usr_data: dict, self):
        conn = sqlite3.connect('everyone.sql')
        cur = conn.cursor()
        cur.execute('INSERT INTO everyone (tg_id, tg_username, status, notif)VALUES(%s, %s, %s, %s)' % (dict['id'], dict['username'], dict['status'], dict['notif']))
        conn.commit()
        cur.close()
        conn.close()
        pass

    def del_usr(usr_id, self):
        pass

    def edit_rol(usr_id, role: str,  self):
        pass

    def edit_notif(a: bool, self):
        pass