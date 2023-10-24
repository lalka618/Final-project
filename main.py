import tkinter as tk
from tkinter import ttk
import sqlite3


# Создаём класс для отображения главного окна
class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()

    # Поиск данных
    def search_records(self, name):
        name = ('%' + name + '%')
        self.db.cur.execute(
            '''SELECT * FROM db WHERE name LIKE ?''', (name,)
        )
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.cur.fetchall()]

    # Удаление данных
    def delete_records(self):
        for selection_item in self.tree.selection():
            self.db.cur.execute("""DELETE FROM db WHERE id = (?) """,
                                (self.tree.set(selection_item, '#1'),))
            self.db.conn.commit()
        self.view_records()

    # Обновление (редактирование) данных
    def update_record(self, name, tel, email, salary):
        self.db.cur.execute(''' UPDATE db SET name=?, tel=?, email=?, salary=? WHERE ID=?''',
                            (name, tel, email, salary, self.tree.set(self.tree.selection()[0], "#1")))
        self.db.conn.commit()
        self.view_records()

    # Добавление записи
    def add_records(self, name, tel, email, salary):
        self.db.insert_data(name, tel, email, salary)
        self.view_records()

    # Обновление виджета с таблицей
    def view_records(self):
        db.cur.execute('''SELECT * FROM db''')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row)
         for row in self.db.cur.fetchall()]

    # Создание связей основного окна с дочерними
    # Связь с окном добавления данных
    def open_dialog(self):
        Child()

    # Связь с окном редактирования данных
    def open_update_dialog(self):
        Update()

    # Связь с окном поиска данных
    def open_search_dialog(self):
        Search()

    # Отображение главного окна
    def init_main(self):
        # Создание виджета для отображения кнопок
        toolbar = tk.Frame(bg='#d7d8e0', bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        # Добавление кнопок
        # Кнопка добавления
        self.add_img = tk.PhotoImage(file='./icons/add.png')
        btn_open_dialog = tk.Button(toolbar, bg='#d7d8e0', bd=0,
                                    image=self.add_img,
                                    command=self.open_dialog)
        btn_open_dialog.pack(side=tk.LEFT)
        # Кнопка редактирования
        self.update_img = tk.PhotoImage(file='./icons/update.png')
        btn_open_update_dialog = tk.Button(toolbar, bg='#d7d8e0', bd=0,
                                           image=self.update_img,
                                           command=self.open_update_dialog)
        btn_open_update_dialog.pack(side=tk.LEFT)
        # Кнопка удаления
        self.delete_image = tk.PhotoImage(file='./icons/delete.png')
        btn_delete = tk.Button(toolbar, bg='#d7d8e0', bd=0,
                               image=self.delete_image,
                               command=self.delete_records)
        btn_delete.pack(side=tk.LEFT)
        # Кнопка поиска
        self.search_img = tk.PhotoImage(file='./icons/search.png')
        btn_open_search_dialog = tk.Button(toolbar, bg='#d7d8e0', bd=0,
                                           image=self.search_img,
                                           command=self.open_search_dialog)
        btn_open_search_dialog.pack(side=tk.LEFT)
        # Кнопка обновления
        self.refresh_img = tk.PhotoImage(file='./icons/refresh.png')
        btn_refresh = tk.Button(toolbar, bg='#d7d8e0', bd=0,
                                image=self.refresh_img,
                                command=self.view_records)
        btn_refresh.pack(side=tk.LEFT)

        # Создание виджета таблицы
        self.tree = ttk.Treeview(self, columns=('ID', 'name', 'tel', 'email', 'salary'),
                                 height=45, show='headings')
        # Задаём столбцы таблицы
        self.tree.column("ID", width=30, anchor=tk.CENTER)
        self.tree.column("name", width=200, anchor=tk.CENTER)
        self.tree.column("tel", width=150, anchor=tk.CENTER)
        self.tree.column("email", width=150, anchor=tk.CENTER)
        self.tree.column("salary", width=100, anchor=tk.CENTER)
        # Создаём отображаемый заголовок столбцам, отображаемым на виджете
        self.tree.heading("ID", text="ID")
        self.tree.heading("name", text="ФИО")
        self.tree.heading("tel", text="Телефон")
        self.tree.heading("email", text="E-mail")
        self.tree.heading("salary", text="Зарплата")

        self.tree.pack(side=tk.LEFT)


# Создаём класс для добавления данных в базу
class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

    # Создаём окно для добавления данных
    def init_child(self):
        # Задаём титул и размеры окна
        self.title('Добавить')
        self.geometry('400x200')
        self.resizable(False, False)
        self.grab_set()
        self.focus_set()
        # Отображаем название столбцов, куда вводятся данные
        label_fullname = tk.Label(self, text='ФИО')
        label_fullname.place(x=50, y=50)
        label_phone = tk.Label(self, text='Телефон')
        label_phone.place(x=50, y=80)
        label_email = tk.Label(self, text='E-mail')
        label_email.place(x=50, y=110)
        label_salary = tk.Label(self, text='Зарплата')
        label_salary.place(x=50, y=140)
        # Создаём поля для ввода данных
        self.entry_name = ttk.Entry(self)
        self.entry_name.place(x=200, y=50)
        self.entry_tel = ttk.Entry(self)
        self.entry_tel.place(x=200, y=80)
        self.entry_email = ttk.Entry(self)
        self.entry_email.place(x=200, y=110)
        self.entry_salary = ttk.Entry(self)
        self.entry_salary.place(x=200, y=140)

        # Добавляем кнопки закрытия окна и добавления данных
        self.btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        self.btn_cancel.place(x=300, y=170)
        self.btn_ok = ttk.Button(self, text='Добавить')
        self.btn_ok.place(x=220, y=170)
        self.btn_ok.bind('<Button-1>',
                         lambda event: self.view.add_records(self.entry_name.get(),
                                                             self.entry_tel.get(),
                                                             self.entry_email.get(),
                                                             self.entry_salary.get()))


# Создаём класс для редактирования данных в базе
class Update(Child):
    def __init__(self):
        super().__init__()
        self.init_edit()
        self.view = app
        self.db = db
        self.default_data()

    # Отображение в окне редактирования данных, которые можно изменить
    def default_data(self):
        self.db.cur.execute('''SELECT * FROM db WHERE ID=?''',
                            self.view.tree.set(self.view.tree.selection()[0], '#1'))
        row = self.db.cur.fetchone()
        self.entry_name.insert(0, row[1])
        self.entry_email.insert(0, row[2])
        self.entry_tel.insert(0, row[3])
        self.entry_salary.insert(0, row[4])

    # Создаём окно для обновления данных
    def init_edit(self):
        self.title("Обновление позиции")
        btn_edit = ttk.Button(self, text="Редактировать")
        btn_edit.place(x=205, y=170)
        btn_edit.bind("<Button-1>", lambda event: self.view.update_record(self.entry_name.get(),
                                                                          self.entry_tel.get(),
                                                                          self.entry_email.get(),
                                                                          self.entry_salary.get()))
        btn_edit.bind('<Button-1>', lambda event: self.destroy(), add='+')
        self.btn_ok.destroy()


# Создаём класс для поиска данных
class Search(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.init_search()
        self.view = app

    # Создаём окно для поиска данных
    def init_search(self):
        # Задаём название и размеры окна
        self.title("Поиск")
        self.geometry('300x100')
        self.resizable(False, False)
        self.grab_set()
        self.focus_set()
        # Создаём строку с требованием ввести искомые данные
        label_search = tk.Label(self, text='Поиск')
        label_search.place(x=50, y=20)
        # Создаём поле для ввода этих данных
        self.entry_search = ttk.Entry(self)
        self.entry_search.place(x=105, y=20, width=150)
        # Создаём кнопки закрытия окна и поиска данных
        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=185, y=50)
        btn_search = ttk.Button(self, text='Найти')
        btn_search.place(x=105, y=50)
        btn_search.bind('<Button-1>', lambda event:
                        self.view.search_records(self.entry_search.get())
                        )
        btn_search.bind('<Button-1>', lambda event: self.destroy(), add='+')


class DB:
    def __init__(self):
        self.conn = sqlite3.connect('db.db')
        self.cur = self.conn.cursor()
        self.cur.execute("""CREATE TABLE IF NOT EXISTS db(
        id INTEGER PRIMARY KEY,
        name TEXT,
        tel TEXT,
        email TEXT,
        salary TEXT);
        """)
        self.conn.commit()

    # Создаём метод для добавления данных в базу
    def insert_data(self, name, tel, email, salary):
        self.cur.execute("""
        INSERT INTO db(name,tel,email,salary)
        VALUES (?,?,?,?)
        """, (name, tel, email, salary))
        self.conn.commit()


if __name__ == '__main__':
    root = tk.Tk()
    db = DB()
    app = Main(root)
    app.pack()
    root.title("Список сотрудников компании")
    root.geometry('665x450')
    root.resizable(False, False)
    root.mainloop()
