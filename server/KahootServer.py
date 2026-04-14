"""
This is going to be the Kahoot Server file! 
Below is the simple server implementation
"""

from socket import * 
from _thread import *

def kahootThread(connectSocket):
    print('Starting the thread for a kahoot user')
    clientRequest=connectSocket.recv(1024).decode()
    print(clientRequest)

    requestCommand = clientRequest.split(' ')[0]].strip()
    if(requestCommand == 'PlayGame'):
        userName = clientRequest.split(' ')[1].strip()
        welcomeMessage = 'Welcome ' + userName + '!\n'
        connectSocket.send(welcomeMessage.encode())

def serverMain():
    serverPort = 12345
    # Create a welcome TCP socket 
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(("", serverPort))
    serverSocket.listen(1)
    print("Kahoot game is ready!")

    while True:
        # Create the connection socket when sensing new connection request 
        connectSocket,addr = serverSocket.accept()
        start_new_thread(kahootThread, (connectSocket,))

serverMain()
