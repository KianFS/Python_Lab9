import mysql.connector
import tkinter as tk
from datetime import datetime

db_password = "121314"

db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password=db_password
)

db_cursor = db_connection.cursor()

db_cursor.execute("CREATE DATABASE marvel")

marvel_connection = mysql.connector.connect(
    host="localhost",
    database="marvel",
    user="root",
    password=db_password
)

if marvel_connection.is_connected():
    print(" we are connected to mysql")

    tableQuery = """
        CREATE TABLE IF NOT EXISTS marvel_table (
            ID INT,
            MOVIE VARCHAR(150),
            DATE DATE,
            MCU_PHASE VARCHAR(150)
        )
    """
    marvel_cursor = marvel_connection.cursor()
    marvel_cursor.execute(tableQuery)

    with open("Marvel.txt", "r") as file:
        lines = file.readlines()
        for line in lines:
            data = line.strip().split()
            id_val = int(data[0])
            movie_val = data[1]
            try:
                date_val = datetime.strptime(data[2], "%B%d,%Y").date()
            except ValueError:
                date_val = datetime.strptime("January1,2000", "%B%d,%Y").date()
            phase_val = " ".join(data[3:])

            insertQuery1 = """
                INSERT INTO marvel_table (ID, MOVIE, DATE, MCU_PHASE)
                VALUES (%s, %s, %s, %s)
            """
            values = (id_val, movie_val, date_val, phase_val)
            marvel_cursor.execute(insertQuery1, values)

    marvel_connection.commit()
    print("now table is filled ")
else:
    print("connection is lost ")

window = tk.Tk()
window.resizable(False, False)
window.title("Marvel info")
window.geometry("600x450")

text_box = tk.Text(window, height=20, width=60)
text_box.pack()

dropdown_var = tk.StringVar(window)
dropdown = tk.OptionMenu(window, dropdown_var, "")
dropdown.pack()


def display_all_data():
    text_box.delete("1.0", tk.END)

    db_cursor.execute("USE marvel")

    db_cursor.execute("SELECT * FROM marvel_table")
    result = db_cursor.fetchall()

    for row in result:
        text_box.insert(tk.END, f"ID: {row[0]}\n")
        text_box.insert(tk.END, f"Movie: {row[1]}\n")
        text_box.insert(tk.END, f"Date: {row[2]}\n")
        text_box.insert(tk.END, f"MCU Phase: {row[3]}\n")


def dropdown_changed(*args):
    display_data()


def display_data():
    text_box.delete("1.0", tk.END)

    db_cursor.execute("USE marvel")

    db_cursor.execute("SELECT * FROM marvel_table WHERE ID = %s", (int(dropdown_var.get()),))
    result = db_cursor.fetchall()

    for row in result:
        text_box.insert(tk.END, f"ID: {row[0]}\n")
        text_box.insert(tk.END, f"Movie: {row[1]}\n")
        text_box.insert(tk.END, f"Date: {row[2]}\n")
        text_box.insert(tk.END, f"MCU Phase: {row[3]}\n")
        text_box.insert(tk.END, "--------------------\n")


def fillingDropDown():
    db_cursor.execute("USE marvel")

    db_cursor.execute("SELECT ID FROM marvel_table")
    ids = db_cursor.fetchall()

    dropdown["menu"].delete(0, "end")

    for id_val in ids:
        dropdown["menu"].add_command(label=id_val[0], command=tk._setit(dropdown_var, id_val[0]))


fillingDropDown()


def addButtonSubmit():
    add_window = tk.Toplevel(window)

    add_window.title("Add Entry")

    add_text_box = tk.Text(add_window, height=1, width=50)
    add_text_box.pack()

    def save_entry():
        entry = add_text_box.get("1.0", tk.END).strip()

        data = entry.split()
        id_val = int(data[0])
        movie_val = data[1]
        date_val = datetime.strptime(data[2], "%B%d,%Y").date()
        phase_val = " ".join(data[3:])

        db_cursor.execute(
            "INSERT INTO marvel_table (ID, MOVIE, DATE, MCU_PHASE) VALUES (%s, %s, %s, %s)",
            (id_val, movie_val, date_val, phase_val)
        )
        marvel_connection.commit()

        fillingDropDown()

        add_window.destroy()

    submit = tk.Button(add_window, text="Ok", command=save_entry)
    submit.pack()

    discard = tk.Button(add_window, text="Cancel", command=add_window.destroy)
    discard.pack()


addButton = tk.Button(window, text="Add", command=addButtonSubmit)
addButton.pack()

showAll = tk.Button(window, text="LIST ALL", command=display_all_data)
showAll.pack()

dropdown_var.trace("w", dropdown_changed)

window.mainloop()
