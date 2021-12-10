import socket
import threading

port = 5050
hostip = "192.168.19.166"
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

address = (hostip, port)
server.bind(address)


def client(conn, addr):
    message = conn.recv()
    pass

def start():
    server.listen()
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=client, args=(conn, addr))
        thread.start()