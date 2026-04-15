"""
This is going to be the client file 
Below is the simple client implementation 
"""

from socket import *
from threading import Thread

def receiveMessages(clientSocket):
    while True:
        try:
            msg = clientSocket.recv(1024).decode()
            print(msg)

            # handle timer
            if msg.startswith("TIMER"):
                _, t = msg.split()
                print(f"⏳ Time left: {t}s")

            # handle question
            if msg.startswith("QUESTION"):
                answer = input("Enter answer (A/B/C/D): ")
                clientSocket.send(f"ANSWER {answer.upper()}\n".encode())

        except:
            print("Disconnected.")
            clientSocket.close()
            break


def ClientMain():
    serverIP = '127.0.0.1'
    serverPort = 12345

    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverIP, serverPort))

    userName = input("What is your username? ")
    playGameMessage = "PlayGame " + userName + "\n"
    clientSocket.send(playGameMessage.encode())

    Thread(target=receiveMessages, args=(clientSocket,)).start()


ClientMain()
