from tkinter import *
#from networktest import *
# cmu_112_graphics cited from 
# http://www.cs.cmu.edu/~112/notes/notes-animations-part1.html
from cmu_112_graphics import *
import random
class Card(object):
    fontSizeRatio = 0.3
    nameSizeRatio = 0.15
    def __init__(self, name, image, cost, stats, effect):
        self.x = 100
        self.y = 100
        
        #card Stuff
        self.name = name
        self.cost = cost
        self.attack = stats[0]
        self.maxLife = stats[1]
        self.curLife = self.maxLife
        self.effect = effect
        self.selected = False

        def __repr__(self):
            return f'{self.name}: cost:{self.cost}, attack:{self.attack}, life:{self.life}'

    def drawCard(self, canvas, width, color):
        height = 2 * width
        if self.selected:
            outline = 'yellow'
        else:
            outline = 'black'
        font = 'Helvetica ' + str(int(width * Card.fontSizeRatio))
        nameFont = 'Helvetica ' + str(int(width * Card.nameSizeRatio))
        canvas.create_rectangle(self.x - (width/2), self.y - (height/2), self.x + (width/2), self.y + (height/2),
                                fill = 'light blue', outline = outline)
        canvas.create_text(self.x - (width/2), self.y - (height/2), text = str(self.cost), font = font, fill = color, anchor = 'nw')
        canvas.create_text(self.x, self.y - (3/8) * height, text = self.name, font  = nameFont)
        canvas.create_text(self.x - (width/4), self.y + (height/4), text = str(self.attack), font = font)
        canvas.create_text(self.x + (width/4), self.y + (height/4), text = str(self.curLife), font = font)

class Player(object):
    def __init__(self):
        self.health = 20
        self.mana = 1
        self.currMana = 6
        self.manaMax = 10
        self.hand = []
        self.deck = []
        self.discard = []
        self.board = []
        self.makeBasicDeck()
        self.message = '' #message to be displayed to the player at a given time
        random.shuffle(self.deck)

    def draw(self, canvas, width, height, side):
        #Draw Hand 
        self.drawHand(canvas, size)
        self.drawHud(canvas, width, height)
        #Draw Deck
        canvas.create_rectangle(675, 575, 775, 725, fill = 'light blue')

    def drawHand(self, canvas, side):
        X, Y = 100, 725
        if side == 0: #main player
            for card in self.hand:
                if not card.selected:
                    card.x = X
                    card.y = Y
                card.drawCard(canvas, 100, 'light blue')
                X += 100
        
    
    def drawBoard(self, canvas, side):
        X, Y = 100, 525
        if side == 0: #main player
            for card in self.hand:
                if not card.selected:
                    card.x = X
                    card.y = Y
                card.drawCard(canvas, 100, 'light red')
                X += 100       

    def drawHud(self, canvas, width, height):
        canvas.create_text(720, 630, text = f'{len(self.deck)}')
        canvas.create_text(width, height, anchor = 'se', text = str(self.health), font = 'Helvetica 30', 
                           fill = 'red')
        canvas.create_text(0, width, anchor = 'sw', text = str(self.currMana), font = 'Helvetica 30', 
                           fill = 'blue')
        canvas.create_text(width/2, 20, text = self.message, font = 'Helvetica 25')


    def makeBasicDeck(self):
        for i in range(5):
            self.deck.append(Card('Newt', None, 1, (2,1), None))
        for i in range(4):
            self.deck.append(Card('Minion', None, 2, (3,3), None))
        for i in range(3):
            self.deck.append(Card('Hound', None, 4, (5,2), None))
        for i in range(4):
            self.deck.append(Card('Beast', None, 6, (8,8), None))
        for i in range(2):
            self.deck.append(Card('Dragon', None, 10, (12,12), None))
            
    #reanamed to avoid confusion with draw methods
    def pickupCard(self):
        self.hand.append(self.deck.pop())

    def clearBoard(self):
        removeCount = 0
        for card in self.board:
            if card.curLife <= 0:
                self.board.remove(card)
                removeCount += 1
        print(removeCount)

    def selectCard(self, x, y):
        #recall past selection 
        pastSelection = self.getSelected()
        #remove current selection
        for card in self.hand:
            card.selected = False
        for card in self.board:
            card.selected = False
        #make new selection 
        halfWidth, halfHeight = 50, 100
        for card in self.hand:
            if card.x + halfWidth > x and card.x - halfWidth < x:
                if card.y + halfHeight > y and card.y - halfHeight < y:
                    card.selected = True  
        for card in self.board:
            if card.x + halfWidth > x and card.x - halfWidth < x:
                if card.y + halfHeight > y and card.y - halfHeight < y:
                    card.selected = True   
 

    def getSelected(self):
        selection = None
        for card in self.hand:
            if card.selected == True:
                selection = card
                break
        for card in self.board:
            if card.selected == True:
                selection = card
                break
        return selection
    #TODO repr for online


class GameState(object):
    def __init__(self, player, opponent):
        self.player = player
        self.opponent = opponent
    def __repr__(self):
        return str([str(self.player), str(self.oponent)])

#NOTE #MP indicates stuff that must be derived from the other player, or code that must be moved to the server
class myApp(App):
    def appStarted(self):
        #network = Network()
        player = Player()
        #TODO for now, the opponent is also a player created in the client, it should eventually recieve from server
        opponent = Player()
        self.state = GameState(player, opponent)
        self.activePlayer = True #will need a way to pick active player 
    
        self.startGame()

    def startGame(self):
        for i in range(5):
            self.state.player.drawCard()
            self.state.opponent.drawCard()
    
    def mousePressed(self, event):
        self.state.player.selectCard(event.x, event.y)
        


    def mouseDragged(self, event):
        selection = self.state.player.getSelected()
        if selection != None:
            selection.x = event.x
            selection.y = event.y

    def mouseReleased(self, event):
        print('released')
        leftMargin, rightMargin = 100, self.width - 100
        bottomMargin = self.height - 300
        selection = self.state.player.getSelected()
        if selection != None and event.x > leftMargin and event.x < rightMargin and \
        event. y < bottomMargin:
            print('released in field')
            if self.state.player.currMana > selection.cost and len(self.state.player.board) < 6:
                self.state.player.currMana -= selection.cost
                self.state.player.hand.remove(selection)
                self.state.player.board.append(selection)
                self.state.player.message = f'Summoned {selection.name}'
            else:
                self.state.player.message = 'Insufficent Mana'


        

    def redrawAll(self, canvas):
        canvas.create_rectangle(100, 0, 700, 500, fill = 'light blue')
        self.state.player.draw(canvas, app.width, app.height, 0) 


app = myApp(800, 800)