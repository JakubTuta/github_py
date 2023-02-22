from tkinter import *
import serial
from time import sleep

print("Start")
bluetooth = serial.Serial("COM7", 9600)
print("Connected")
bluetooth.flushInput()

# bluetooth.write(str.encode(str(2)))


def main():
    # decoded_data = "10100"
    a, b, c = 0, 0, 0

    while True:
        data = bluetooth.readline()
        decoded_data = str(data.decode())

        przycisk3, przycisk2, przycisk1, _, _ = decoded_data

        if przycisk1 == "1" and a < 100:
            a += 1
        elif przycisk1 == "0" and a > 0:
            a -= 1

        if przycisk2 == "1" and b < 100:
            b += 1
        elif przycisk2 == "0" and b > 0:
            b -= 1

        if przycisk3 == "1" and c < 100:
            c += 1
        elif przycisk3 == "0" and c > 0:
            c -= 1

        canvas.delete("all")

        canvas.create_rectangle(0, GAME_HEIGHT, BLOK_X,
                                GAME_HEIGHT - (BLOK_Y * a), fill="white")
        canvas.create_rectangle(BLOK_X, GAME_HEIGHT, BLOK_X * 2,
                                GAME_HEIGHT - (BLOK_Y * b), fill="white")
        canvas.create_rectangle(BLOK_X * 2, GAME_HEIGHT, BLOK_X * 3,
                                GAME_HEIGHT - (BLOK_Y * c), fill="white")

        root.update()
        sleep(0.01)


root = Tk()
root.attributes('-fullscreen', True)
root.title("Ilość liczb")
root.resizable(False, False)

GAME_HEIGHT = root.winfo_screenheight()
GAME_WIDTH = root.winfo_screenwidth()

MAX_WARTOSC = 100
ILOSC_LICZB = 3

BLOK_X = GAME_WIDTH / ILOSC_LICZB
BLOK_Y = GAME_HEIGHT / MAX_WARTOSC

canvas = Canvas(root, bd=0, bg="grey", highlightthickness=0,
                height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

if __name__ == "__main__":
    main()

root.mainloop()
