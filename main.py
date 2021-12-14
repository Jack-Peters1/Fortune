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

# set up connection with server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

# initialize main window
window = Tk()
window['background'] = '#FFE3D7'
window.title("Fortune Client")
text_area = scrolledtext.ScrolledText(window, wrap=WORD, width=95, height=20, font=("Consolas", 15), bg="#FECEB9")

window.iconbitmap("fortunecookie.ico")

image1 = Image.open("logofortune.png")
test = ImageTk.PhotoImage(image1)
# create logo
label1 = Label(image=test)
label1.image = test
label1['background'] = '#FFE3D7'
label1.place(x=0, y=0)

# create text area and entry area
text_area.grid(row=2, column=0, columnspan=14, pady=69, padx=10)
text_area.configure(state='disabled')

e = Entry(window, width=75, borderwidth=5, font=('Consolas', 12))
e.grid(row=4, column=0, columnspan=3, padx=10, pady=10)
# create background for inputs on top
canvas = Canvas(
    window,
    height=65,
    width=550,
    bg='#FECEB9',
)

canvas.place(x=565, y=0)
# create name entry area
e2 = Entry(window, width=20, borderwidth=5, font=('Consolas', 12))
e2.place(x=915, y=20)
e2.insert(END, "Anonymous")
# create name area
name_text = Label(text="Name:", font=('Consolas', 14))
name_text['background'] = '#FECEB9'
name_text.place(x=861, y=23)
# create target entry
e3 = Entry(window, width=20, borderwidth=5, font=('Consolas', 12))
e3.place(x=650, y=20)
e3.insert(END, "")
# create background of text box
target_text = Label(text="Target:", font=('Consolas', 14))
target_text['background'] = '#FECEB9'
target_text.place(x=570, y=23)

# creating text tags
text_area.tag_config('greentext', foreground='#77A44F')
text_area.tag_config('redtext', foreground="#962121")


# function to disconnect from server
def button_disconnect():
    send(DISCONNECT_MESSAGE)
    sys.exit()


def update_thread():
    thread = threading.Thread(target=update)
    thread.start()


# update the clients text area with other clients messages from server
def update():
    while True:
        newLine = str(client.recv(2048).decode(FORMAT))  # get message from server

        a, b = newLine.split(': ', 1)
        a = a + ": "
        b = b + "\n"
        text_area.configure(state='normal')
        text_area.insert(END, a, "redtext")
        text_area.configure(state='disabled')

        if str(newLine[newLine.find(": ") + 2]) == ">":
            text_area.configure(state='normal')
            text_area.insert(END, b, "greentext")
            text_area.configure(state='disabled')
            text_area.yview_moveto(1)
        else:
            text_area.configure(state='normal')
            text_area.insert(END, b, "redtext")
            text_area.configure(state='disabled')
            text_area.yview_moveto(1)


def button_enter():  # send message to server
    # get date and time for message logs
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    if len(e.get()) > 0:
        send(e2.get() + " " + current_time + ": " + e.get())  # call send method with name, time , and message
        text_area.yview_moveto(1)
        e.delete(0, END)


def send(msg):  # main send method
    message = msg.encode(FORMAT)  # encode the message into string for the server
    msg_length = len(message)  # get length of essage to send
    send_length = str(msg_length).encode(FORMAT)  # convert length
    send_length += b' ' * (HEADER - len(send_length))
    if len(str(e3.get())) > 0:  # get the target IP if doing a private message
        target = str(e3.get()).encode(FORMAT)
    else:
        target = "null".encode(FORMAT)
    target += b' ' * (HEADER - len(send_length))
    client.send(target)  # send target and message length first, then send everything else
    client.send(send_length)
    client.send(message)


# create buttons
button_enter = Button(window, text="Enter", padx=91, pady=20, command=button_enter, font=('Consolas', 14))
button_disconnect = Button(window, text="Disconnect", padx=79, pady=20, command=button_disconnect, font=('Consolas', 14))


def disable_event():
    pass


window.protocol("WM_DELETE_WINDOW", disable_event)  # make it so you cant press X button to close window, causing crash

# Put the buttons on the screen
button_disconnect.grid(row=4, column=12, columnspan=2)
button_enter.grid(row=4, column=10, columnspan=2)

update_thread()
window.mainloop()
