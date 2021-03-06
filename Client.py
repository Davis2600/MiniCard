from tkinter import *
from networktest import *
# cmu_112_graphics cited from 
# http://www.cs.cmu.edu/~112/notes/notes-animations-part1.html
from cmu_112_graphics import *
import random
from card import Card
from player import Player
from state import GameState
from deckimport import importDeck
from button import Button
from utilities import *


#Main App
class ModalGame(ModalApp):
    def appStarted(app):
        buildCardDict()
        app.deckString = ''
        backgroundImageUrl = 'https://i.imgur.com/XtAYLuq.jpg'
        app.backgroundImage = app.loadImage(backgroundImageUrl)
        app.backgroundImage = app.scaleImage(app.backgroundImage, 3.2)
        app.titleScreenMode = TitleScreenMode()
        app.gameMode = Game()
        app.winMode = WinMode()
        app.loseMode = LoseMode()
        app.setActiveMode(app.titleScreenMode)
        app.deckMode = DeckSelectMode()
        app.helpMode = HelpMode()
        
class HelpMode(Mode):
    def appStarted(mode):
        mode.backButton = Button('Back', 600, 750, 100, 50)

    def mousePressed(mode, event):
        if mode.backButton.checkClicked(event.x, event.y):
            mode.app.setActiveMode(mode.app.titleScreenMode)

    def redrawAll(mode, canvas):
        canvas.create_image(mode.width/2, mode.height/2, image = getCachedPhotoImage(mode.app.backgroundImage))
        canvas.create_text(10,10, text = 'Help', font = 'Helvetica 20', anchor = 'nw', fill = 'white')
        canvas.create_text(10, 30, text = 'MiniCard is a simple, two player card game. to play, each player takes\n turns summoning creatures', font = 'Helvetica 20', anchor = 'nw', fill = 'white')
        canvas.create_text(10, 80, text = 'To summon these creatures, each player spends mana. you start with 10\nmana, and that gradually increases over a game', font = 'Helvetica 20', anchor = 'nw', fill = 'white')
        canvas.create_text(10, 130, text = 'The Cost of each card is indicated in the upper left hand corner of the\n card. cards also have effects, attack, and life', font = 'Helvetica 20', anchor = 'nw', fill = 'white')
        canvas.create_text(10, 180, text = 'Cards can attack when they are on the field for more than one turn. \nthey can attack the opponents cards, or the opponent direcltly', font = 'Helvetica 20', anchor = 'nw', fill = 'white')
        canvas.create_text(10, 230, text = 'when you attack the opponent direclty. the opponent loses health equal\n to the attack of your card', font = 'Helvetica 20', anchor = 'nw', fill = 'white')
        canvas.create_text(10, 280, text = 'when cards attack each other, they each deal damage equal to their \nattack to each other', font = 'Helvetica 20', anchor = 'nw', fill = 'white')
        canvas.create_text(10, 330, text = 'The first player to get the opponent down to 0 life, or the last \nplayer to have cards in their deck wins', font = 'Helvetica 20', anchor = 'nw', fill = 'white')
        canvas.create_text(10, 380, text = 'each card also has unique effects that bend the way the rules work, \nthese effects apply automatically, so you will get the', font = 'Helvetica 20', anchor = 'nw', fill = 'white')
        canvas.create_text(10, 430, text = 'hang of it quickly! Have fun', font = 'Helvetica 20', anchor = 'nw', fill = 'white')
        mode.backButton.drawButton(canvas)


# Hub/Title Screen
class TitleScreenMode(Mode):
    def appStarted(mode):
        mode.startButton = Button('Start', mode.width/6, mode.height * 0.80, 200, 100)
        mode.deckButton = Button('Deck   Builder', mode.width/2, mode.height * 0.80, 200, 100)
        mode.helpButton = Button('Help', 5 * mode.width/6, mode.height * 0.80, 200, 100)
        mode.titleImage = getCustomFontText('MiniCard', 45, 'white')
        mode.subMessage = getCustomFontText('a   15  112   creation', 30, 'white')
        mode.creditMessage = getCustomFontText('credit   for   card   images   to  the   shovel   knight   team   at   yacht   club   games', 20, 'white')


    def redrawAll(mode, canvas):

        canvas.create_image(mode.width/2, mode.height/2, image = getCachedPhotoImage(mode.app.backgroundImage))
        canvas.create_image(mode.width/2,mode.height/4, image = getCachedPhotoImage(mode.titleImage))
        canvas.create_image(mode.width/2,mode.height/3, image = getCachedPhotoImage(mode.subMessage))
        canvas.create_image(mode.width/2, mode.height - 30, image = getCachedPhotoImage(mode.creditMessage))
        mode.startButton.drawButton(canvas)
        mode.deckButton.drawButton(canvas)
        mode.helpButton.drawButton(canvas)
        
    def mousePressed(mode, event):
        if mode.startButton.checkClicked(event.x, event.y):
            mode.app.setActiveMode(mode.app.gameMode)
        elif mode.deckButton.checkClicked(event.x, event.y):
            mode.app.setActiveMode(mode.app.deckMode)
        elif mode.helpButton.checkClicked(event.x, event.y):
            mode.app.setActiveMode(mode.app.helpMode)


