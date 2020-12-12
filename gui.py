import tkinter
from tkinter import *
from PIL import ImageTk, Image
from db import search_ability, show_table, insert_card, delete_card, clean_table, delete_base, change_card, delete_some_cards, \
    create_db, load_triggers_index, insert_data_t1, insert_data_t2, close_base, connect_postgres, insert_data_t3, delete_chosen_card
from tkinter import font as tkFont

root = Tk()
root.geometry("800x540+100+100")
root.resizable(False, False)
content = Frame(root, width = 800, height=600)
content.pack(fill="both", side="top", expand=True)

background = ImageTk.PhotoImage(Image.open("image.jpg"))

def get_power(power):
    window2 = Toplevel()
    window2.geometry("400x250+400+400")
    label2 = Label(window2, text=search_ability(power))
    label2.pack()

def btn1():
    window = Toplevel()
    window.geometry("400x250+400+400")
    label = Label(window, text="Введите название карты")
    label.pack()
    entry = Entry(window)
    entry.pack()
    Temp = Button(window, text="Отправить", command=lambda: get_power(entry.get()))
    Temp.pack()

def btn2():
    window = Toplevel()
    window.geometry("600x250+400+400")
    label = Label(window, text="Введите имя карты")
    label.pack()
    entry = Entry(window, width=40)
    entry.pack()
    Temp = Button(window, text="Отправить", command=lambda: delete_chosen_card(entry.get()))
    Temp.pack()

def for_btn4(dbname):
    window = Toplevel()
    window.geometry("600x600+700+100")
    table = show_table(dbname)
    for i in range(len(table)):
        exec('Label%d=Label(window,text="%s")\nLabel%d.pack()' % (i, table[i], i))

def btn4():
    window = Toplevel()
    window.geometry("600x250+400+400")
    label = Label(window, text="Введите имя таблицы")
    label.pack()
    entry = Entry(window, width = 80)
    entry.pack()
    Temp = Button(window, text="Отправить", command=lambda: for_btn4(entry.get()))
    Temp.pack()

def push_card(string):
    temp = string.split(', ')
    a1 = temp[0]
    a2 = temp[1]
    a3 = 'Северные королевства'
    a4 = temp[2]
    a5 = temp[3]
    insert_card(a1, a2, a3, a4, a5)

def btn5():
    window = Toplevel()
    window.geometry("600x250+400+400")
    label = Label(window, text="Введите название карты, расположение, силу и способность")
    label.pack()
    entry = Entry(window, width = 80)
    entry.pack()
    Temp = Button(window, text="Отправить", command=lambda: push_card(entry.get()))
    Temp.pack()

def btn6():
    delete_card()

def btn7():
    window = Toplevel()
    window.geometry("600x250+400+400")
    label = Label(window, text="Введите имя базы данных")
    label.pack()
    entry = Entry(window, width=40)
    entry.pack()
    Temp = Button(window, text="Отправить", command=lambda: clean_table(entry.get()))
    Temp.pack()

def btn8():
    window = Toplevel()
    window.geometry("600x250+400+400")
    label = Label(window, text="Введите имя базы данных")
    label.pack()
    entry = Entry(window, width=40)
    entry.pack()
    Temp = Button(window, text="Отправить", command=lambda: delete_base(entry.get()))
    Temp.pack()

def update_card(string):
    temp = string.split(', ')
    a1 = temp[0]
    a2 = temp[1]
    change_card(a1, a2)

def btn9():
    window = Toplevel()
    window.geometry("600x250+400+400")
    label = Label(window, text="Введите новую силу карты и ее имя")
    label.pack()
    entry = Entry(window, width=80)
    entry.pack()
    Temp = Button(window, text="Отправить", command=lambda: update_card(entry.get()))
    Temp.pack()


def btn10():
    window = Toplevel()
    window.geometry("600x250+400+400")
    label = Label(window, text="Введите название базы данных")
    label.pack()
    entry = Entry(window, width=40)
    entry.pack()
    Temp = Button(window, text="Отправить", command=lambda: create_db(entry.get()))
    Temp.pack()

def btn11():
    load_triggers_index()

def btn12():
    insert_data_t1()
    insert_data_t2()
    insert_data_t3()

