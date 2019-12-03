import socket
import sys
from _thread import *
from card import Card
from player import Player
from state import GameState
import random
#creating a default socket 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('we did it boys')

#default port
port, server = 2345, 'localhost'
serverIP = socket.gethostbyname(server)
try:
    s.bind((server, port))   
    print(f'socket bound to port {port}')
except socket.error as e:
    print(str(e))


s.listen(5)
print('we are listening')
currId = '0'

player0 = Player()
player1 = Player()
player0.currentPlayer = False
player1.currentPlayer = False
deck0Str = ''
deck1Str = ''
#init the shared game 
def startGame(player0, player1):
    print('Starting Game')
    coinFlip = random.randint(0,2)
    if coinFlip == 1:
        player1.currentPlayer = True
        player1.firstTurn = False
    else:
        player0.currentPlayer = True
        player0.firstTurn = False


    for i in range(5):
        player0.pickupCard()
        player1.pickupCard()
    
    player0.gameStarted = True
    player1.gameStarted = True

def threadedClient(c):
    global currId, player0, player1
    theID = currId

    
    if currId == '0':
        currState = GameState(player0, player1)
        c.send(str.encode(currId + '|||' + str(currState)))
        currId = '1'
        deck0Str = c.recv(4096).decode()
        print('DECK 0 RECIEVED')
        print('THIS IS THE DECK STRING:', deck0Str)
        player0.buildDeckFromString(deck0Str)
        player0.message = 'waiting for player'
        currState = GameState(player0, player1)
    else:
        currState = GameState(player1, player0)
        c.send(str.encode(currId + '|||' + str(currState)))
        deck1Str = c.recv(4096).decode()
        print('THIS IS THE DECK STRING:', deck1Str)
        player1.buildDeckFromString(deck1Str)
        print('DECK 1 RECIEVED')
        print(deck1Str)        
        startGame(player0, player1)

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
                #print('*************************************************')
                #print('Recieved ', reply)
                #print('*************************************************')
                if reply[-1] != '*':                    
                    contents = reply.split('|||')
                    playerNum = contents[0] #gets the ID
                    activeP = contents[1] #gets that clients player 1
                    passiveP = contents[2] #gets that clients player 2
                    if playerNum == '0':
                        player0.buildPlayerFromString(activeP)
                        player1.buildPlayerFromString(passiveP)
                        stateToReturn = GameState(player0, player1)
                    else:
                        player1.buildPlayerFromString(activeP)
                        player0.buildPlayerFromString(passiveP)
                        stateToReturn = GameState(player1, player0)
                else:
                    playerNum = reply[0]
                    if playerNum == '0':
                        stateToReturn = GameState(player0, player1)
                    else:

                        stateToReturn = GameState(player1, player0)  
                #build the state from the strings


                sendBack = str(stateToReturn)
                #print('*************************************************')
                #print(sendBack)
                #print('*************************************************')
                  
            
            c.sendall(str.encode(sendBack))
            print('sent reply')
        except socket.error as e:
            print(e)
            break 


    print('connection finishied', theID)
    c.close()


while True:
    c, addr = s.accept()
    print(f'Got Connection from {addr}')
    start_new_thread(threadedClient, (c,))