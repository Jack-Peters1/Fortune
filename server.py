import socket
import threading

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

clients = set()
clients_lock = threading.Lock()

def handle_client(conn, addr):
    print("New connection. " + str(addr) + " connected.")
    with clients_lock:
        clients.add(conn)

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            print(str(addr) + " " + str(msg))
            with clients_lock:
                for client in clients:
                    client.sendall(msg.encode(FORMAT))

            if msg == DISCONNECT_MESSAGE:
                connected = False
                with clients_lock:
                    clients.remove(conn)

    conn.close()


def start():
    server.listen()
    print("Server is listening on " + SERVER)
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print("Active connections: " + str(threading.active_count() - 1))



print("Server is starting...")
start()
