from tkinter import *
import pygame
from random import shuffle
from time import sleep

ILOSC_LICZB = 0
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
GRAY = (100, 100, 100)

def zamknij(odpowiedz):

    global ILOSC_LICZB
    try:
        ILOSC_LICZB = int(odpowiedz)
    except TypeError:
        return
    
    if ILOSC_LICZB < 1 or ILOSC_LICZB > 512:
        return

    top.destroy()


top = Tk()
top.title("Ilość liczb")
top.resizable(False, False)
top.attributes('-topmost', True)

Label(top, text="Podaj ilość liczb:", font=("Times New Roman", 20)).grid(row=0, column=0, padx=20, pady=10)
Label(top, text="(1 - 512)", font=("Times New Roman", 15, "italic")).grid(row=1, column=0, padx=10, pady=10)
Label(top, text="Wybierz rodzaj sortowania:", font=("Times New Roman", 20)).grid(row=0, column=1, padx=20, pady=10)

var = StringVar(value="bubble")

Radiobutton(top, text="Sortowanie bąbelkowe", variable=var, value="bubble", font=("Times New Roman", 15)).grid(row=1, column=1, padx=10, pady=10, sticky=W)
Radiobutton(top, text="Sortowanie przez wstawianie", variable=var, value="insertion", font=("Times New Roman", 15)).grid(row=2, column=1, padx=10, pady=10, sticky=W)
Radiobutton(top, text="Sortowanie przez wybieranie", variable=var, value="selection", font=("Times New Roman", 15)).grid(row=3, column=1, padx=10, pady=10, sticky=W)
Radiobutton(top, text="Bogo sort", variable=var, value="bogo", font=("Times New Roman", 15)).grid(row=4, column=1, padx=10, pady=10, sticky=W)
Radiobutton(top, text="Cocktail shaker sort", variable=var, value="shaker", font=("Times New Roman", 15)).grid(row=5, column=1, padx=10, pady=10, sticky=W)
Radiobutton(top, text="Quicksort", variable=var, value="quick", font=("Times New Roman", 15)).grid(row=6, column=1, padx=10, pady=10, sticky=W)
Radiobutton(top, text="Sortowanie grzebieniowe (comb sort)", variable=var, value="comb", font=("Times New Roman", 15)).grid(row=7, column=1, padx=10, pady=10, sticky=W)
Radiobutton(top, text="Sortowanie pozycyjne (radix sort)", variable=var, value="radix", font=("Times New Roman", 15)).grid(row=8, column=1, padx=10, pady=10, sticky=W)

odpowiedz = Entry(top, font=("Times New Roman", 15))
odpowiedz.grid(row=2, column=0, padx=10, pady=10, ipadx=10)

Label(top, text="Wybierz prędkość sortowania (niższa liczba - szybsze sortowanie):", font=("Times New Roman", 15)).grid(row=9, column=0, columnspan=2, padx=10, pady=20)

delayVar = DoubleVar(value=0.005)
delayScale = Scale(top, from_=0.005, to=1.0, digits=4, resolution=0.005, orient=HORIZONTAL, variable=delayVar).grid(row=10, column=0, columnspan=2, padx=10, pady=10, ipadx=100)

gotowy = Button(top, text="Pokaż!", font=("Times New Roman", 15), command=lambda: zamknij(odpowiedz.get())).grid(row=11, column=0, columnspan=2, padx=10, pady=10, ipadx=30)

top.mainloop()


def quick_sort(liczby, low, high):
    def partition(liczby, low, high):
        pivot = liczby[high]
        i = low - 1
        for j in range(low, high):
            if liczby[j] <= pivot:
                i = i + 1
                (liczby[i], liczby[j]) = (liczby[j], liczby[i])
        (liczby[i + 1], liczby[high]) = (liczby[high], liczby[i + 1])
        return i + 1

    WIN.fill(GRAY)
    for index, liczba in enumerate(liczby):
        x = BLOK_X * index
        y = HEIGHT - (BLOK_Y * liczba)
        pygame.draw.rect(WIN, WHITE, (x, y, BLOK_X, BLOK_Y * liczba))

    try:
        x = BLOK_X * low
        y = HEIGHT - (BLOK_Y * liczby[low])
        pygame.draw.rect(WIN, GREEN, (x, y, BLOK_X, BLOK_Y * liczby[low]))
    except IndexError:
        pass
    
    x = BLOK_X * high
    y = HEIGHT - (BLOK_Y * liczby[high])
    pygame.draw.rect(WIN, GREEN, (x, y, BLOK_X, BLOK_Y * liczby[high]))

    pygame.display.update()
    sleep(DELAY)

    if low < high:
        pi = partition(liczby, low, high)
        quick_sort(liczby, low, pi - 1)
        quick_sort(liczby, pi + 1, high)


def szybszy_bubble_sort():
    for i in range(ILOSC_LICZB - 1):
        czy = 0
        for j in range(ILOSC_LICZB - i - 1):
            if liczby[j] > liczby[j+1]:
                czy = 1
                liczby[j], liczby[j+1] = liczby[j+1], liczby[j]

                draw(liczby)
                x = BLOK_X * (j + 1)
                y = HEIGHT - (BLOK_Y * liczby[j+1])
                pygame.draw.rect(WIN, GREEN, (x, y, BLOK_X, BLOK_Y * liczby[j+1]))
                x = BLOK_X * (j)
                y = HEIGHT - (BLOK_Y * liczby[j])
                pygame.draw.rect(WIN, GREEN, (x, y, BLOK_X, BLOK_Y * liczby[j]))
                pygame.display.update()
                sleep(DELAY)

        if czy == 0:
            break


