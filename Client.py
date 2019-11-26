from tkinter import *
from networktest import *
# cmu_112_graphics cited from 
# http://www.cs.cmu.edu/~112/notes/notes-animations-part1.html
from cmu_112_graphics import *
import random
from card import Card
from player import Player
from state import GameState

class ModalGame(ModalApp):
    def appStarted(app):

        app.titleScreenMode = TitleScreenMode()
        app.gameMode = Game()
        app.winMode = WinMode()
        app.loseMode = LoseMode()
        app.setActiveMode(app.titleScreenMode)

class TitleScreenMode(Mode):

    def redrawAll(mode, canvas):
        canvas.create_text(mode.width/2,mode.height/2, text = "MiniCards: Press Enter to Begin",
            font = "Helvetica 28")

    def keyPressed(mode, event):
        mode.app.setActiveMode(mode.app.gameMode)

class WinMode(Mode):

    def redrawAll(mode, canvas):
        canvas.create_text(mode.width/2,mode.height/2, text = "You Win",
            font = "Helvetica 28", fill = 'green')

    def keyPressed(mode, event):
        mode.app.setActiveMode(mode.app.gameMode)

class LoseMode(Mode):

    def redrawAll(mode, canvas):
        canvas.create_text(mode.width/2,mode.height/2, text = "You Lose",
            font = "Helvetica 28", fill = 'red')

    def keyPressed(mode, event):
        mode.app.setActiveMode(mode.app.gameMode)        

class Game(Mode):
    def appStarted(self):
        self.network = Network()
        
        #activePlayer = Player()
        #TODO for now, the opponent is also a player created in the client, it should eventually recieve from server
        #opponent = Player()
        #opponent.currentPlayer = False
        self.state = self.network.connect()
        #self.startGame()
        self.timePassed = 0
        self.state.activePlayer.firstTurn = False # first turn prevents gaining extra mana on first turn, only effects p2

    def sendData(self, passive = False):
        print('sending Data')
        if not passive:
            data = str(self.network.id) + '|||' + str(self.state)
        else:
            data = self.network.id + '*'
        reply = self.network.send(data)
        print('completed')
        components = reply.split('|||')
        activeP = components[0]
        passiveP = components[1]
        self.state.activePlayer.buildPlayerFromString(activeP)
        self.state.opponent.buildPlayerFromString(passiveP)
        print(type(self.state))
        


    
    def mousePressed(self, event):
        self.state.activePlayer.selectCard(event.x, event.y)
        
    def keyPressed(self,event):
        if event.key == '0':
            print('switching sides')
            self.state.activePlayer, self.state.opponent = self.state.opponent, self.state.activePlayer
        if event.key == 'Enter' and self.state.activePlayer.currentPlayer == True:
            #print(self.state.activePlayer)
            for card in self.state.activePlayer.board:
                card.summoningSickness = False
                card.attackedThisTurn = False
            self.swapTurns()
            self.sendData()


    def swapTurns(self):
            self.state.activePlayer.message = 'Turn Over'
            self.state.activePlayer.currentPlayer = False 
            self.state.opponent.currentPlayer = True
            activePlayers = self.state.activePlayer, self.state.opponent
            for activePlayer in activePlayers:
                if activePlayer.currentPlayer:
                    if activePlayer.firstTurn:
                        activePlayer.firstTurn = False
                    else:
                        activePlayer.pickupCard()
                        if activePlayer.mana < activePlayer.manaMax:
                            activePlayer.mana += 1
                        activePlayer.currMana = activePlayer.mana

    def mouseDragged(self, event):
        selection = self.state.activePlayer.getSelected()
        if selection != None:
            selection.x = event.x
            selection.y = event.y
    
    def mouseReleased(self, event):
        print('released')
        #if selection in hand, try to summon 
        selection = self.state.activePlayer.getSelected()
        if selection == None:
            return
        if not self.state.activePlayer.currentPlayer:
            selection.selected = False
            return 
        if selection != None and selection in self.state.activePlayer.hand:
            self.attemptSummon(selection, event.x, event.y)
            selection.selected = False
            self.sendData()
            return 
        if selection != None and selection in self.state.activePlayer.board:
            pass
            self.attemptAttack(selection, event.x, event.y)
            selection.selected = False
            self.sendData()
            return 
        
    def timerFired(self):
        self.timePassed += 1
        if self.timePassed == 10:
            if self.state.activePlayer.currentPlayer == False:
                self.sendData(passive = True)
                self.checkWin()
            self.timePassed = 0


    def attemptSummon(self, selection, x, y):
        leftMargin, rightMargin = 100, self.width - 100
        bottomMargin = self.height - 200
        if Game.checkInField(x, y, (leftMargin, 0, rightMargin, bottomMargin)):
            print('released in field')
            if self.state.activePlayer.currMana >= selection.cost and len(self.state.activePlayer.board) < 6:
                self.state.activePlayer.currMana -= selection.cost
                self.state.activePlayer.hand.remove(selection)
                self.state.activePlayer.board.append(selection)
                self.state.activePlayer.message = f'Summoned {selection.name}'               
            else:
                self.state.activePlayer.message = 'Insufficent Mana'


    def attemptAttack(self, selection, x , y):
        if selection.summoningSickness or selection.attackedThisTurn:
            return
        #first check if direct attack
        if Game.checkInField(x, y, Player.enemyBoxDims):
            print('attacking opponent')
            selection.attackedThisTurn = True
            self.state.opponent.health -= selection.attack
            self.checkWin()
            return 
        #check if card attack
        halfHeight, halfWidth = Player.cardWidth + 20, (Player.cardWidth / 2) + 20
        for enemyCard in self.state.opponent.board:
            bounds = enemyCard.x - halfWidth, enemyCard.y - halfHeight, \
                     enemyCard.x + halfWidth, enemyCard.y + halfHeight
            if Game.checkInField(x, y, bounds):
                enemyCard.curLife -= selection.attack
                selection.curLife -= enemyCard.attack
                self.state.activePlayer.clearBoard()
                self.state.opponent.clearBoard()
                selection.attackedThisTurn = True
                return 
        
    def checkWin(self):
        if self.state.activePlayer.health <= 0:
            self.app.setActiveMode(self.app.loseMode)
        elif self.state.opponent.health <= 0:
            self.app.setActiveMode(self.app.winMode)
   
    @staticmethod
    def checkInField(x, y, dims):
        if x > dims[0] and y > dims[1] and x < dims[2] and y < dims[3]:
            print('True')
            return True
        else:
            print('False')
            return False

        

    def redrawAll(self, canvas):
        #canvas.create_rectangle(100, 0, 700, 500, fill = 'light blue')
        if self.state.activePlayer.currentPlayer == True:
            canvas.create_rectangle(0,0,self.width,self.height, width = 20, outline = 'green')
        else:
             canvas.create_rectangle(0,0,self.width,self.height, width = 20, outline = 'orange')           
        self.state.opponent.draw(canvas, self.width, self.height, 1)
        self.state.activePlayer.draw(canvas, self.width, self.height, 0) 
        canvas.create_text(self.width - 10, self.height, text = 'Press "Enter" to end your turn',
         anchor  = 'se', font = 'Helvetica 15', fill = 'black')
        



app = ModalGame(width = 800, height = 800)