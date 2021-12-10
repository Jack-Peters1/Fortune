from tkinter import *
from tkinter import scrolledtext
from PIL import ImageTk, Image
import socket
import threading
import sys

#network initialize


HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "fortunechat.ddns.net"
ADDR = (SERVER, PORT)


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect(ADDR)

windowText = """"""

window = Tk()
window.title("Fortune Client")
text_area = scrolledtext.ScrolledText(window, wrap=WORD, width=95, height=10, font=("Times New Roman", 15))

image1 = Image.open("logofortune.jpg")
test = ImageTk.PhotoImage(image1)

label1 = Label(image=test)
label1.image = test

label1.place(x=0, y=0)


text_area.grid(column=0, columnspan=14, pady=65, padx=10)
text_area.configure(state='disabled')

e = Entry(window, width=35, borderwidth=5)
e.grid(row=4, column=0, columnspan=3, padx=10, pady=10)

e2 = Entry(window, width=20, borderwidth=5)
e2.place(x=600, y=0)
e2.insert(END, "Anonymous")


def button_click(number):
    current = e.get()
    e.delete(0, END)
    e.insert(0, str(current) + str(number))


def button_disconnect():
    send(DISCONNECT_MESSAGE)
    sys.exit()


def update_thread():
    thread = threading.Thread(target=update)
    thread.start()

def button_username():
    #nothing is actually needed here
    pass


def update():
    while True:
        global windowText
        windowText = "" + windowText + "\n" + str(client.recv(2048).decode(FORMAT))
        text_area.configure(state='normal')
        text_area.delete("1.0", "end")
        text_area.insert(END, windowText)
        text_area.configure(state='disabled')
        text_area.yview_moveto(1)


def button_enter():
    send(e2.get() + ": " + e.get())
    text_area.yview_moveto(1)
    e.delete(0, END)


def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)


button_enter = Button(window, text="Enter", padx=91, pady=20, command=button_enter)
button_disconnect = Button(window, text="Disconnect", padx=79, pady=20, command=button_disconnect)
button_username = Button(window, activebackground="#FFFFFF", bg="#FFFFFF", text="Input Name:", padx=10, pady=6, command=button_username)

# Put the buttons on the screen
button_disconnect.grid(row=4, column=7, columnspan=2)
button_enter.grid(row=4, column=5, columnspan=2)
button_username.place(x=500, y=1)

update_thread()
window.mainloop()

