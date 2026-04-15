"""
This is going to be the Kahoot Server file! 
Below is the simple server implementation
"""

from socket import *
from _thread import *
import time

clients = []
usernames = {}
scores = {}

questions = [
    ("What is the capital of France?", ["A) London", "B) Berlin", "C) Paris", "D) Madrid"], "C"),
    ("What is 2 + 2?", ["A) 3", "B) 4", "C) 5", "D) 6"], "B")
]

def kahootThread(connectSocket):
    print('New client connected')

    try:
        clientRequest = connectSocket.recv(1024).decode().strip()
        print(clientRequest)

        parts = clientRequest.split(" ")
        command = parts[0]

        if command == 'PlayGame':
            userName = parts[1]

            clients.append(connectSocket)
            usernames[connectSocket] = userName
            scores[userName] = 0

            welcomeMessage = 'WELCOME ' + userName + '\n'
            connectSocket.send(welcomeMessage.encode())

            print(userName + " joined the game.")

    except:
        connectSocket.close()


def broadcast(message):
    for c in clients:
        try:
            c.send(message.encode())
        except:
            c.close()


def runGame():
    time.sleep(5)  # wait for players to join

    for i, (question, options, correct) in enumerate(questions, start=1):
        msg = f"QUESTION {i}\n{question}\n"
        for opt in options:
            msg += opt + "\n"

        broadcast(msg)

        answers = {}

        start = time.time()

        # collect answers for 10 seconds
        while time.time() - start < 10:
            for c in clients:
                try:
                    c.settimeout(0.1)
                    data = c.recv(1024).decode().strip()

                    if data.startswith("ANSWER"):
                        _, choice = data.split()
                        answers[c] = (choice, time.time() - start)

                except:
                    pass

        # scoring
        for c, (choice, t) in answers.items():
            if choice == correct:
                username = usernames[c]
                points = max(0, int(10 - t))
                scores[username] += points

        # send scores
        scoreMsg = "SCORES\n"
        for u, s in scores.items():
            scoreMsg += f"{u} {s}\n"
        scoreMsg += "END\n"

        broadcast(scoreMsg)

    # game over
    final = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    msg = "GAME_OVER\n"
    for i, (u, s) in enumerate(final, start=1):
        msg += f"{i} {u} {s}\n"

    broadcast(msg)


def serverMain():
    serverPort = 12345
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(("", serverPort))
    serverSocket.listen(5)

    print("Kahoot game is ready!")

    start_new_thread(runGame, ())

    while True:
        connectSocket, addr = serverSocket.accept()
        start_new_thread(kahootThread, (connectSocket,))


serverMain()
