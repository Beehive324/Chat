# clients will connect to each other
# server broadcasts the messages
# run each separate function on different threads, to improve efficiency


import socket
import threading

Host = '127.0.0.1'
PORT = 9090

h_p = (Host, PORT)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(h_p)
server.listen()
clients = []  # array of clients
usernames = []  # array of nicknames


# broadcast function, function to send message to all connected clients


def broadcast(message):  # show message
    for client in clients:
        client.send(message)


# receive function, accept new connections, new clients connecting

def handle(client):  # handles messages and removes clients
    while True:
        try:
            message = client.recv(1024)
            print(f"{usernames[clients.index(client)]} says {message}")
            broadcast(message)
        except:  # remove client
            index = clients.index(client)
            clients.remove(client)
            client.close()
            username = usernames[index]
            usernames.remove(username)
            break


def receive():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}! ")

        client.send("ABA".encode('utf-8'))
        username = client.recv(1024)
        usernames.append(username)
        clients.append(client)
        broadcast(f"{username} is now connected".encode('utf-8'))
        client.send("Connected to the server".encode('utf-8'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


print("Server running..")
receive()
