import socket
from player import Player
from state import GameState

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = 'localhost'
        #change this when using on other computers
        self.port = 2345
        self.addr = (self.host, self.port)
        self.id = 'temp'

    def connect(self):
        self.client.connect(self.addr)
        firstMessage = self.client.recv(4096).decode()
        contents = firstMessage.split('|||')
        self.id = contents[0]
        player0 = Player()
        player1 = Player()
        player0.buildPlayerFromString(contents[1])
        player1.buildPlayerFromString(contents[2])
        return GameState(player0, player1)

    def send(self, data):
        try:
            print('sending')
            self.client.send(str.encode(data))
            reply = self.client.recv(4096).decode()
            print('received')
            return reply
        except socket.error as e:
            return str(e)

    def end(self):
        self.client.close()

'''
def sendData(toSend):
    print('sending Data')
    data = str(network.id) + '|||' + str(toSend)
    reply = network.send(data)
    print('completed')
    return reply

network = Network()
run = True
number = 5
while run:
    number = input('Hello Friend, input a number')
    print('input = ', number)
    message = sendData(number)
    print('the message = ', message)
'''
