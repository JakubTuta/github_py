import socket

mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = 2137

mySocket.connect(("127.0.0.1", port))

while True:
    data = mySocket.recv(1024).decode()
    print(data)

mySocket.close()
