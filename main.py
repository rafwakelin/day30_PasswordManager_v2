from tkinter import *
from tkinter import messagebox
from random import randint, choice, shuffle
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def new_password():
    """Generates a random password and saves it on the clipboard"""
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '@', '*', '+']

    pw_letters = [choice(letters) for _ in range(randint(8, 10))]
    pw_symbols = [choice(symbols) for _ in range(randint(1, 1))]
    pw_numbers = [choice(numbers) for _ in range(randint(3, 4))]
    password_list = pw_numbers + pw_symbols + pw_letters
    shuffle(password_list)

    password = "".join(password_list)

    pw_entry.delete(0, END)
    pw_entry.insert(0, f"{password}")
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    """Saves the provided information to a txt file"""
    website = website_entry.get().title()
    username = username_entry.get()
    password = pw_entry.get()
    new_data = {
        website: {
            "username": username,
            "password": password,
        }
    }

    if len(website) == 0 or len(username) == 0 or len(password) == 0:
        messagebox.showerror(message="Please fill all the fields")
    else:
        try:
            with open("data.json", "r") as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            data.update(new_data)
            with open("data.json", "w") as data_file:
                json.dump(data, data_file, indent=4)
        finally:
            website_entry.delete(0, END)
            pw_entry.delete(0, END)


# -------------------------SEARCH PASSWORD -__------------------------- #
def search():
    search_website = website_entry.get().title()
    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="There are no passwords stored.")
    else:
        if search_website in data:
            user = data[search_website]["username"]
            pw = data[search_website]["password"]
            messagebox.showinfo(title="Password found", message=f"Website: {search_website}\nUsername: {user}\n"
                                                                f"Password: {pw}")
        else:
            messagebox.showinfo(message="Password not found")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200)
padlock = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=padlock)
canvas.grid(column=1, row=0)

website_label = Label(text="Website:")
website_label.grid(column=0, row=1)
username_label = Label(text="Email/Username:")
username_label.grid(column=0, row=2)
pw_label = Label(text="Password:")
pw_label.grid(column=0, row=3)

website_entry = Entry(width=21)
website_entry.focus()
website_entry.grid(column=1, row=1)
username_entry = Entry(width=38)
username_entry.grid(column=1, row=2, columnspan=2)
username_entry.insert(0, "wrafael.queiroz@icloud.com")
pw_entry = Entry(width=21)
pw_entry.grid(column=1, row=3)

pw_button = Button(text="Generate Password", command=new_password)
pw_button.grid(column=2, row=3)
add_button = Button(text="Add", width=36, command=save)
add_button.grid(column=1, row=4, columnspan=2)
search_button = Button(text="Search", width=13, command=search)
search_button.grid(column=2, row=1)

window.mainloop()
