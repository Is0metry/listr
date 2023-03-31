import re
import sqlite3
from typing import List
from listr import Listr

from listrdb import ListrDB
ROOT_LISTR = Listr("root", 0, parent=0)


class ListrUI(ListrDB):
    def __init__(self, conn: sqlite3.Connection = None, root=0) -> None:
        super().__init__(conn)
        self.parent = ROOT_LISTR
        self.current = self.get_root()

    def ls(self):
        print(self.parent)
        for k, v in enumerate(self.current):
            print(f'    {k+1}. ' + str(v))
        print('\n\n')

    def move_in(self, selection):
        self.conn.commit()
        self.parent = self.current[selection - 1]
        self.current = self.get_sublist(self.parent.id)

    def move_out(self):
        self.conn.commit()
        if self.parent.parent == 0:
            self.parent = ROOT_LISTR
            self.current = self.get_root()
        else:
            self.parent = self.get(self.parent.parent)
            self.current = self.get_sublist(self.parent.id)

    def add(self, new_tsk: str):
        new_item = super().add(new_tsk, self.parent.id)
        self.current.append(new_item)

    def complete(self, selection):
        completed = self.current[selection - 1]
        completed.completed = True
        super().complete(completed.id)

    def delete(self, selection):
        deleted_item = self.current[selection - 1]
        self.current.remove(deleted_item)
        super().delete(deleted_item.id)

    def repl(self):
        print("Listr 0.1")
        flag = True
        while flag:
            self.ls()
            command = input(':')
            if command.isnumeric():
                self.move_in(int(command))
            elif re.search('!\d+$', command) is not None:
                self.complete(int(command[1:]))
            elif re.search('-\d+$', command) is not None:
                self.delete(int(command[1:]))
            elif command == '<':
                self.move_out()
            elif command == 'quit':
                flag = False
            else:
                self.add(command)


if __name__ == '__main__':
    ui = ListrUI()
    ui.repl()
