from tkinter import *           # pip install tkinter
import pygame                   # pip install pygame    /   pip install pygame --pre
from random import shuffle
from time import sleep
import pyautogui                # pip install pyautogui

SETTINGS = {}
COLORS = {
    "WHITE": (255, 255, 255),
    "GREEN": (0, 255, 0),
    "GRAY": (100, 100, 100)
}
WIDTH, HEIGHT = pyautogui.size()


def settings():
    def zamknij(algorythm, iloscLiczb, delay):
        try:
            iloscLiczb = int(iloscLiczb)
        except:
            return
        
        if iloscLiczb < 1 or iloscLiczb > 512:
            return
        
        SETTINGS["algorythm"] = algorythm
        SETTINGS["iloscLiczb"] = iloscLiczb
        SETTINGS["delay"] = delay

        top.destroy()

    top = Tk()
    top.title("Ilość liczb")
    top.resizable(False, False)

    Label(top, text="Podaj ilość liczb:", font=("Times New Roman", 20)).grid(row=0, column=0, padx=20, pady=10)
    Label(top, text="(1 - 512)", font=("Times New Roman", 15, "italic")).grid(row=1, column=0, padx=10, pady=10)
    Label(top, text="Wybierz rodzaj sortowania:", font=("Times New Roman", 20)).grid(row=0, column=1, padx=20, pady=10)

    sortingAlgorythm = StringVar(value="bubble")
    Radiobutton(top, text="Sortowanie bąbelkowe", variable=sortingAlgorythm, value="bubble", font=("Times New Roman", 15)).grid(row=1, column=1, padx=10, pady=10, sticky=W)
    Radiobutton(top, text="Sortowanie przez wstawianie", variable=sortingAlgorythm, value="insertion", font=("Times New Roman", 15)).grid(row=2, column=1, padx=10, pady=10, sticky=W)
    Radiobutton(top, text="Sortowanie przez wybieranie", variable=sortingAlgorythm, value="selection", font=("Times New Roman", 15)).grid(row=3, column=1, padx=10, pady=10, sticky=W)
    Radiobutton(top, text="Bogo sort", variable=sortingAlgorythm, value="bogo", font=("Times New Roman", 15)).grid(row=4, column=1, padx=10, pady=10, sticky=W)
    Radiobutton(top, text="Cocktail shaker sort", variable=sortingAlgorythm, value="shaker", font=("Times New Roman", 15)).grid(row=5, column=1, padx=10, pady=10, sticky=W)
    Radiobutton(top, text="Quicksort", variable=sortingAlgorythm, value="quick", font=("Times New Roman", 15)).grid(row=6, column=1, padx=10, pady=10, sticky=W)
    Radiobutton(top, text="Sortowanie grzebieniowe (comb sort)", variable=sortingAlgorythm, value="comb", font=("Times New Roman", 15)).grid(row=7, column=1, padx=10, pady=10, sticky=W)
    Radiobutton(top, text="Sortowanie pozycyjne (radix sort)", variable=sortingAlgorythm, value="radix", font=("Times New Roman", 15)).grid(row=8, column=1, padx=10, pady=10, sticky=W)

    iloscLiczb = Entry(top, font=("Times New Roman", 15))
    iloscLiczb.grid(row=2, column=0, padx=10, pady=10, ipadx=10)

    Label(top, text="Wybierz prędkość sortowania (niższa liczba - szybsze sortowanie):", font=("Times New Roman", 15)).grid(row=9, column=0, columnspan=2, padx=10, pady=20)

    delayVar = DoubleVar(value=0.005)
    delayScale = Scale(top, from_=0.005, to=1.0, digits=4, resolution=0.005, orient=HORIZONTAL, variable=delayVar)
    delayScale.grid(row=10, column=0, columnspan=2, padx=10, pady=10, ipadx=100)

    Button(top, text="Pokaż!", font=("Times New Roman", 15), command=lambda: zamknij(sortingAlgorythm.get(), iloscLiczb.get(), delayScale.get())).grid(row=11, column=0, columnspan=2, padx=10, pady=10, ipadx=30)

    top.mainloop()


def quick_sort(WIN, clock, liczby):
    def quick_sort_rec(liczby, low, high):
        def partition(liczby, low, high):
            pivot = liczby[high]
            i = low - 1
            for j in range(low, high):
                if liczby[j] <= pivot:
                    i = i + 1
                    liczby[i], liczby[j] = liczby[j], liczby[i]
            liczby[i + 1], liczby[high] = liczby[high], liczby[i + 1]
            return i + 1
        
        try:
            liczby[low]
        except IndexError:
            draw(WIN, liczby, [liczby[high]])
        else:
            draw(WIN, liczby, [liczby[low], liczby[high]])
        clock.tick(SETTINGS["FPS"])

        if low < high:
            pi = partition(liczby, low, high)
            quick_sort_rec(liczby, low, pi - 1)
            quick_sort_rec(liczby, pi + 1, high)
    quick_sort_rec(liczby, 0, len(liczby) - 1)


