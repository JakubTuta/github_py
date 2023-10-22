from tkinter import *
from tkinter import filedialog

from PIL import Image, ImageTk
from TkinterDnD2 import DND_FILES, TkinterDnD

filepath = ""


def resize_and_save_image(width, height):
    try:
        width = int(width)
        height = int(height)
    except:
        return
    else:
        if width <= 0 or height <= 0:
            return

    global filepath
    if not filepath.endswith(".png") and not filepath.endswith(".jpg"):
        return

    help_filepath = filepath.split("/")
    name = help_filepath[-1]
    path = "/".join(help_filepath[0:-1])

    image = Image.open(filepath)
    image = image.resize((width, height))
    image = image.save(f"{path}/resized_{name}")

    Label(text="Image saved", font=smaller_font).grid(row=8, column=1)


def open_smaller_image():
    if not filepath.endswith(".png") and not filepath.endswith(".jpg"):
        return

    help_image = Image.open(filepath)
    width, height = help_image.size

    Label(text=f"{width}x{height}", font=smaller_font).grid(row=6, column=1)

    while width > 200 and height > 200:
        width *= 0.9
        height *= 0.9

    width, height = int(width), int(height)

    help_image = help_image.resize((width, height))
    image_to_show = ImageTk.PhotoImage(help_image)
    lab = Label(image=image_to_show)
    lab.grid(row=7, column=0, columnspan=3, padx=10, pady=10)
    lab.image = image_to_show


def drag_and_drop(event):
    global filepath
    filepath = event.data[1:-1]
    open_smaller_image()


def open_file_dialog():
    global filepath
    filepath = filedialog.askopenfilename(
        title="Select a file",
        filetypes=((".png, .jpg", ("*.png", "*.jpg")), ("all files", "*.*")),
    )
    open_smaller_image()


root = TkinterDnD.Tk()
root.title("Resize image")
root.resizable(False, False)
root.attributes("-topmost", True)

title_font = ("Arial", 20, "bold")
main_font = ("Arial", 15)
smaller_font = ("Arial", 10, "italic")

Label(text="Paste an image and resize it", font=title_font).grid(
    row=0, column=0, columnspan=3, padx=10, pady=10
)

Label(text="Drop an image", font=main_font).grid(
    row=1, column=0, padx=10, pady=10, sticky=W
)
box = Label(text="Drop here", font=smaller_font, background="#CCCCCC")
box.grid(row=2, column=0, padx=10, pady=10, ipadx=60, ipady=20)
box.drop_target_register(DND_FILES)
box.dnd_bind("<<Drop>>", drag_and_drop)
Label(text="Upload an image", font=main_font).grid(
    row=3, column=0, padx=10, pady=10, sticky=W
)
Button(text="Open a file", font=main_font, command=open_file_dialog).grid(
    row=4, column=0, padx=10, pady=10, ipadx=10, ipady=5
)

Label(text="Width:", font=main_font).grid(row=1, column=2, padx=10, pady=10, sticky=W)
WidthEntry = Entry(root, font=main_font)
WidthEntry.grid(row=2, column=2, padx=10, pady=10, ipadx=10, ipady=5, sticky=W)
Label(text="Height:", font=main_font).grid(row=3, column=2, padx=10, pady=10, sticky=W)
HeightEntry = Entry(root, font=main_font)
HeightEntry.grid(row=4, column=2, padx=10, pady=10, ipadx=10, ipady=5, sticky=W)

Button(
    text="Ready",
    font=title_font,
    command=lambda: resize_and_save_image(WidthEntry.get(), HeightEntry.get()),
).grid(row=5, column=1, padx=10, pady=10, ipadx=30, ipady=10)

root.mainloop()
