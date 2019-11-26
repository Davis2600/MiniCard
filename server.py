import socket
import sys
from _thread import *
from card import Card
from player import Player
from state import GameState
#creating a default socket 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('we did it boys')

#default port
port, server = 1234, 'localhost'
serverIP = socket.gethostbyname(server)
try:
    s.bind((server, port))   
    print(f'socket bound to port {port}')
except socket.error as e:
    print(str(e))


s.listen(5)
print('we are listening')
currId = '0'

#init the shared game state
player0 = Player()
player1 = Player()

#TODO for now the decks will be set, customizable decks soon
player0.makeBasicDeck()
player1.makeBasicDeck()

def threadedClient(c):
    global currId, player0, player1
    if currId == '0':
        currState = GameState(player0,player1)
    else:
        currState = GameState(player1,player0)
    c.send(str.encode(currId,',',str(currState)))
    if currId == '1':
        c.close()
    else:
        currId = '1'
    reply = ''
    running = True
    while running:
        try:
            data = c.recv(4096)
            reply = data.decode('utf-8')
            if not data: #nothing was recieved or something broke
                c.send(str.encode("Ended"))
                running = False
                break
            else:
                print('Recieved ', reply)
                contents = reply.split(',')
                playerNum = contents[0] #gets the ID
                activeP = contents[1] #gets that clients player 1
                passiveP = contents[2] #gets that clients player 2

                #build the state from the strings
                
                if index == 0:
                    newIndex = 1
                else:
                    newIndex = 0

                sendBack = f'changed value {index} to {newVal} '
                print(sendBack)
                sendBack = sendBack + str(values)
            
            c.sendall(str.encode(sendBack))
            print('sent reply')
        except socket.error as e:
            print(e)
            break 


    print('connection finishied')
    c.close()


while True:
    c, addr = s.accept()
    print(f'Got Connection from {addr}')
    start_new_thread(threadedClient, (c,))