from tkinter import *
#from networktest import *
# cmu_112_graphics cited from 
# http://www.cs.cmu.edu/~112/notes/notes-animations-part1.html
from cmu_112_graphics import *
import random
from card import Card

class Player(object):
    enemyBoxDims = 300, 0, 600, 100
    manaMax = 10  
    cardWidth = 100
    def __init__(self):
        self.health = 20
        self.currentPlayer = True
        self.mana = 1
        self.currMana = 1 
        self.firstTurn = True  #used to prevent first the second player from starting with two mana and drawing
        self.hand = []
        self.deck = []
        self.discard = []
        self.board = []
        self.makeBasicDeck()
        self.message = '' #message to be displayed to the player at a given time
        self.gameStarted = False
        random.shuffle(self.deck)

    def draw(self, canvas, width, height, side):
        #Draw Hand 
        self.drawHand(canvas, side)
        self.drawBoard(canvas, side)
        self.drawHud(canvas, width, height, side)
        #Draw Deck
        canvas.create_rectangle(675, 575, 775, 725, fill = 'light blue')
        canvas.create_text(720, 630, text = f'{len(self.deck)}')

    def drawHand(self, canvas, side):
        X, Y = 100, 725
        if side == 0: #main player
            for card in self.hand:
                if not card.selected:
                    card.x = X
                    card.y = Y
                card.drawCard(canvas, Player.cardWidth, 'light blue')
                X += 100
        
    
    def drawBoard(self, canvas, side):
        X, Y = 100, 425
        if side == 0: #main player
            for card in self.board:
                if not card.selected:
                    card.x = X
                    card.y = Y
                card.drawCard(canvas, Player.cardWidth, 'light blue')
                X += 150    
        X, Y = 100, 200 
        if side == 1: # opponent
            for card in self.board:
                if not card.selected:
                    card.x = X
                    card.y = Y
                card.drawCard(canvas, Player.cardWidth, 'red')
                X += 150    
            canvas.create_rectangle(Player.enemyBoxDims[0], Player.enemyBoxDims[1], 
                                     Player.enemyBoxDims[2], Player.enemyBoxDims[3],
                                     fill = 'red')


    def drawHud(self, canvas, width, height, side):
        if side == 0:
            canvas.create_text(0, 0, text = self.message, font = 'Helvetica 25', anchor = 'nw')
            canvas.create_text(5, width, anchor = 'sw', text = str(self.currMana), font = 'Helvetica 30', 
                           fill = 'blue')
            canvas.create_text(5, height - 30, anchor = 'sw', text = str(self.health), font = 'Helvetica 30', 
                           fill = 'red')
        if side  == 1:
            canvas.create_text(Player.enemyBoxDims[0], Player.enemyBoxDims[1], anchor = 'nw', text = str(self.currMana), font = 'Helvetica 30', 
                           fill = 'blue')
            canvas.create_text(Player.enemyBoxDims[2], Player.enemyBoxDims[3], anchor = 'se', text = str(self.health), font = 'Helvetica 30', 
                           fill = 'black')            


    def makeBasicDeck(self):
        for i in range(3):
            self.deck.append(Card('Newt', 1, (2,1), 'Rush'))
        for i in range(4):
            self.deck.append(Card('Pally', 1, (2,2), 'DivineShield'))
        for i in range(4):
            self.deck.append(Card('Minion', 2, (3,3), 'Taunt'))
        for i in range(3):
            self.deck.append(Card('Hound', 2, (1,8), 'Poison'))
        for i in range(4):
            self.deck.append(Card('Beast', 4, (8,8), 'QuickStrike'))
        for i in range(2):
            self.deck.append(Card('Dragon', 10, (12,12), None))
            
    #reanamed to avoid confusion with draw methods
    def pickupCard(self):
        self.hand.append(self.deck.pop())

    def clearBoard(self):
        removeList = []
        index = 0
        while index < len(self.board):
            if self.board[index].curLife <= 0:
                removeList.append(self.board[index].name)
                self.discard.append(self.board[index])
                self.board.remove(self.board[index])
            else:
                index += 1
        if len(removeList) > 0:
            removeString = ', '.join(removeList) + ' Died'         
            self.message = removeString

    def selectCard(self, x, y):
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

    def buildPlayerFromString(self, string):
        components = string.split(';')
        self.health = int(components[0])
        self.currentPlayer = (components[1] == 'True')
        self.mana = int(components[2])
        self.currMana = int(components[3])
        self.firstTurn = (components[4] == 'True')
        self.message = components[5]
        self.gameStarted = components[6]
        self.deck = Player.buildZoneFromString(components[7])
        self.hand = Player.buildZoneFromString(components[8])
        self.board = Player.buildZoneFromString(components[9])
        self.discard = Player.buildZoneFromString(components[10])

    def buildDeckFromString(self, string):
        print('building deck from string', string)
        self.deck = Player.buildZoneFromString(string)
        print(self.deck)
           
    @staticmethod
    def buildZoneFromString(string):
        if string == '':
            return []
        zoneString = string.split(',')
        zoneList = []
        for cardString in zoneString:
            card = Card()
            card.createCardFromString(cardString)
            zoneList.append(card)
        return zoneList

        

    def __repr__(self):
        deck = ''
        for card in self.deck:
            deck = deck + str(card) + ','
        if deck != '':
            deck = deck[0:-1] #remove last comma
        hand = ''
        for card in self.hand:
            hand = hand + str(card) + ','
        if hand != '':
            hand = hand[0:-1]
        board = ''
        for card in self.board:
            board = board +  str(card) + ','
        if board != '':
            board = board[0:-1]
        discard = ''
        for card in self.discard:
            discard = discard + str(card) + ','
        if discard != '':
            discard = discard[0:-1]
        cards = deck + ';' + hand + ';' + board + ';' + discard + ';'
        rep = (str(self.health) + ';' +
               str(self.currentPlayer) + ';' +
               str(self.mana) + ';' +
               str(self.currMana) + ';' +
               str(self.firstTurn) + ';' +
               str(self.gameStarted) + ';' +
               str(self.message) + ';' + cards)
               
        return rep