class WinMode(Mode):
    def appStarted(mode):
        mode.text = getCustomFontText('You    Win', 100, 'white')
        mode.getBack = getCustomFontText('press  enter  to   return   to   title   screen', 25, 'white')
    def redrawAll(mode, canvas):
        canvas.create_image(mode.width/2, mode.height/2, image = getCachedPhotoImage(mode.app.backgroundImage))
        canvas.create_image(mode.width/2,mode.height/2, image = getCachedPhotoImage(mode.text))
        canvas.create_image(mode.width/2,3 * mode.height/4, image = getCachedPhotoImage(mode.getBack))

    def keyPressed(mode, event):
        if event.key == 'Enter':
            mode.app.appStarted()

class LoseMode(Mode):
    def appStarted(mode):
        mode.text = getCustomFontText('You    Lose', 100, 'white')
        mode.getBack = getCustomFontText('press  enter  to   return   to   title   screen', 25, 'white')
    def redrawAll(mode, canvas):
        canvas.create_image(mode.width/2, mode.height/2, image = getCachedPhotoImage(mode.app.backgroundImage))
        canvas.create_image(mode.width/2,mode.height/2, image = getCachedPhotoImage(mode.text))
        canvas.create_image(mode.width/2,3 * mode.height/4, image = getCachedPhotoImage(mode.getBack))

    def keyPressed(mode, event):
        if event.key == 'Enter':
            mode.app.appStarted()  

