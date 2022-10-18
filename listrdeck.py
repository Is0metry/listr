from listr import Listr
import sqlite3,typing
from sqlite3 import Error
DB_FILE = 'listr.db'
def init_db(db_str:str = DB_FILE):
    with sqlite3.connect(db_str) as conn:
        conn.execute('''DROP TABLE IF EXISTS listr;''')
        conn.execute('''
        CREATE TABLE IF NOT EXISTS listr (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            parent INTEGER NOT NULL,
            task TEXT NOT NULL,
            completed INTEGER NOT NULL,
            FOREIGN KEY(parent) REFERENCES listr (id)
        );''')
        conn.execute('''INSERT INTO listr(parent,task,completed) VALUES(0,"Welcome To Listr",0); ''')
        conn.execute('''INSERT INTO listr(parent,task,completed) VALUES(0,"Add lists by typing",0); ''')
        conn.execute('''INSERT INTO listr(parent,task,completed) VALUES(0,"Add lists by typing",0); ''')
    print('initialized database')
def db_result_to_listr(tup):
        return Listr(tup[2],tup[0],tup[3],tup[1])
class ListrDB:
    def __init__(self,conn:sqlite3.Connection=None,root:int = 0) -> None:
        if conn is None:
            try:
                conn = sqlite3.connect(DB_FILE)
            except Error as e:
                print(e)
        self.conn = conn
        self.root = root
    def __del__(self):
        if self.conn is not None:
            self.conn.commit()
            self.conn.close()
            print('data connection closed. Goodbye!')
    def get(self,id:int)->Listr:
        query = f'SELECT * FROM listr WHERE id = {id}'
        cursor = self.conn.cursor()
        cursor = cursor.execute(query)
        data = cursor.fetchone()
        return db_result_to_listr(data)
    def get_sublist(self,parent:int)->typing.List[Listr]:
        query = f'SELECT * FROM listr WHERE parent={parent}'
        cursor = self.conn.cursor()
        children:typing.List[int] = []
        data = cursor.execute(query).fetchall()
        for d in data:
            children.append(db_result_to_listr(d))
        return children
    def get_root(self):
        return self.get_sublist(0)
    def add(self,task,parent):
        query = f'INSERT INTO listr(task,completed,parent) VALUES(\"{task}",false,{parent});'
        cursor = self.conn.cursor()
        cursor = cursor.execute(query)
        return Listr(task,id=cursor.lastrowid,parent=parent)
    def complete(id):
        query = f'UPDATE listr SET completed = 1 WHERE id = {id}'
if __name__ == '__main__':
    init_db()