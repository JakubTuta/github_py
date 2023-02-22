import csv
from tkinter import *

PLIK = "email.txt"

root = Tk()
root.title("Email")
root.resizable(False, False)


def fun():
    load_data()
    read_data()


def read_data():
    i = 0

    with open(PLIK, "r") as fd:
        reader = csv.reader(fd, delimiter=";")
        for data in reader:
            pustyLogin = Label(root, text=data[0], font=50)
            pustyLogin.grid(row=5+i, column=0, padx=10, pady=10, sticky=W)

            pustyEmail = Label(root, text=data[1], font=50)
            pustyEmail.grid(row=5+i, column=1, padx=10, pady=10, sticky=W)

            pustyHaslo = Label(root, text=data[2], font=50)
            pustyHaslo.grid(row=5+i, column=2, padx=10, pady=10, sticky=W)

            i += 1


def load_data():
    login = loginEntry.get()
    email = emailEntry.get()
    haslo = hasloEntry.get()
    with open("email.txt", "a", newline="") as fd:
        writerr = csv.writer(fd, delimiter=";")
        writerr.writerow([login, email, haslo])


Label(root, text="Login:", font=100).grid(row=0, column=0, padx=10, pady=10, sticky=W)
Label(root, text="Email:", font=100).grid(row=1, column=0, padx=10, pady=10, sticky=W)
Label(root, text="Hasło:", font=100).grid(row=2, column=0, padx=10, pady=10, sticky=W)

loginEntry = Entry(root, font=100)
loginEntry.grid(row=0, column=1, columnspan=2, padx=10, pady=10, sticky=EW)

emailEntry = Entry(root, font=100)
emailEntry.grid(row=1, column=1, columnspan=2, padx=10, pady=10, sticky=EW)

hasloEntry = Entry(root, font=100)
hasloEntry.grid(row=2, column=1, columnspan=2, padx=10, pady=10, sticky=EW)

Button(root, text="Zapisz", command=fun, font=100).grid(row=3, column=1, padx=10, pady=10, sticky=EW)
Label(root, text="Login", font=50).grid(row=4, column=0, padx=50, pady=10)
Label(root, text="Email", font=50).grid(row=4, column=1, padx=50, pady=10)
Label(root, text="Hasło", font=50).grid(row=4, column=2, padx=50, pady=10)

read_data()


root.mainloop()
