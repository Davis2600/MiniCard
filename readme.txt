Hello.
Welcome to MiniCard! a fun little python based card game. here's all the information you 
need to get started. 

**** 
Description
****
This is a lightweight, 8-bit inspired Trading Card Game that is fully customizable. In 
MiniCard, players can build their own 20 card decks using the cards we provide before 
jumping into battle against other players online. deck lists are saved as .txt files, and
can be easily shared with friends. The gameplay is quick to pick up, and provides 
interesting depth with all of the in game effects and mechanics. 

*****
How to Run
*****
locally: 
The entire game can be run locally. First cd into the MiniCard directory, and run the 
server.py file. Afterwards, you can then open two other terminals and both run clients.
online:
The game can also work over wireless networks, but the server ip will have to be changed 
in the server.py file to be set to the name of whatever server you host the server file 
on. Then, the networktest.py files would have to be set to point to that server, and the 
game will run online. 

*****
Libraries
****
Minicard has minimal dependancies. The only modules imported are:
Tkinter
PIL
requests
sockets
the only thing you should have to install is PIL!!

****
Shortcuts
****
When the game is run locally. the user has access to both sides of the game; therefore
almost any game state can be recreated with minimal effort. It is for this reason that 
there are no shortcuts/cheat codes.