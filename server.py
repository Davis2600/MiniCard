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

#init the shared game state
player0 = Player()
player1 = Player()
player1.currentPlayer = False
for i in range(5):
    player0.pickupCard()
    player1.pickupCard()

def threadedClient(c):
    global currId, player0, player1
    theID = currId

    
    if currId == '0':
        currState = GameState(player0, player1)
        c.send(str.encode(currId + '|||' + str(currState)))
        currId = '1'
    else:
        currState = GameState(player1, player0)
        c.send(str.encode(currId + '|||' + str(currState)))
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
                print('*************************************************')
                print('Recieved ', reply)
                print('*************************************************')
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
                print('*************************************************')
                print(sendBack)
                print('*************************************************')
                  
            
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