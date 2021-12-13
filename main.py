from tkinter import *
from tkinter import scrolledtext
from PIL import ImageTk, Image
import socket
import threading
import sys
from datetime import datetime

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "fortunechat.ddns.net"
ADDR = (SERVER, PORT)


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#client.connect(ADDR)

windowText = """"""

window = Tk()
window['background']='#E0FFE9'
window.title("Fortune Client")
text_area = scrolledtext.ScrolledText(window, wrap=WORD, width=95, height=20, font=("Consolas", 15), bg="#A2F3BB")

image1 = Image.open("logofortune.png")
test = ImageTk.PhotoImage(image1)

label1 = Label(image=test)
label1.image = test
label1['background']='#E0FFE9'
label1.place(x=0, y=0)



text_area.grid(row=2, column=0, columnspan=14, pady=69, padx=10)
text_area.configure(state='disabled')

e = Entry(window, width=75, borderwidth=5, font=('Consolas', 12))
e.grid(row=4, column=0, columnspan=3, padx=10, pady=10)

canvas = Canvas(
    window,
    height=67,
    width=550,
    bg='#a0a0a0'
)

canvas.place(x=565, y=0)

e2 = Entry(window, width=20, borderwidth=5, font=('Consolas', 12))
e2.place(x=915, y=20)
e2.insert(END, "Anonymous")

name_text = Label(text="Name:", font=('Consolas', 14))
name_text['background']='#a0a0a0'
name_text.place(x=861, y=23)

e3 = Entry(window, width=20, borderwidth=5, font=('Consolas', 12))
e3.place(x=650, y=20)
e3.insert(END, "")

target_text = Label(text="Target:", font=('Consolas', 14))
target_text['background']='#a0a0a0'
target_text.place(x=570, y=23)


def button_disconnect():
    send(DISCONNECT_MESSAGE)
    sys.exit()


def update_thread():
    thread = threading.Thread(target=update)
    thread.start()


def update():
    while True:
        global windowText
        windowText = "" + windowText + "\n" + str(client.recv(2048).decode(FORMAT))
        text_area.configure(state='normal')
        text_area.delete("1.0", "end")
        text_area.insert(END, windowText)
        text_area.configure(state='disabled')
        text_area.yview_moveto(1)

now = datetime.now()
current_time = now.strftime("%H:%M:%S")

def button_enter():
    if len(e.get()) > 0:
        send(e2.get() + " " + current_time + ": " + e.get())
        text_area.yview_moveto(1)
        e.delete(0, END)

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)


button_enter = Button(window, text="Enter", padx=91, pady=20, command=button_enter, font=('Consolas', 14))
button_disconnect = Button(window, text="Disconnect", padx=79, pady=20, command=button_disconnect, font=('Consolas', 14))

def disable_event():
   pass
window.protocol("WM_DELETE_WINDOW", disable_event)

# Put the buttons on the screen
button_disconnect.grid(row=4, column=12, columnspan=2)
button_enter.grid(row=4, column=10, columnspan=2)

update_thread()
window.mainloop()

