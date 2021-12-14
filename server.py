import socket
import threading

HEADER = 64
PORT = 5050
#SERVER = ""
SERVER = "10.1.136.87"
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create Socket server
server.bind(ADDR)  # Bind server to the target address

clients = set()  # List of all clients. Part of PMs and also part of broadcasting to all clients.
clients_lock = threading.Lock()  # Useful for making all threads accessible from all threads so that the all clients can be send broadcasts


def handle_client(conn, addr):
    print("New connection. " + str(addr) + " connected.")
    with clients_lock:
        clients.add(conn)  # Add the new client to the list

    with clients_lock:
        for client in clients:
            client.sendall(("A new client has connected. Active connections: " + str(threading.active_count() - 1)).encode(FORMAT))  # Broadcast to all clients when a new user has connected

    connected = True
    while connected:  # While each connection is established...
        target = conn.recv(HEADER).decode(FORMAT)  # Begin searching for messages. The first message, target, is for the IP that the server will try to PM.
                                                   # If this IP is null, it will instead broadcast the message to all clients. IPs should be the Default Gateway
                                                   # On Windows, your default gateway can be found by running ipconfig in terminal.
        print(target)
        msg_length = conn.recv(HEADER).decode(FORMAT)  # The second message will always be the length of the third comment so that the server always knows how much data to request from the client
        if msg_length:  # If the message is not empty, continue
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)  # Decode the incoming message which was sent in UTF-8 format
            print(str(addr) + " " + str(msg))

            with clients_lock:  # For all of the clients in all threads...
                for client in clients:
                    if msg != DISCONNECT_MESSAGE:  # If the client is not trying to disconnect...
                        if target == "null":  # If there is no specific target for the message, broadcast to all clients.
                            client.sendall(msg.encode(FORMAT))
                        elif client.getpeername()[0] == addr[0]:  # Otherwise, Send the PM back to the sender so that it shows up in the chatbox.
                            client.send(str(msg + " [PRIVATE MESSAGE]").encode(FORMAT))
                        if client.getpeername()[0] == target:  # And also Send the PM to the target and only to the target.
                            print("Client to PM Found")
                            client.send(str(msg + " [PRIVATE MESSAGE]").encode(FORMAT))
                    else:  # If the client is trying to disconnect and the disconnect message has been recieved by the server, notify all clients still connected that a disconnect has occurred.
                        client.sendall(("A user has disconnected. Active connections: " + str(threading.active_count() - 2)).encode(FORMAT))

            if msg == DISCONNECT_MESSAGE:
                connected = False  # Stop the loop
                with clients_lock:  # Remove the clients from the client list
                    clients.remove(conn)

    conn.close()  # close the connection to the client


def start():
    server.listen()  # Make the server start listening
    print("Server is listening")
    while True:  # While the server is active...
        conn, addr = server.accept()  # wait to accept new connections. The code will only move on when a connection is made
        thread = threading.Thread(target=handle_client, args=(conn, addr))  # A new thread is created to handle the new connection with the hendle_client method
        thread.start()  # Start the new thread
        print("Active connections: " + str(threading.active_count() - 1))


print("Server is starting...")
start()