#Deckbuilder
class DeckSelectMode(Mode):
    def appStarted(mode):
        
        mode.possibleCards = []
        mode.deck = []
        cardListFile = importDeck('cardList.txt')
        mode.possibleCards = DeckSelectMode.buildZoneFromString(cardListFile)
        mode.scrollX = 0
        mode.scrollButton = Button('Scroll Foreward', 700, 400, 150, 50, True)
        mode.scrollBackButton = Button('Scroll Backward', 100, 400, 150, 50, True)
        mode.scrollDist = 50
        mode.selectedFromDeck = False
        mode.scrollDeck = 0
        mode.scrollButtonDeck = Button('Scroll Foreward', 700, 700, 150, 50, True)
        mode.scrollBackButtonDeck = Button('Scroll Backward', 100, 700, 150, 50, True )
        mode.createDeckButton = Button('Export Deck', 400, 750, 120, 50, True )
        mode.backButton = Button('Back', 600, 750, 100, 50)
        mode.message = ''
        backgroundImageUrl = 'https://i.imgur.com/oWKMdMj.png'
        mode.backgroundImage = mode.loadImage(backgroundImageUrl)
        for card in mode.possibleCards:
            card.summoningSickness = False

    def mousePressed(mode, event):
        
        if mode.scrollButton.checkClicked(event.x, event.y) and mode.scrollX < 1000:
            mode.scrollX += mode.scrollDist
        elif mode.scrollBackButton.checkClicked(event.x, event.y) and mode.scrollX > 0:
            mode.scrollX -= mode.scrollDist
        elif mode.scrollButtonDeck.checkClicked(event.x, event.y) and mode.scrollDeck < (len(mode.deck) * 100):
            mode.scrollDeck += 50
        elif mode.scrollBackButtonDeck.checkClicked(event.x, event.y) and mode.scrollDeck > 0:
            mode.scrollDeck -= 50
        elif mode.createDeckButton.checkClicked(event.x, event.y): 
            if len(mode.deck) != 20:
                mode.message = 'Decks Must be 20 Cards Long!'
            else:
                mode.exportDeck()
        elif mode.backButton.checkClicked(event.x, event.y):
            mode.app.setActiveMode(mode.app.titleScreenMode)
        else:
            mode.selectCard(event.x, event.y)

    #reused from player class
    def selectCard(mode, x, y):
        #remove current selection
        for card in mode.possibleCards:
            card.selected = False
        for card in mode.deck:
            card.selected = False
        #make new selection 
        halfWidth, halfHeight = 75, 150
        for card in mode.possibleCards:
            if card.x + halfWidth > x and card.x - halfWidth < x:
                if card.y + halfHeight > y and card.y - halfHeight < y:
                    card.selected = True
                    mode.selectedFromDeck = False
        for card in mode.deck:
            if card.x + halfWidth > x and card.x - halfWidth < x:
                if card.y + halfHeight > y and card.y - halfHeight < y:
                    card.selected = True  
                    mode.selectedFromDeck = True

    #modified from the player class
    def getSelected(mode):
        selection = None
        for card in mode.possibleCards:
            if card.selected == True:
                selection = card
                break
        for card in mode.deck:
            if card.selected == True:
                selection = card
                break
        return selection

    #modified from gameMode
    def mouseDragged(mode, event):
        selection = mode.getSelected()
        if selection != None:
            selection.x = event.x
            selection.y = event.y
    def mouseReleased(mode,event):
        selection = mode.getSelected()
        if selection != None:
            if selection.y > 400 and mode.selectedFromDeck == False:
                if len(mode.deck) < 20:
                    selection.selected = False
                    selectionStr = str(selection)
                    newCard = Card()
                    newCard.createCardFromString(selectionStr)
                    mode.deck.append(newCard)
                    mode.message = f'{selection.name} added to deck'
                else:
                    mode.message = 'Deck is Full'
                    selection.selected = False
            elif selection.y < 400 and mode.selectedFromDeck == True:
                mode.deck.remove(selection)
                mode.message = f'{selection.name} removed from deck'
            else:
                selection.selected = False

    #reused from player class
    def drawCards(mode, canvas, height, width, scroll, cards):
        X, Y = 75, height

        for card in cards:
            if not card.selected:
                card.x = X - scroll
                card.y = Y
            card.drawCard(canvas, width, 'cyan')
            X += width

    def exportDeck(mode):
        deckName = mode.getUserInput('Please Enter Deck Name')
        newDeckFile = open(deckName, 'w+')
        for card in mode.deck[0:-1]:
            newDeckFile.write(str(card) + '\n')
        newDeckFile.write(str(mode.deck[-1]))
        newDeckFile.close()
        mode.message = f'Created Deck file {deckName}.txt'

    #reused from player class
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

    def redrawAll(mode, canvas):
        canvas.create_image(mode.width/2, mode.height/2, image = getCachedPhotoImage(mode.app.backgroundImage))
        canvas.create_text(10,10, text = 'Deck Buider', font = 'Helvetica 20', anchor = 'nw')
        mode.drawCards(canvas, 200, 150, mode.scrollX, mode.possibleCards)
        mode.drawCards(canvas, 600, 100, mode.scrollDeck, mode.deck)
        mode.scrollButton.drawButton(canvas)
        mode.scrollBackButton.drawButton(canvas)
        mode.scrollButtonDeck.drawButton(canvas)
        mode.scrollBackButtonDeck.drawButton(canvas)
        mode.createDeckButton.drawButton(canvas)
        canvas.create_text(mode.width/2,mode.height/2, text = f'{len(mode.deck)} / 20 Cards', fill = 'black')
        mode.backButton.drawButton(canvas)
        canvas.create_text(mode.width - 20, 0, text = mode.message, font = 'Helevetica 20', anchor = 'ne', fill = 'red')

