import sqlite3

conn = sqlite3.connect('db/everyone.sql')
cur = conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS everyone (id int auto_increment primary key, tg_id varchar(255), tg_username varchar(255), status varchar(255), notif int, chat_id int)')
conn.commit()
cur.close()
conn.close()

class UsersTable:
    def add_user(self, usr_data: dict):
        conn = sqlite3.connect('db/everyone.sql')
        cur = conn.cursor()
        cur.execute('SELECT EXISTS(SELECT tg_id FROM everyone WHERE tg_id = ?)', (usr_data['id'],))
        existing = cur.fetchone()[0]
        if not existing:
            cur.execute('INSERT INTO everyone (tg_id, tg_username, status, notif, chat_id) VALUES(?, ?, ?, ?, ?)',
                        (usr_data["id"], usr_data["username"], usr_data["status"], usr_data["notif"], usr_data["chat_id"]))
        conn.commit()
        cur.close()
        conn.close()

    def del_user(self, usr_id):
        # Открываем соединение с базой данных
        conn = sqlite3.connect('db/everyone.sql')
        cur = conn.cursor()
        cur.execute('DELETE FROM everyone WHERE tg_id = ?', (usr_id,))
        conn.commit()
        cur.close()
        conn.close()

    def get_user(self, usr_id: int) -> dict:
        conn = sqlite3.connect('db/everyone.sql')
        cur = conn.cursor()
        cur.execute('SELECT * FROM everyone WHERE tg_id = ?', (usr_id, ))
        user_info = cur.fetchone() # массив с данными об 1 пользователе
        conn.commit()
        cur.close()
        conn.close()

        user_dict = {'id': user_info[1],
             'username': user_info[2],
             'status': user_info[3],
             'notif': user_info[4],
             'chat_id': user_info[5]
                     }
        return user_dict # возвращает словарь с инф ой о пользователе

    def is_dev(self, usr_id) -> bool:
        role = self.get_role(usr_id)
        if(role=='dev'):
            return True
        return False

    def is_admin(self, usr_id) -> bool:
        role = self.get_role(usr_id)
        if (role == 'dev' or role == 'admin'):
            return True
        return False

    def is_user(self, usr_id) -> bool:
        role = self.get_role(usr_id)
        if (role == 'dev' or role == 'user'):
            return True
        return False

    def is_ban(self, usr_id) -> bool:
        role = self.get_role(usr_id)
        if (role == 'ban'):
            return True
        return False

    def is_notif(self, usr_id: object) -> bool:
        conn = sqlite3.connect('db/everyone.sql')
        cur = conn.cursor()
        cur.execute(f'SELECT notif FROM everyone WHERE tg_id = ?', (usr_id,))
        ans = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        if(ans):
            return ans[0]
        return None

    def edit_rol(self, usr_id, role: str):
        conn = sqlite3.connect('db/everyone.sql')
        cur = conn.cursor()
        cur.execute('UPDATE everyone SET status = ? WHERE tg_id = ?', (role, usr_id))
        conn.commit()
        cur.close()
        conn.close()

    def edit_notif(self, usr_id, a: bool):
        conn = sqlite3.connect('db/everyone.sql')
        cur = conn.cursor()
        cur.execute('UPDATE everyone SET notif = ? WHERE tg_id = ?', (a, usr_id))
        conn.commit()
        cur.close()
        conn.close()

    def get_role(self, usr_id) -> str:
        conn = sqlite3.connect('db/everyone.sql')
        cur = conn.cursor()
        cur.execute('SELECT status FROM everyone WHERE tg_id = ?', (usr_id,))
        rol = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        if(rol):
            return rol[0]
        return None

    def get_id(self, username):
        conn = sqlite3.connect('db/everyone.sql')
        cur = conn.cursor()
        cur.execute('SELECT tg_id FROM everyone WHERE tg_username = ?', (username,))
        usr_id = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        if (usr_id):
            return usr_id[0]
        return None
    def get_notif(self, user):
        conn = sqlite3.connect('db/everyone.sql')
        cur = conn.cursor()
        cur.execute("SELECT chat_id FROM everyone WHERE (notif = 1 AND (status = 'admin' OR status = 'dev'))")
        table = cur.fetchall()
        conn.commit()
        cur.close()
        conn.close()
        return table

