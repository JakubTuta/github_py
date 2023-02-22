from tkinter import *
import json

PLIK = "email.json"

root = Tk()
root.title("Email")
root.resizable(False, False)


def save_data(data):
    with open(PLIK, "w") as file:
        json.dump(data, file, indent=4)


def load_data():
    try:
        with open(PLIK, "r") as file:
            data = json.load(file)
            return data
    except:
        return {}


def zapisz_dane():
    data = load_data()

    idd = data["id"]
    idd += 1
    data["id"] = idd

    listData = {}

    listData["login"] = loginEntry.get()
    listData["email"] = emailEntry.get()
    listData["haslo"] = hasloEntry.get()

    data[idd] = listData

    save_data(data)

    odczytaj_dane()


def odczytaj_dane():
    data = load_data()
    idd = data["id"]
    for i in range(1, idd + 1):
        login = data[f"{i}"]["login"]
        email = data[f"{i}"]["email"]
        haslo = data[f"{i}"]["haslo"]

        Label(root, text=login, font=50).grid(row=5+i-1, column=0, padx=10, pady=10, sticky=W)
        Label(root, text=email, font=50).grid(row=5+i-1, column=1, padx=10, pady=10, sticky=W)
        Label(root, text=haslo, font=50).grid(row=5+i-1, column=2, padx=10, pady=10, sticky=W)

try:
    oneTimeData = {}
    oneTimeData["id"] = 0

    with open(PLIK, "w") as file:
        json.dump(oneTimeData, file, indent=4)
except:
    pass

Label(root, text="Login:", font=100).grid(row=0, column=0, padx=10, pady=10, sticky=W)
Label(root, text="Email:", font=100).grid(row=1, column=0, padx=10, pady=10, sticky=W)
Label(root, text="Hasło:", font=100).grid(row=2, column=0, padx=10, pady=10, sticky=W)

loginEntry = Entry(root, font=100)
loginEntry.grid(row=0, column=1, columnspan=2, padx=10, pady=10, sticky=EW)

emailEntry = Entry(root, font=100)
emailEntry.grid(row=1, column=1, columnspan=2, padx=10, pady=10, sticky=EW)

hasloEntry = Entry(root, font=100)
hasloEntry.grid(row=2, column=1, columnspan=2, padx=10, pady=10, sticky=EW)

Button(root, text="Zapisz", command=zapisz_dane, font=100).grid(row=3, column=1, padx=10, pady=10, sticky=EW)

Label(root, text="Login", font=50).grid(row=4, column=0, padx=50, pady=10)
Label(root, text="Email", font=50).grid(row=4, column=1, padx=50, pady=10)
Label(root, text="Hasło", font=50).grid(row=4, column=2, padx=50, pady=10)

odczytaj_dane()

root.mainloop()
