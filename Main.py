import sqlite3
from datetime import datetime
from tkinter import *
from tkinter import ttk


class Task:

    def __init__(self, task, date_time):
        self.task = task
        self.date_time = date_time

    def save_task(self):
        I.cursor.execute('INSERT INTO Task (task, data_tame) VALUES (?, ?)',
                       (self.task, self.date_time))

class User:
    obj = None

    def __init__(self):
        self.connection = sqlite3.connect('todo_database.db')
        self.cursor = self.connection.cursor()

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS Task (
        id INTEGER PRIMARY KEY,
        task TEXT NOT NULL,
        data_tame DATETIME NOT NULL
        )
        ''')

    def __new__(cls):
        if cls.obj is None:
            cls.obj = object.__new__(cls)
        return cls.obj

    def select(self):
        self.cursor.execute('SELECT task, strftime("%d-%m-%Y", DATE(data_tame)), strftime("%H:%M", TIME(data_tame)) FROM Task ORDER BY data_tame')
        self.tasks = self.cursor.fetchall()
        return self.tasks

    def commit(self):
        self.connection.commit()

    def close(self):
        self.connection.close()



I = User()
# date_time = "30/01/25 17:00"
# first_task = Task("дз ", datetime.strptime(date_time, "%d/%m/%y %H:%M"))
# first_task.save_task()
# I.commit()

window = Tk()
window.title("To Do List")
window.geometry('600x400')

columns = ("task", "data", "time")
tasks = I.select()

tree = ttk.Treeview(columns=columns, show="headings")
tree.pack(fill=BOTH, expand=1)

# определяем заголовки
tree.heading("task", text="Задание")
tree.heading("data", text="день")
tree.heading("time", text="время")

# добавляем данные
for task in tasks:
    tree.insert("", END, values=task)

window.mainloop()
I.close()
