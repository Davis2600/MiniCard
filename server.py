import socket
import sys
from _thread import *

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
values = [1,2,3,4,5]



def threadedClient(c):
    global currId, values
    c.send(str.encode(currId))
    if currId == '1':
        currId = '0'
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
                stuff = reply.split(',')
                index = stuff[0]
                newVal = stuff[1]
                values[int(index)] = int(newVal)

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