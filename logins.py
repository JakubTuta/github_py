import sqlite3 as sql
import tkinter as tk

def main():
    root = tk.Tk()
    root.title("LOGIN AND PASSWORD DATABASE")
    root.grid_rowconfigure(4, weight=1)
    
    smallerFont = ("Arial", 15)
    buttonFont = ("Arial", 15, "italic")
    biggerFont = ("Arial", 25, "bold")
    
    tk.Label(text="Database for logins and passwords", font=biggerFont).grid(row=0, column=0, columnspan=5, padx=10, pady=15)
    
    nameEntry = tk.Entry(root, font=smallerFont)
    nameEntry.grid(row=1, column=0, padx=10, pady=15, ipady=5, ipadx=80)
    loginEntry = tk.Entry(root, font=smallerFont)
    loginEntry.grid(row=1, column=2, padx=10, pady=15, ipady=5, ipadx=50)
    passwordLabel = tk.Entry(root, font=smallerFont)
    passwordLabel.grid(row=1, column=4, padx=10, pady=15, ipady=5, ipadx=50)
    
    tk.Button(text="Add", font=buttonFont, width=12).grid(row=2, column=0, padx=10, pady=15)
    tk.Button(text="Delete 1", font=buttonFont, width=12).grid(row=2, column=2, padx=10, pady=15)
    tk.Button(text="Delete all", font=buttonFont, width=12).grid(row=2, column=4, padx=10, pady=15)
    
    tk.Button(text="Show 1", font=buttonFont, width=12).grid(row=3, column=1, padx=10, pady=15)
    tk.Button(text="Show all", font=buttonFont, width=12).grid(row=3, column=3, padx=10, pady=15)
    
    textLabel = tk.Text(root, height=15)
    scrollbar = tk.Scrollbar(root, orient="vertical", command=textLabel.yview)
    textLabel.config(yscrollcommand=scrollbar.set)
    textLabel.grid(row=4, column=0, columnspan=5, padx=10, pady=10, sticky="nesw")
    scrollbar.grid(row=4, column=4, sticky="nse")
    
    root.mainloop()

if __name__ == "__main__":
    main()