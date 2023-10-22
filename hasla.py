from random import choice, shuffle
from tkinter import *

import clipboard

root = Tk()
root.title("PASSWORD GENERATOR")
root.resizable(False, False)


def password_generator(length):
    result.delete(0, END)
    try:
        length = int(length)
    except ValueError:
        result.insert(0, "Incorrect length")
        return
    else:
        if length <= 5:
            result.insert(0, "Password must be at least 6 characters long")
            return

    smallLetters = [
        "a",
        "b",
        "c",
        "d",
        "e",
        "f",
        "g",
        "h",
        "i",
        "j",
        "k",
        "l",
        "m",
        "n",
        "o",
        "p",
        "r",
        "s",
        "t",
        "u",
        "v",
        "w",
        "x",
        "y",
        "z",
    ]
    bigLetters = [
        "A",
        "B",
        "C",
        "D",
        "E",
        "F",
        "G",
        "H",
        "I",
        "J",
        "K",
        "L",
        "M",
        "N",
        "O",
        "P",
        "R",
        "S",
        "T",
        "U",
        "V",
        "W",
        "X",
        "Y",
        "Z",
    ]
    numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    specialCharacters = ["!", "@", "#", "$", "%", "&"]
    password = []

    if varBigLetter.get() == 1:
        password.append(choice(bigLetters))
        length -= 1

    if varNumber.get() == 1:
        password.append(choice(numbers))
        length -= 1

    if varSpecialCharacter.get() == 1:
        password.append(choice(specialCharacters))
        length -= 1

    for i in range(length):
        password.append(choice(smallLetters))

    shuffle(password)
    result.insert(0, "".join(password))


def kopy():
    clipboard.copy(result.get())


Label(root, text="Insert password length:", font=("Arial", 15)).grid(
    row=0, column=0, padx=10, pady=10, sticky=W, columnspan=2
)

passwordLength = Entry(root, font=("Arial", 15))
passwordLength.grid(row=1, column=0, padx=10, pady=10, sticky=W)

varBigLetter = IntVar()
Checkbutton(
    root,
    text="Password must contain a big letter",
    variable=varBigLetter,
    font=("Arial", 12),
).grid(row=2, column=0, padx=10, pady=10, sticky=W, columnspan=2)

varNumber = IntVar()
Checkbutton(
    root, text="Password must contain a number", variable=varNumber, font=("Arial", 12)
).grid(row=3, column=0, padx=10, pady=10, sticky=W, columnspan=2)

varSpecialCharacter = IntVar()
Checkbutton(
    root,
    text="Password must contain a special character",
    variable=varSpecialCharacter,
    font=("Arial", 12),
).grid(row=4, column=0, padx=10, pady=10, sticky=W, columnspan=2)

Button(
    root,
    text="Show password",
    font=("Arial", 12),
    command=lambda: password_generator(passwordLength.get()),
).grid(row=5, column=0, padx=10, pady=10, ipadx=10, ipady=10, columnspan=2)

result = Entry(root, font=("Arial", 12))
result.grid(row=6, column=0, padx=10, pady=10, ipadx=50, sticky=EW)

Button(root, text="COPY", command=kopy).grid(
    row=6, column=1, padx=10, pady=10, ipadx=10, ipady=10, sticky=W
)


root.mainloop()
