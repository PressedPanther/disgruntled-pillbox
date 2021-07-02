#TCPClient.py

from socket import socket, AF_INET, SOCK_STREAM

serverName = 'localhost'
#host = socket.gethostname()
serverPort = 25565
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
message = input('Input lowercase sentence: ')
clientSocket.send(message.encode())
modifiedMessage = clientSocket.recv(2048).decode()
print ('From Server: ', modifiedMessage)
clientSocket.close()