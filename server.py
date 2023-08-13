import socket
import threading


def acceptClients():
    while True:
        connection, clientIP = mySocket.accept()
        print(f"\nConnection from: {clientIP}")
        connectedClients.append(connection)


def sendData():
    while True:
        data = input("Dawaj dane: ")
        for client in connectedClients:
            client.send(data.encode())


t_acceptClients = threading.Thread(target=acceptClients)
t_sendDataToClients = threading.Thread(target=sendData)

mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
hostName = socket.gethostname()
hostIP = socket.gethostbyname(hostName)
port = 2137

mySocket.bind(("127.0.0.1", port))
mySocket.listen(5)

connectedClients = []

t_acceptClients.start()
t_sendDataToClients.start()
