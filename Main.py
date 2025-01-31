import sqlite3
from datetime import datetime
from tkinter import *
from tkinter import ttk


class Task:

    def __init__(self, task, date_time):
        self.task = task
        self.date_time = date_time


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

    def save_task(self, obj_task):
        self.cursor.execute('INSERT INTO Task (task, data_tame) VALUES (?, ?)',
                            (obj_task.task, obj_task.date_time))

    def select(self):
        self.cursor.execute(
            'SELECT task, strftime("%d-%m-%Y", DATE(data_tame)), strftime("%H:%M", TIME(data_tame)), id FROM Task ORDER BY data_tame')
        self.tasks = self.cursor.fetchall()

    def commit(self):
        self.connection.commit()

    def close(self):
        self.connection.close()


class Window:
    def __init__(self, I, window):
        self.I = I
        self.window = window
        self.interface()

    def interface(self):
        self.window.title("To Do List")
        self.window.geometry('600x400')

        columns = ("task", "data", "time", "id")
        self.I.select()

        self.tree = ttk.Treeview(columns=columns, show="headings")
        self.tree.grid(row=3, column=0, sticky="nsew")

        self.btn = Button(self.window, text="Удалить", command=self.delete_task)
        self.btn.grid(row=2, column=1)

        self.btn2 = Button(self.window, text="Добавить", command=self.add_task)
        self.btn2.grid(row=2, column=0)

        self.task_label = ttk.Label(self.window, text="Задание:")
        self.entryTask = ttk.Entry()
        self.task_label.grid(row=0, column=0)
        self.entryTask.grid(row=0, column=1)

        self.date_label = ttk.Label(self.window, text="День и Время ('%d-%m-%Y %H:%M'):")
        self.entryDate = ttk.Entry()
        self.date_label.grid(row=1, column=0)
        self.entryDate.grid(row=1, column=1)

        self.tree.heading("task", text="Задание")
        self.tree.heading("data", text="День")
        self.tree.heading("time", text="Время")
        self.tree.heading("id", text="id")

        self.tree.column("#1", stretch=False, width=200)
        self.tree.column("#2", stretch=False, width=70)
        self.tree.column("#3", stretch=False, width=70)
        self.tree.column("#4", stretch=False, width=40)

        self.view_records()

        self.scrollbar = ttk.Scrollbar(orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=self.scrollbar.set)
        self.scrollbar.grid(row=3, column=1, sticky="ns")

    def delete_task(self):
        for selected_item in self.tree.selection():
            item = self.tree.set(selected_item, '#4')
            self.I.cursor.execute('DELETE FROM Task WHERE id=?', (item,))
            self.I.select()
        self.view_records()
        self.I.commit()

    def add_task(self):
        new_task = Task(self.entryTask.get(), datetime.strptime(self.entryDate.get(), '%d-%m-%Y %H:%M'))
        self.I.save_task(new_task)
        self.I.commit()
        self.I.select()
        self.view_records()

    def view_records(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for task in self.I.tasks:
            self.tree.insert("", END, values=task)


user = User()
app = Window(user, Tk())
app.window.mainloop()
user.close()