def btn13():
    window = Toplevel()
    window.geometry("600x250+400+400")
    label = Label(window, text="Введите силу карт")
    label.pack()
    entry = Entry(window, width=40)
    entry.pack()
    Temp = Button(window, text="Отправить", command=lambda: delete_some_cards(entry.get()))
    Temp.pack()

def btn14():
    window = Toplevel()
    window.geometry("600x250+400+400")
    label = Label(window, text="Введите название базы данных")
    label.pack()
    entry = Entry(window, width=40)
    entry.pack()
    Temp = Button(window, text="Отправить", command=lambda: close_base(entry.get()))
    Temp.pack()

def btn15():
    connect_postgres()

helv = tkFont.Font(family='Helvetica', size=10)

Btn1 = Button(content, text="Вывести способн.", width=15, height=3, background="#370008", foreground="#ccc",
              font=helv, command = btn1)
Btn2 = Button(content, text="Удалить выбр. карту", width=15, height=3, background="#370008", foreground="#ccc",
              font=helv, command = btn2)
Btn3 = Button(content, text="Выход", width=15, height=3, background="#370008", foreground="#ccc",
              font=helv, command = root.quit)
Btn4 = Button(content, text="Покажи таблицу", width=15, height=3, background="#370008", foreground="#ccc",
              font=helv, command = btn4)
Btn5 = Button(content, text="Добавить карту", width=15, height=3, background="#370008", foreground="#ccc",
              font=helv, command = btn5)
Btn6 = Button(content, text="Удалить карту", width=15, height=3, background="#370008", foreground="#ccc",
              font=helv, command = btn6)
Btn7 = Button(content, text="Очистить таблицу", width=15, height=3, background="#370008", foreground="#ccc",
              font=helv, command = btn7)
Btn8 = Button(content, text="Удаление бд", width=15, height=3, background="#370008", foreground="#ccc",
              font=helv, command = btn8)
Btn9 = Button(content, text="Изменение силы", width=15, height=3, background="#370008", foreground="#ccc",
              font=helv, command = btn9)
Btn10 = Button(content, text="Создание бд", width=15, height=3, background="#370008", foreground="#ccc",
              font=helv, command = btn10)
Btn11 = Button(content, text="Триггер и индекс", width=15, height=3, background="#370008", foreground="#ccc",
              font=helv, command = btn11)
Btn12 = Button(content, text="Загрузка таблиц", width=15, height=3, background="#370008", foreground="#ccc",
              font=helv, command = btn12)
Btn13 = Button(content, text="Удалить неск. карт", width=15, height=3, background="#370008", foreground="#ccc",
              font=helv, command = btn13)
Btn14 = Button(content, text="Закрыть бд", width=15, height=3, background="#370008", foreground="#ccc",
              font=helv, command = btn14)
Btn15 = Button(content, text="Подсключ. postgr", width=15, height=3, background="#370008", foreground="#ccc",
              font=helv, command = btn15)

backgroundlabel = tkinter.Label(content, image=background)
backgroundlabel.image = background

backgroundlabel.place(x=0, y=0, relwidth=1, relheight=1)

Btn10.grid(row=0, column=0, padx = 105, pady=5)
Btn10.lift()

Btn12.grid(row=1, column=0)
Btn12.lift()

Btn4.grid(row=2, column=0, pady=5)
Btn4.lift()

Btn2.grid(row=3, column=0)
Btn2.lift()

Btn3.grid(row=7, column=1)
Btn3.lift()

Btn6.grid(row=0, column=2, padx = 105)
Btn6.lift()

Btn7.grid(row=1, column=2)
Btn7.lift()

Btn13.grid(row=2, column=2)
Btn13.lift()

Btn9.grid(row=3, column=2)
Btn9.lift()

Btn1.grid(row=4, column=0, pady=5)
Btn1.lift()

Btn15.grid(row=4, column=2)
Btn15.lift()

Btn5.grid(row=5, column=0)
Btn5.lift()

Btn14.grid(row=5, column=2)
Btn14.lift()

Btn11.grid(row=6, column=0, pady=5)
Btn11.lift()

Btn8.grid(row=6, column=2)
Btn8.lift()

root.mainloop()
