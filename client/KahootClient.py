"""
This is going to be the client file 
Below is the simple client implementation 
"""

from socket import *

def ClientMain():
    serverIP = '127.0.0.1' #Will need to change to public IP eventually 
    serverPort = 12345 
    while True:
        clientSocket = socket(AF_INET, SOCK_STREAM)
        clientSocket.connect((serverIP, serverPort))

        userName = input("What is your username?")
        playGameMessage = "PlayGame " + userName + "\n"
        clientSocket.send(playGameMessage.encode())

ClientMain()
