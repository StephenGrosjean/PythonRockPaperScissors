# coding: utf-8
#!/usr/bin/env python3
import socket

HOST = '127.0.0.1'
PORT = 27003
LOOP_ACTIVE = True

State = 0


def ValidChoices(choice):
    if choice == "Rock" or choice == "Paper" or choice == "Scissors" \
            or choice == "rock" or choice == "paper" or choice == "scissors":
        return True
    else:
        return False


def Send(message, socket):
    socket.send(bytes(message, "utf-8"))

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))

except:
    print("-ERROR- Server is not reachable")
    exit()

while True:

    if State == 0:
        msg = s.recv(1024)

        if msg.decode() == "Disconnect":
            s.close()
            print("The connection was lost")
            exit()

        if msg.decode() == "GS":
            State = 1
        else:
            print(msg.decode())

    if State == 1:
        msg = s.recv(1024)

        if msg.decode() == "Disconnect":
            s.close()
            print("The connection was lost")
            exit()

        if msg.decode() == "GR":
            State = 2
        else:
            print(msg.decode())

        if State == 1:
            choice = input()
            while not ValidChoices(choice):
                print("--Error, Valid choices are : Rock, Paper, Scissors --")
                choice = input()

            Send(choice, s)

    if State == 2:
        line1 = s.recv(1024)
        line2 = s.recv(1024)
        line3 = s.recv(1024)
        line4 = s.recv(1024)

        print(line1.decode())
        print(line2.decode())
        print(line3.decode())
        print(line4.decode())

        break




