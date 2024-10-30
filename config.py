import sqlite3

conn = sqlite3.connect('everyone.sql')
cur = conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS devs (id int auto_increment primary key, tg_id varchar(255), tg_username varchar(255), status varchar(255), notif int)')
conn.commit()
cur.close()
conn.close()

class UsersTable:
    def get_user(usr_id: int, self) -> dict:
        pass

    def is_admin(usr_id, self) -> bool:
        pass

    def is_ban(usr_id, self) -> bool:
        pass

    def is_dev(usr_id, self) -> bool:
        pass

    def is_user(usr_id, self) -> bool:
        pass

    def add_user(usr_data: dict, self):
        pass

    def del_usr(usr_id, self):
        pass

    def edit_rol(usr_id, role: str,  self):
        pass

    def edit_notif(a: bool, self):
        pass