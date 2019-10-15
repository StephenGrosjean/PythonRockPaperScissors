# coding: utf-8
import socket

HOST = '127.0.0.1'
PORT = 27003
SENTENCE_SIZE = 3
PLAYER1 = socket
PLAYER2 = socket
Players = 0

player1_Choice = ""
player2_Choice = ""

def DisconnectAll():
    Send("Disconnect", PLAYER1)
    Send("Disconnect", PLAYER2)

def Send(message, socket):
    if message != "Disconnect":
        try:
            socket.send(bytes(message, "utf-8"))
        except:
            print("ERROR, maybe the connection was lost")
            DisconnectAll()
            exit()

def SendResult(status, p1, p2, socket):
    Send(f"--------------------------------", socket)
    Send(f"     {p1} VS {p2}     ", socket)
    Send(f"          {status}       ", socket)
    Send(f"--------------------------------", socket)


def DefineChoice(choice):
    if choice == "Rock" or choice == "rock":
        return "R"

    if choice == "Paper" or choice == "paper":
        return "P"

    if choice == "Scissors" or choice == "scissors":
        return "S"


def Compute(p1, p2):
    # Case player 1 Rock
    if p1 == "R" and p2 == "P":
        return 2

    if p1 == "R" and p2 == "S":
        return 1

    if p1 == "R" and p2 == "R":
        return 0

    # Case player 1 Paper
    if p1 == "P" and p2 == "P":
        return 0

    if p1 == "P" and p2 == "S":
        return 2

    if p1 == "P" and p2 == "R":
        return 1

    # Case player 1 Scissors
    if p1 == "S" and p2 == "P":
        return 1

    if p1 == "S" and p2 == "S":
        return 0

    if p1 == "S" and p2 == "R":
        return 2


while True:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(5)
    conn, addr = s.accept()

    print(f"{addr} is Connected")

    if Players == 0:
        PLAYER1 = conn
        Send("Hello Player 1", PLAYER1)
        Players += 1
    else:
        PLAYER2 = conn
        Send("Hello Player 2", PLAYER2)
        Players += 1

    print(f"{Players} Players")

    if Players == 2:
        # Set GameState to 1
        Send("GS", PLAYER1)
        Send("GS", PLAYER2)

        # Ask input player 1
        Send("Give me your choice : ", PLAYER1)

        # Wait for reception
        reception = PLAYER1.recv(1024)

        # Print reception
        player1_Choice = reception.decode()
        print(f"Player 1 has chosen {reception.decode()}")

        # ## Same thing for player 2 ## #

        # Ask input player 2
        Send("Give me your choice : ", PLAYER2)

        # Wait for reception
        reception = PLAYER2.recv(1024)

        # Print reception
        player2_Choice = reception.decode()
        print(f"Player 2 has chosen {reception.decode()}")

        player1_Choice_Def = DefineChoice(player1_Choice)
        player2_Choice_Def = DefineChoice(player2_Choice)

        matchResult = Compute(player1_Choice_Def, player2_Choice_Def)

        print(f"Result {matchResult}")

        Send("GR", PLAYER1)
        Send("GR", PLAYER2)

        if matchResult == 0:
            SendResult("TIE", player1_Choice, player2_Choice, PLAYER1)
            SendResult("TIE", player2_Choice, player1_Choice, PLAYER2)

        if matchResult == 1:
            SendResult("WINNER", player1_Choice, player2_Choice, PLAYER1)
            SendResult("LOOSER", player2_Choice, player1_Choice, PLAYER2)

        if matchResult == 2:
            SendResult("LOOSER", player1_Choice, player2_Choice, PLAYER1)
            SendResult("WINNER", player2_Choice, player1_Choice, PLAYER2)

        break