def insertion_sort():
    for i in range(1, ILOSC_LICZB):

        pom = liczby[i]
        j = i - 1
        while j >= 0 and liczby[j] > pom:
            liczby[j + 1] = liczby[j]
            j -= 1

            draw(liczby)
            x = BLOK_X * j
            y = HEIGHT - (BLOK_Y * liczby[j])
            pygame.draw.rect(WIN, GREEN, (x, y, BLOK_X, BLOK_Y * liczby[j]))
            pygame.display.update()
            sleep(DELAY)

        liczby[j+1] = pom


def selection_sort():
    minimum = MAX_WARTOSC + 1
    for i in range(0, ILOSC_LICZB):
        for j in range(i, ILOSC_LICZB):
            if liczby[j] < minimum:
                minimum = liczby[j]

        for j in range(i, ILOSC_LICZB):
            if liczby[j] == minimum:
                draw(liczby)
                x = BLOK_X * j
                y = HEIGHT - (BLOK_Y * liczby[j])
                pygame.draw.rect(WIN, GREEN, (x, y, BLOK_X, BLOK_Y * liczby[j]))
                pygame.display.update()

                pom = liczby[j]
                liczby[j] = liczby[i]
                liczby[i] = pom

                sleep(DELAY)

        minimum = MAX_WARTOSC + 1


def bogo_sort():
    def posortowane():
        for i in range(0, len(liczby) - 1):
            if liczby[i] > liczby[i + 1]:
                return False
        return True

    while not posortowane():
        shuffle(liczby)

        draw(liczby)
        pygame.display.update()
        sleep(DELAY)


def shaker_sort():
    swap = True
    start = 0
    end = ILOSC_LICZB - 1

    while (swap == True):
        swap = False

        draw(liczby)
        pygame.display.update()
        sleep(DELAY)

        for a in range(start, end):
            if (liczby[a] > liczby[a+1]):
                liczby[a], liczby[a+1] = liczby[a+1], liczby[a]
                swap = True

        if(swap == False):
            end = end-1

        for a in range(end - 1, start - 1, -1):
            if(liczby[a] > liczby[a+1]):
                liczby[a], liczby[a+1] = liczby[a+1], liczby[a]
                swap = True

        start = start + 1


def comb_sort():
    gap = len(liczby)
    shrink = 1.3
    sorted = False
    
    while not sorted:
        gap = int(gap / shrink)
        if gap <= 1:
            gap = 1
            sorted = True
        
        i = 0
        while i + gap < len(liczby):
            if liczby[i] > liczby[i + gap]:
                liczby[i], liczby[i + gap] = liczby[i + gap], liczby[i]
                sorted = False
            i += 1
            
            draw(liczby)
            pygame.display.update()
            sleep(DELAY // 2)


def radix_sort():
    def countingSort(arr, exp1):
        n = len(arr)

        output = [0] * (n)
        count = [0] * (10)

        for i in range(0, n):
            index = arr[i] // exp1
            count[index % 10] += 1

        for i in range(1, 10):
            count[i] += count[i - 1]

        for i in range(n - 1, -1, -1):
            index = arr[i] // exp1
            output[count[index % 10] - 1] = arr[i]
            count[index % 10] -= 1

        for i in range(0, len(arr)):
            arr[i] = output[i]

            draw(liczby)
            pygame.display.update()
            sleep(DELAY)

    max1 = max(liczby)
    exp = 1

    while max1 / exp >= 1:
        countingSort(liczby, exp)
        exp *= 10


def draw(liczby):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    WIN.fill(GRAY)
    for index, liczba in enumerate(liczby):
        x = BLOK_X * index
        y = HEIGHT - (BLOK_Y * liczba)
        pygame.draw.rect(WIN, WHITE, (x, y, BLOK_X, BLOK_Y * liczba))
        # moveX = round(BLOK_X, 0) // 2
        # pygame.draw.line(WIN, WHITE, (BLOK_X * index + moveX, HEIGHT), (BLOK_X * index + moveX, HEIGHT - (BLOK_Y * liczba)), int(round(BLOK_X, 0)))


def main():
    wybor = var.get()
    
    match wybor:
        case "bubble":
            szybszy_bubble_sort()
        case "insertion":
            insertion_sort()
        case "selection":
            selection_sort()
        case "bogo":
            bogo_sort()
        case "shaker":
            shaker_sort()
        case "quick":
            quick_sort(liczby, 0, ILOSC_LICZB - 1)
        case "comb":
            comb_sort()
        case "radix":
            radix_sort()
        case _:
            pygame.quit()
    
    draw(liczby)
    pygame.display.update()
    
    while True:
        event = pygame.event.wait()
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
            break


if ILOSC_LICZB != 0:
    WIN = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("SORTOWANIE")
    WIDTH, HEIGHT = WIN.get_size()

    DELAY = delayVar.get()

    liczby = [i + 1 for i in range(ILOSC_LICZB)]
    shuffle(liczby)

    MAX_WARTOSC = max(liczby)
    BLOK_X = WIDTH / ILOSC_LICZB
    BLOK_Y = HEIGHT / MAX_WARTOSC

    if __name__ == "__main__":
        main()
