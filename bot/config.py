import sqlite3

conn = sqlite3.connect('everyone.sql')
cur = conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS everyone (id int auto_increment primary key, tg_id varchar(255), tg_username varchar(255), status varchar(255), notif int)')
conn.commit()
cur.close()
conn.close()
del conn
del cur

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
        conn = sqlite3.connect('everyone.sql')
        cur = conn.cursor()
        cur.execute('SELECT status FROM everyone WHERE tg_id = ?', (usr_id,))
        rol = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        if(rol=='admin' or rol=='dev'):
            return True
        else:
            return False

    def get_role(usr_id, self):
        cur.execute('SELECT EXISTS(SELECT status FROM users WHERE tg_username = ?)', (user,))
        if (cur.fetchone()[0]):
            return cur.fetchone()[0]
        return None
    def is_notif(usr_id, self):
        conn = sqlite3.connect('everyone.sql')
        cur = conn.cursor()
        cur.execute(f'SELECT notif FROM everyone WHERE tg_id = {usr_id}')
        ans = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        return ans

    def is_ban(usr_id, self) -> bool:
        conn = sqlite3.connect('everyone.sql')
        cur = conn.cursor()
        cur.execute('SELECT status FROM everyone WHERE tg_id = ?', (usr_id,))
        rol = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        if (rol == 'ban'):
            return True
        else:
            return False

    def is_dev(usr_id, self) -> bool:
        conn = sqlite3.connect('everyone.sql')
        cur = conn.cursor()
        cur.execute('SELECT status FROM everyone WHERE tg_id = ?', (usr_id,))
        rol = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        if (rol == 'dev'):
            return True
        else:
            return False

    def is_user(usr_id, self) -> bool:
        conn = sqlite3.connect('everyone.sql')
        cur = conn.cursor()
        cur.execute('SELECT status FROM everyone WHERE tg_id = ?', (usr_id,))
        rol = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        if (rol == 'user' or rol == 'dev'):
            return True
        else:
            return False

    def add_user(usr_data: dict, self):
        conn = sqlite3.connect('everyone.sql')
        cur = conn.cursor()
        cur.execute(f'INSERT INTO everyone (tg_id, tg_username, status, notif) VALUES({usr_data["id"]}, {usr_data["username"]}, {usr_data["status"]}, {usr_data["notif"]})')
        conn.commit()
        cur.close()
        conn.close()
        pass

    def del_usr(usr_id, self):
        conn = sqlite3.connect('everyone.sql')
        cur = conn.cursor()
        cur.execute('DELETE FROM everyone WHERE tg_id = ?', (usr_id,))
        conn.commit()
        cur.close()
        conn.close()

    def edit_rol(usr_id, role: str, self: object) -> object:
        conn = sqlite3.connect('everyone.sql')
        cur = conn.cursor()
        cur.execute('UPDATE users SET status = ? WHERE tg_id == ?', (role, usr_id))
        conn.commit()
        cur.close()
        conn.close()

    def edit_notif(usr_id, a: bool, self):
        conn = sqlite3.connect('everyone.sql')
        cur = conn.cursor()
        cur.execute('UPDATE users SET notif = ? WHERE tg_id == ?', (a, usr_id))
        conn.commit()
        cur.close()
        conn.close()
    def get_id(username, self):
        conn = sqlite3.connect('everyone.sql')
        cur = conn.cursor()
        cur.execute(f'SELECT tg_id FROM everyone WHERE tg_username = {username}')
        usr_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        if(usr_id):
            return usr_id
        return None
a = UsersTable()
a.add_user({"id":"228", "username":"goida", "status":"user", "notif" : 0})