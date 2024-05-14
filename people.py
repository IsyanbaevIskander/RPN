from tkinter import *
from tkinter.ttk import Combobox
from tkcalendar import DateEntry
import csv
from datetime import datetime

def dismiss(window):
    window.grab_release()
    window.destroy()


def warning():
    warning = Toplevel()
    warning.title('Ошибка')
    warning.geometry('250x60')
    text = Label(warning, text='Заполните обязательные поля!', foreground='red')
    text.pack(anchor=CENTER)
    button = Button(warning, text='Закрыть', command=lambda: dismiss(warning))
    button.pack(anchor=CENTER)
    warning.grab_set()

def save_add(add_window):
    for i, j in add_entries.items():
        if i not in ('Отчество', 'Квартира') and len(j.get()) == 0:
            warning()
            return
    buffer = {}
    for i, j in add_entries.items():
        if type(j) is DateEntry:
            print('erfsd')
            buffer[i] = j.get_date()
        else:
            buffer[i] = j.get()
    people_data.append(buffer)
    list_output()
    dismiss(add_window)


def add():
    add_window = Toplevel()
    add_window.title('Добавление человека')
    add_window.geometry('500x500')
    parameters = ('Фамилия', 'Имя', 'Отчество', 'Национальность', 'Номер телефона')
    address_parameters = ('Почтовый индекс', 'Страна', 'Область', 'Район',
                          'Населенный пункт', 'Улица', 'Дом', 'Квартира')
    add_entries.clear()
    for i in range(len(parameters)):
        param = Label(add_window, text=parameters[i])
        param.place(x=10, y=10 + i * 20)
        param_entry = Entry(add_window)
        add_entries[parameters[i]] = param_entry
        param_entry.place(x=150, y=10 + i * 20)

    sex_label = Label(add_window, text='Пол')
    sex_label.place(x=10, y=110)
    sex_listbox = Combobox(add_window, values=('Мужской', 'Женский'))
    add_entries['Пол'] = sex_listbox
    sex_listbox.place(x=150, y=110)

    height_label = Label(add_window, text='Рост')
    height_label.place(x=10, y=130)
    height_spinbox = Spinbox(add_window, from_=30, to=250)
    add_entries['Рост'] = height_spinbox
    height_spinbox.place(x=150, y=130)

    weight_label = Label(add_window, text='Вес')
    weight_label.place(x=10, y=150)
    weight_spinbox = Spinbox(add_window, from_=1, to=400)
    add_entries['Вес'] = weight_spinbox
    weight_spinbox.place(x=150, y=150)

    date_label = Label(add_window, text='Дата рождения')
    date_label.place(x=10, y=170)
    date_entry = DateEntry(add_window)
    add_entries['Дата рождения'] = date_entry
    date_entry.place(x=150, y=170)

    a = Label(add_window, text='Адрес')
    a.place(x=10, y=200)

    for i in range(len(address_parameters)):
        param = Label(add_window, text=address_parameters[i])
        param.place(x=10, y=220 + i * 20)
        param_entry = Entry(add_window)
        add_entries[address_parameters[i]] = param_entry
        param_entry.place(x=150, y=220 + i * 20)

    info = Label(add_window, text='Все поля, кроме полей "Отчество", "Квартира", являются обязательными!', foreground='red')
    info.place(x=10, y=380)
    to_save = Button(add_window, text='Сохранить', command=lambda: save_add(add_window))
    to_save.place(x=10, y=400)
    add_window.grab_set()


def delete():
    if delete_entry.get().isdigit():
        input_number = int(delete_entry.get())
        if 0 < input_number <= len(people_data):
            people_data.pop(input_number - 1)

    delete_entry.delete(0, END)
    list_output()


def save_edit(edit_window, input_number):
    for i, j in add_entries.items():
        if i not in ('Отчество', 'Квартира') and len(j.get()) == 0:
            warning()
            return
    buffer = {}
    people_data.pop(input_number - 1)
    for i, j in add_entries.items():
        if type(j) is DateEntry:
            print('erfsd')
            buffer[i] = j.get_date()
        else:
            buffer[i] = j.get()
    people_data.append(buffer)
    list_output()
    dismiss(edit_window)