#The main course, the Game itsself
class Game(Mode):
    def appStarted(self):
        self.timePassed = 0
        deck = None
        self.network = None 
        self.network = Network()
        self.serverIssue = False
        self.state = None
        self.deckSelected = False
        self.connected = False
        self.serverIssueText = 'SERVER ISSUE: press enter to return to title.'
        activePlayerBackgroundUrl = 'https://i.imgur.com/AvQiTLl.jpg'
        passivelPlayerBackgroundUrl = 'https://i.imgur.com/jmzZ2FN.jpg'
        self.activePlayerBackground = self.loadImage(activePlayerBackgroundUrl)
        self.passivePlayerBackground = self.loadImage(passivelPlayerBackgroundUrl)
        self.nextTurnButton = Button('End   Turn', 700, 400, 100, 50, True)

        while deck == None:
            try:
                deckList = self.getUserInput('Enter the deck file name (.txt)')
                deck = importDeck(deckList)
                self.deckSelected = True
            except:
                deck = None
        try:
            self.state = self.network.connect(deck)
            self.connected = True

        except:
            self.serverIssue = True
            self.deckSelected = False
            self.deck = None
        #self.startGame()
        if self.deckSelected and self.connected:
            self.state.activePlayer.firstTurn = False 
            if self.network.id == '0':
                opponentImageUrl = 'https://i.imgur.com/49O2D8T.png'
                self.state.activePlayer.opponentImage = self.loadImage(opponentImageUrl)
                opponentImageUrl = 'https://i.imgur.com/FxJDMuo.png'
                self.state.opponent.opponentImage = self.loadImage(opponentImageUrl)
            else:
                opponentImageUrl = 'https://i.imgur.com/FxJDMuo.png'
                self.state.activePlayer.opponentImage = self.loadImage(opponentImageUrl)
                opponentImageUrl = 'https://i.imgur.com/49O2D8T.png'
                self.state.opponent.opponentImage = self.loadImage(opponentImageUrl)


    def sendData(self, passive = False):
        if not passive:
            data = str(self.network.id) + '|||' + str(self.state)
        else:
            data = self.network.id + '*'
        reply = self.network.send(data)
        if reply == None:
            self.serverIssue = True
            return
        components = reply.split('|||')
        try:
            activeP = components[0]
            passiveP = components[1]
        except:
            self.serverIssue = True
            return
        self.state.activePlayer.buildPlayerFromString(activeP)
        self.state.opponent.buildPlayerFromString(passiveP)
        
    
    def mousePressed(self, event):
        if not self.connected or not self.deckSelected:
            return
        if self.nextTurnButton.checkClicked(event.x,event.y) and self.state.activePlayer.currentPlayer == True:
            for card in self.state.activePlayer.board:
                card.summoningSickness = False
                card.attackedThisTurn = False
            self.swapTurns()
            self.sendData()
        self.state.activePlayer.selectCard(event.x, event.y)
        selection = self.state.activePlayer.getSelected()
        if selection != None and selection in self.state.activePlayer.board:
            taunt, activeTargets = self.tauntCheck()
            if taunt:
                self.state.activePlayer.message = f"an    Opponents   creature   is   taunting"
            else:
                self.state.activePlayer.message = f'Pick   a   Valid   Target'
            for card in self.state.opponent.board:
                if card in activeTargets:
                    card.target = True
        
    def keyPressed(self,event):
        if self.serverIssue and event.key == 'Enter':
            self.app.setActiveMode(self.app.titleScreenMode)
            self.serverIssue = False
            return
        if event.key == '0':
            self.state.activePlayer, self.state.opponent = self.state.opponent, self.state.activePlayer
        if event.key == 'Enter' and self.state.activePlayer.currentPlayer == True:
            for card in self.state.activePlayer.board:
                card.summoningSickness = False
                card.attackedThisTurn = False
            self.swapTurns()
            self.sendData()


    def swapTurns(self):
            self.state.activePlayer.message = 'Turn   Over'
            self.state.opponent.message = 'Turn   Started!'
            self.state.activePlayer.currentPlayer = False 
            self.state.opponent.currentPlayer = True
            activePlayers = self.state.activePlayer, self.state.opponent
            for activePlayer in activePlayers:
                if activePlayer.currentPlayer:
                    if activePlayer.firstTurn:
                        activePlayer.firstTurn = False
                    else:
                        losecheck = activePlayer.pickupCard()
                        if losecheck == 0:
                            self.state.opponent.health = 0
                            self.app.setActiveMode(self.app.winMode)
                            self.checkWin()    
                        if activePlayer.mana < activePlayer.manaMax:
                            activePlayer.mana += 1
                        activePlayer.currMana = activePlayer.mana

    def mouseDragged(self, event):
        if not self.connected or not self.deckSelected:
            return
        selection = self.state.activePlayer.getSelected()
        if selection != None:
            selection.x = event.x
            selection.y = event.y

    
    def mouseReleased(self, event):
        if not self.connected or not self.deckSelected:
            return
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
            self.attemptAttack(selection, event.x, event.y)
            selection.selected = False
            for card in self.state.opponent.board:
                card.target = False
            self.sendData()
            return 
        
    def timerFired(self):
        if not self.connected or not self.deckSelected:
            return
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
            if self.state.activePlayer.currMana >= selection.cost and len(self.state.activePlayer.board) < 7:
                if len(self.state.activePlayer.board) == 6:
                    self.state.activePlayer.message = 'You   cannot   summon   more   than   6   monsters'
                    return
                self.state.activePlayer.currMana -= selection.cost
                self.state.activePlayer.hand.remove(selection)
                self.state.activePlayer.board.append(selection)
                self.state.activePlayer.message = f'Summoned   {selection.name}' 
                self.state.opponent.message = f'Opponent   summoned   {selection.name}'
                if selection.effect == 'Rush':
                    selection.summoningSickness = False
                if selection.effect == 'Companion':
                    self.state.activePlayer.board.append(Card('Mummy', 0, (3,1), None))
            else:
                self.state.activePlayer.message = 'Insufficent   Mana'


    def attemptAttack(self, selection, x , y):
        if selection.summoningSickness:
            self.state.activePlayer.message = f'{selection.name}   has   summoning   sickness!'
            return 
        if selection.attackedThisTurn:
            self.state.activePlayer.message = f'{selection.name}   already   attacked!!' 
            return

        #check if card attack
        #taunt check
        taunt = False 
        validTargets = [] #list of valid tagets to attack 
        taunt, validTargets = self.tauntCheck()
        halfHeight, halfWidth = Player.cardWidth + 20, (Player.cardWidth / 2) + 20
        for card in validTargets:
            card.target = True
        for enemyCard in validTargets:
            bounds = enemyCard.x - halfWidth, enemyCard.y - halfHeight, \
                     enemyCard.x + halfWidth, enemyCard.y + halfHeight
            if Game.checkInField(x, y, bounds):
                self.doAttack(selection, enemyCard)
                
                return 
        #direct attack
        if Game.checkInField(x, y, Player.enemyBoxDims) and not taunt:
            self.state.activePlayer.message = f'{selection.name}   attacked   the   oposing   hero   for   {selection.attack}   damage'
            self.state.opponent.message = f'We  took   {selection.attack}   damage'
            selection.attackedThisTurn = True
            self.state.opponent.health -= selection.attack
            self.checkWin()
            return 

    def doAttack(self, selection, target):
        if selection.effect == 'Poison':
            target.curLife = 0
            selection.curLife -= target.attack
            selection.curLife -= target.attack
        elif target.effect == 'Poison':
            selection.curLife = 0
            target.curLife -= selection.attack
        elif selection.effect == 'QuickStrike':
            target.curLife -= selection.attack
            if target.curLife != 0:
                selection.curLife -= target.attack
        else:
            if target.effect != 'DivineShield':
                self.state.activePlayer.message = f'{selection.name}   attacked   the   oposing   {target.name}   for   {selection.attack}   damage'
                self.state.opponent.message = f'{target.name}   took   {selection.attack}   damage'
            target.curLife -= selection.attack
            selection.curLife -= target.attack
            if target.effect == 'DivineShield':
                target.effect = None
                target.curLife = target.maxLife
            if selection.effect == 'DivineShield':
                selection.effect = None
                selection.curLife = selection.maxLife

        self.state.activePlayer.clearBoard()
        self.state.opponent.clearBoard()
        selection.attackedThisTurn = True


    def tauntCheck(self):
        validTargets = []
        taunt = False
        for enemyCard in self.state.opponent.board:
            if enemyCard.effect == 'Taunt':
                taunt = True
                validTargets.append(enemyCard)
        if validTargets == []:
            validTargets = self.state.opponent.board
        return taunt, validTargets

    def checkWin(self):
        if self.state.activePlayer.health <= 0:
            self.app.setActiveMode(self.app.loseMode)
        elif self.state.opponent.health <= 0:
            self.app.setActiveMode(self.app.winMode)
   
    @staticmethod
    def checkInField(x, y, dims):
        if x > dims[0] and y > dims[1] and x < dims[2] and y < dims[3]:
            return True
        else:
            return False

        

    def redrawAll(self, canvas):
        if self.serverIssue:
            canvas.create_text(self.width/2,self.height/2, text = self.serverIssueText,
                        font = 'Helvetica 30', fill = 'red')
            return
        if not self.connected or not self.deckSelected:
            return
        
        #canvas.create_rectangle(100, 0, 700, 500, fill = 'light blue')
        if self.state.activePlayer.currentPlayer == True:
            canvas.create_image(self.width/2, self.height/2, image = getCachedPhotoImage(self.activePlayerBackground))
        else:
            canvas.create_image(self.width/2, self.height/2, image = getCachedPhotoImage(self.passivePlayerBackground))        
        self.state.opponent.draw(canvas, self.width, self.height, 1)
        self.state.activePlayer.draw(canvas, self.width, self.height, 0) 
        #TODO make this message more visible
        #canvas.create_text(self.width - 10, self.height, text = 'Press   "Enter"   to   end   your   turn',
        # anchor  = 'se', font = 'Helvetica 15', fill = 'black')
        self.nextTurnButton.drawButton(canvas)


app = ModalGame(width = 800, height = 800)