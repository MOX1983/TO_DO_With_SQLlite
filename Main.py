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

def delete_task():
    for selected_item in tree.selection():
        item = tree.set(selected_item, '#1')
        I.cursor.execute('DELETE FROM Task WHERE task=?', (item,))
        row = tree.item(selected_item)
        I.tasks.remove(tuple(row["values"]))
    view_records()
    I.commit()

def add_task():
    new_task = Task(entryTask.get(), datetime.strptime(entryDate.get(), '%d-%m-%Y %H:%M'))
    new_task.save_task()
    I.commit()
    I.tasks = I.select()
    view_records()

def view_records():
    for i in tree.get_children():
        tree.delete(i)
    for task in I.tasks:
        tree.insert("", END, values=task)

I = User()

window = Tk()
window.title("To Do List")
window.geometry('600x400')

columns = ("task", "data", "time")
I.tasks = I.select()

tree = ttk.Treeview(columns=columns, show="headings")
tree.grid(row=3, column=0, sticky="nsew")

btn = Button(window, text="Удалить", command=delete_task)
btn.grid(row=2,column=1)

btn2 = Button(window, text="Добавить", command=add_task)
btn2.grid(row=2,column=0)

task_label = ttk.Label(window, text="Задание:")
entryTask = ttk.Entry()
task_label.grid(row=0, column=0)
entryTask.grid(row=0, column=1)

date_label = ttk.Label(window, text="День и Время ('%d-%m-%Y %H:%M'):")
entryDate = ttk.Entry()
date_label.grid(row=1, column=0)
entryDate.grid(row=1, column=1)

tree.heading("task", text="Задание")
tree.heading("data", text="День")
tree.heading("time", text="Время")

#добавить ещё одну колонку с ID, чтобы при удалении не удалялись все одинаковые задачи
tree.column("#1", stretch=True,  width=300)
tree.column("#2", stretch=NO, width=70)
tree.column("#3", stretch=NO, width=70)

view_records()

scrollbar = ttk.Scrollbar(orient=VERTICAL, command=tree.yview)
tree.configure(yscroll=scrollbar.set)
scrollbar.grid(row=3, column=1, sticky="ns")

window.mainloop()
I.close()
