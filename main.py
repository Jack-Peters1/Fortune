from tkinter import *
from tkinter import scrolledtext

windowText = """"""

window = Tk()
window.title("Text Interface")

# Title Label
Label(window, text="ScrolledText Widget Example", font=("Times New Roman", 15), background='green', foreground="white").grid(column=0,row=0)

# Creating scrolled text
# area widget
text_area = scrolledtext.ScrolledText(window, wrap=WORD, width=40, height=10, font=("Times New Roman", 15))

text_area.grid(column=0, pady=10, padx=10)
text_area.configure(state='disabled')

e = Entry(window, width=35, borderwidth=5)
e.grid(row=4, column=0, columnspan=3, padx=10, pady=10)


def button_click(number):
    current = e.get()
    e.delete(0, END)
    e.insert(0, str(current) + str(number))


def button_clear():
    e.delete(0, END)


def button_enter():
    global windowText
    windowText = "" + windowText + "\n" + e.get()
    text_area.configure(state='normal')
    text_area.delete("1.0", "end")  # if you want to remove the old data
    text_area.insert(END, windowText)
    text_area.configure(state='disabled')
    e.delete(0, END)

button_enter = Button(window, text="Enter", padx=91, pady=20, command=button_enter)
button_clear = Button(window, text="Clear", padx=79, pady=20, command=button_clear)

# Put the buttons on the screen
button_clear.grid(row=4, column=5, columnspan=2)
button_enter.grid(row=4, column=7, columnspan=2)

window.mainloop()
