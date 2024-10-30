import sqlite3

conn = sqlite3.connect('everyone.sql')
cur = conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS everyone (id int auto_increment primary key, tg_id varchar(255), tg_username varchar(255), status varchar(255), notif int)')
conn.commit()
cur.close()
conn.close()

class UsersTable:
    def get_user(usr_id: int, self) -> dict:
        pass

    def is_admin(usr_id, self) -> bool:
        conn = sqlite3.connect('everyone.sql')
        cur = conn.cursor()
        cur.execute('SELECT status from everyone WHERE tg_id = ?', (usr_id,))
        rol = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        if(rol=='admin' or rol=='dev'):
            return True
        else:
            return False

    def is_ban(usr_id, self) -> bool:
        conn = sqlite3.connect('everyone.sql')
        cur = conn.cursor()
        cur.execute('SELECT status from everyone WHERE tg_id = ?', (usr_id,))
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
        cur.execute('SELECT status from everyone WHERE tg_id = ?', (usr_id,))
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
        cur.execute('SELECT status from everyone WHERE tg_id = ?', (usr_id,))
        rol = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        if (rol == 'user' or rol == 'dev'):
            return True
        else:
            return False

    def add_user(usr_data: dict, self):
        pass

    def del_usr(usr_id, self):
        pass

    def edit_rol(usr_id, role: str,  self):
        pass

    def edit_notif(a: bool, self):
        pass