def szybszy_bubble_sort(WIN, clock, liczby):
    for i in range(len(liczby) - 1):
        swapped = False
        for j in range(len(liczby) - i - 1):
            if liczby[j] > liczby[j+1]:
                draw(WIN, liczby, [liczby[j], liczby[j+1]])
                clock.tick(SETTINGS["FPS"])
                
                swapped = True
                liczby[j], liczby[j+1] = liczby[j+1], liczby[j]

        if not swapped:
            break


def insertion_sort(WIN, clock, liczby):
    for i in range(1, len(liczby)):
        pom = liczby[i]
        j = i - 1
        while j >= 0 and liczby[j] > pom:
            liczby[j + 1] = liczby[j]
            j -= 1
            
            draw(WIN, liczby, [liczby[j]])
            clock.tick(SETTINGS["FPS"])
            
        liczby[j + 1] = pom


def selection_sort(WIN, clock, liczby):
    for i in range(0, len(liczby)):
        minimum = min(liczby[i:len(liczby)])
        index = liczby.index(minimum)
        
        draw(WIN, liczby, [liczby[index]])
        clock.tick(SETTINGS["FPS"])
        
        liczby[i], liczby[index] = liczby[index], liczby[i]


def bogo_sort(WIN, clock, liczby):
    def is_sorted(lista):
        return liczby == sorted(lista)

    while not is_sorted(liczby):
        shuffle(liczby)
        draw(WIN, liczby)
        clock.tick(SETTINGS["FPS"])


def shaker_sort(WIN, clock, liczby):
    start = 0
    end = len(liczby) - 1
    
    epilepsja = True
    swap = True
    while swap:
        swap = False

        draw(WIN, liczby)
        clock.tick(SETTINGS["FPS"])

        for a in range(start, end):
            if liczby[a] > liczby[a+1]:
                liczby[a], liczby[a+1] = liczby[a+1], liczby[a]
                swap = True

        if not swap:
            end -= 1
        
        if epilepsja:
            draw(WIN, liczby)
            clock.tick(SETTINGS["FPS"])

        for a in range(end - 1, start - 1, -1):
            if liczby[a] > liczby[a+1]:
                liczby[a], liczby[a+1] = liczby[a+1], liczby[a]
                swap = True

        start += 1


def comb_sort(WIN, clock, liczby):
    gap = len(liczby)
    shrink = 1.3
    
    sorted = False
    while not sorted:
        gap = int(gap / shrink)
        if gap < 1:
            gap = 1
            sorted = True
        
        i = 0
        while i + gap < len(liczby):
            if liczby[i] > liczby[i + gap]:
                liczby[i], liczby[i + gap] = liczby[i + gap], liczby[i]
                sorted = False
            i += 1
            
            draw(WIN, liczby)
            clock.tick(SETTINGS["FPS"])


def radix_sort(WIN, clock, liczby):
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

            draw(WIN, liczby)
            clock.tick(SETTINGS["FPS"])

    max1 = max(liczby)
    exp = 1

    while max1 / exp >= 1:
        countingSort(liczby, exp)
        exp *= 10


def draw(WIN, liczby, highlights = []):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    
    blokX = SETTINGS["blokX"]
    blokY = SETTINGS["blokY"]
    WIN.fill(COLORS["GRAY"])
    
    for index, liczba in enumerate(liczby):
        if liczba in highlights:
            color = COLORS["GREEN"]
        else:
            color = COLORS["WHITE"]
        x = blokX * index
        y = HEIGHT - (blokY * liczba)
        pygame.draw.rect(WIN, color, (x, y, blokX, blokY * liczba))
    
    pygame.display.update()


def main():
    
    sortingAlgorythm = SETTINGS["algorythm"]
    iloscLiczb = SETTINGS["iloscLiczb"]
    SETTINGS["FPS"] = 1 / SETTINGS["delay"]
    
    WIN = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("SORTOWANIE")
    clock = pygame.time.Clock()

    liczby = [i + 1 for i in range(iloscLiczb)]
    shuffle(liczby)
    
    SETTINGS["blokX"] = WIDTH / iloscLiczb
    SETTINGS["blokY"] = HEIGHT / max(liczby)
    
    match sortingAlgorythm:
        case "bubble":
            szybszy_bubble_sort(WIN, clock, liczby)
        case "insertion":
            insertion_sort(WIN, clock, liczby)
        case "selection":
            selection_sort(WIN, clock, liczby)
        case "bogo":
            bogo_sort(WIN, clock, liczby)
        case "shaker":
            shaker_sort(WIN, clock, liczby)
        case "quick":
            quick_sort(WIN, clock, liczby)
        case "comb":
            comb_sort(WIN, clock, liczby)
        case "radix":
            radix_sort(WIN, clock, liczby)
        case _:
            pygame.quit()
    
    for i in range(len(liczby)):
        if i == 0:
            draw(WIN, liczby, [liczby[i], liczby[i+1]])
        elif i == len(liczby) - 1:
            draw(WIN, liczby, [liczby[i], liczby[i-1]])
        else:
            draw(WIN, liczby, [liczby[i-1], liczby[i], liczby[i+1]])
    draw(WIN, liczby)
    
    while True:
        event = pygame.event.wait()
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
            break


if __name__ == "__main__":
    settings()
    main()