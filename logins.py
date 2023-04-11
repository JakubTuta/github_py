import sqlite3 as sql
import tkinter as tk


def insertIntoDB(nameText, loginText, passwordText):
    if nameText == "" or loginText == "" or passwordText == "":
        return
    
    databaseConnection.execute(f"INSERT INTO data (name, login, password) \
        VALUES({nameText}, {loginText}, {passwordText})")
    databaseConnection.commit()


def showWholeDatabase(textLabel):
    textLabel.configure(state="normal")
    textLabel.delete(1.0, tk.END)
    textLabel.insert(tk.END, "{:<10}{:<70}{:<50}{:<50}\n".format("Id", "Name", "Login", "Password"))
    cursor = databaseConnection.execute("SELECT * FROM data")
    for i, (name, login, password) in enumerate(cursor):
        textLabel.insert(tk.END, "{:<10}{:<70}{:<50}{:<50}\n".format(i + 1, name, login, password))
    textLabel.configure(state="disabled")


def main():
    root = tk.Tk()
    root.title("LOGIN AND PASSWORD DATABASE")
    root.grid_rowconfigure(4, weight=1)
    
    smallerFont = ("Arial", 12)
    buttonFont = ("Arial", 14, "italic")
    biggerFont = ("Arial", 25, "bold")
    
    tk.Label(text="Database for logins and passwords", font=biggerFont).grid(row=0, column=0, columnspan=5, padx=10, pady=15)
    
    nameEntry = tk.Entry(root, font=smallerFont)
    nameEntry.grid(row=1, column=0, padx=10, pady=15, ipady=5, ipadx=30)
    loginEntry = tk.Entry(root, font=smallerFont)
    loginEntry.grid(row=1, column=2, padx=10, pady=15, ipady=5, ipadx=20)
    passwordEntry = tk.Entry(root, font=smallerFont)
    passwordEntry.grid(row=1, column=4, padx=10, pady=15, ipady=5, ipadx=20)
    
    textLabel = tk.Text(root, height=10, spacing3=5, wrap=tk.WORD, font=smallerFont)
    scrollbar = tk.Scrollbar(root, orient="vertical", command=textLabel.yview)
    textLabel.config(yscrollcommand=scrollbar.set)
    textLabel.grid(row=4, column=0, columnspan=5, padx=10, pady=10, sticky="nesw")
    scrollbar.grid(row=4, column=4, sticky="nse")
    
    textLabel.insert(tk.END, "{:<10}{:<70}{:<50}{:<50}\n".format("Id", "Name", "Login", "Password"))
    textLabel.configure(state="disabled")
    
    tk.Button(text="Add", font=buttonFont, width=12, command=lambda: insertIntoDB(nameEntry.get(), loginEntry.get(), passwordEntry.get())).grid(row=2, column=0, padx=10, pady=15)
    tk.Button(text="Delete 1", font=buttonFont, width=12).grid(row=2, column=2, padx=10, pady=15)
    tk.Button(text="Delete all", font=buttonFont, width=12).grid(row=2, column=4, padx=10, pady=15)
    
    tk.Button(text="Show name", font=buttonFont, width=12).grid(row=3, column=1, padx=10, pady=15)
    tk.Button(text="Show all", font=buttonFont, width=12, command=lambda: showWholeDatabase(textLabel)).grid(row=3, column=3, padx=10, pady=15)
    
    root.mainloop()


databaseConnection = sql.connect("loginsDB.db")

try:
    databaseConnection.execute('''
                               CREATE TABLE data
                               (
                                   name varchar(50),
                                   login varchar(50),
                                   password varchar(50)
                               );
                               ''')
except sql.OperationalError:
    pass


if __name__ == "__main__":
    main()

databaseConnection.close()