def editing():
    if edit_entry.get().isdigit():
        input_number = int(edit_entry.get())
        if 0 < input_number <= len(people_data):
            edit_window = Toplevel()
            edit_window.title('Редактирование')
            edit_window.geometry('500x500')
            parameters = ('Фамилия', 'Имя', 'Отчество', 'Национальность', 'Номер телефона')
            address_parameters = ('Почтовый индекс', 'Страна', 'Область', 'Район',
                                  'Населенный пункт', 'Улица', 'Дом', 'Квартира')
            add_entries.clear()

            for i in range(len(parameters)):
                param = Label(edit_window, text=parameters[i])
                param.place(x=10, y=10 + i * 20)
                param_entry = Entry(edit_window)
                param_entry.insert(0, people_data[input_number - 1][parameters[i]])
                add_entries[parameters[i]] = param_entry
                param_entry.place(x=150, y=10 + i * 20)

            sex_label = Label(edit_window, text='Пол')
            sex_label.place(x=10, y=110)
            sex_listbox = Combobox(edit_window, values=('Мужской', 'Женский'))
            sex_listbox.insert(0, people_data[input_number - 1]['Пол'])
            add_entries['Пол'] = sex_listbox
            sex_listbox.place(x=150, y=110)

            height_label = Label(edit_window, text='Рост')
            height_label.place(x=10, y=130)
            height_spinbox = Spinbox(edit_window, from_=30, to=250)
            height_spinbox.delete(0, END)
            height_spinbox.insert(0, people_data[input_number - 1]['Рост'])
            add_entries['Рост'] = height_spinbox
            height_spinbox.place(x=150, y=130)

            weight_label = Label(edit_window, text='Вес')
            weight_label.place(x=10, y=150)
            weight_spinbox = Spinbox(edit_window, from_=1, to=400)
            weight_spinbox.delete(0, END)
            weight_spinbox.insert(0, people_data[input_number - 1]['Вес'])
            add_entries['Вес'] = weight_spinbox
            weight_spinbox.place(x=150, y=150)

            date_label = Label(edit_window, text='Дата рождения')
            date_label.place(x=10, y=170)
            date_entry = DateEntry(edit_window)
            date_entry.delete(0, END)
            date_entry.insert(0, people_data[input_number - 1]['Дата рождения'])
            add_entries['Дата рождения'] = date_entry
            date_entry.place(x=150, y=170)

            a = Label(edit_window, text='Адрес')
            a.place(x=10, y=200)

            for i in range(len(address_parameters)):
                param = Label(edit_window, text=address_parameters[i])
                param.place(x=10, y=220 + i * 20)
                param_entry = Entry(edit_window)
                param_entry.insert(0, people_data[input_number - 1][address_parameters[i]])
                add_entries[address_parameters[i]] = param_entry
                param_entry.place(x=150, y=220 + i * 20)

            info = Label(edit_window, text='Все поля, кроме полей "Отчество", "Квартира", являются обязательными!', foreground='red')
            info.place(x=10, y=380)
            to_save = Button(edit_window, text='Сохранить', command=lambda: save_edit(edit_window, input_number))
            to_save.place(x=10, y=400)
            edit_window.grab_set()
    edit_entry.delete(0, END)


def list_output():
    people_list['state'] = NORMAL
    people_list.delete('1.0', END)
    for i in people_data:
        print(i)
    people_data.sort(key=lambda x: x['Дата рождения'], reverse=True)
    for i, j in enumerate(people_data):
        people_list.insert('1.0', f"{len(people_data) - i}) {j['Фамилия']} {j['Имя']} {j['Отчество']}, {j['Дата рождения']}, {j['Страна']}\n")
    people_list['state'] = DISABLED
    people_data.sort(key=lambda x: x['Дата рождения'])
    with open("C:/Users/Iskander/OneDrive/Рабочий стол/People/youngest.txt", 'w', encoding='utf-8') as file:
        if len(people_data) > 0:
            for i, j in people_data[-1].items():
                file.write(f'{i}: {j}\n')


def send_to_file():
    if len(people_data) > 0:
        with open("C:/Users\Iskander\OneDrive/Рабочий стол/People/data.csv", 'w', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(people_data[0].keys())
            for i in people_data:
                writer.writerow(i.values())


def get_from_file():
    address = from_file_entry.get()[1:-1]

    with open(f'{address}', 'r', encoding='utf-8') as file:
        rows = csv.DictReader(file)
        for row in rows:
            copy = row
            if tuple(row.keys()) != titles:
                return
            flag = True
            for j, k in row.items():
                if j not in ('Отчество', 'Квартира') and k is None:
                    flag = False
                    break
            if flag:
                copy['Дата рождения'] = datetime.strptime(copy['Дата рождения'], '%d/%m/%Y').date()
                if copy['Отчество'] is None:
                    copy['Отчество'] = ''
                if copy['Квартира'] is None:
                    copy['Квартира'] = ''

                people_data.append(row)
    list_output()


if __name__ == '__main__':
    people_data = []
    add_entries = {}
    titles = ('Фамилия', 'Имя', 'Отчество', 'Национальность', 'Номер телефона', 'Пол', 'Рост', 'Вес', 'Дата рождения',
              'Почтовый индекс', 'Страна', 'Область', 'Район', 'Населенный пункт', 'Улица', 'Дом', 'Квартира')
    root = Tk()
    root.title('Люди')
    root.geometry('900x700')

    adding = Button(text='Добавить человека', command=add)
    adding.place(x=10, y=20)

    delete_label = Label(text='Укажите номер человека, которого хотите удалить')
    delete_label.place(x=10, y=60)
    delete_entry = Entry()
    delete_entry.place(x=10, y=90)
    deleting = Button(text='Удалить человека', command=delete)
    deleting.place(x=150, y=85)

    edit_label = Label(text='Укажите номер человека, данные которого хотите изменить')
    edit_label.place(x=10, y=130)
    edit_entry = Entry()
    edit_entry.place(x=10, y=160)
    editing = Button(text='Редактировать', command=editing)
    editing.place(x=150, y=155)

    to_file = Button(text='Запись в файл', command=send_to_file)
    to_file.place(x=10, y=190)

    from_file_label = Label(text='Укажите ссылку на файл для считывания')
    from_file_label.place(x=10, y=220)
    from_file_entry = Entry()
    from_file_entry.place(x=10, y=250)
    from_file_button = Button(text='Импорт', command=get_from_file)
    from_file_button.place(x=150, y=245)

    people_list = Text(state=DISABLED, wrap='word')
    people_list.place(x=10, y=300)
    root.mainloop()
