from tkinter import *
# cmu_112_graphics cited from 
# http://www.cs.cmu.edu/~112/notes/notes-animations-part1.html
from cmu_112_graphics import *
from utilities import *
class Card(object):
    fontSizeRatio = 0.3
    nameSizeRatio = 0.15
    cardCount =0
    def __init__(self, name = 'none', cost = 0, stats = (0,0), effect = 'none', image = None):

        
        #card Stuff
        self.name = name
        self.cost = cost
        self.attack = stats[0]
        self.maxLife = stats[1]
        self.curLife = self.maxLife
        self.effect = effect        
        self.selected = False
        Card.cardCount += 1
        self.x = -1 # -1 indicates not visible on the board
        self.y = -1
        self.id = self.cardCount #even identical cards stat wise are unique
        self.summoningSickness = True
        self.attackedThisTurn = False
        self.target = False


        def __repr__(self):
            return f'{self.name}: cost:{self.cost}, attack:{self.attack}, life:{self.life}'

    def getCardZones(self, width, color):
        cardImg = getCardImage(self.name)
        fontSize = int(width * Card.fontSizeRatio)
        nameFontSize = int(width * Card.nameSizeRatio)
        nameImg = getCustomFontText(str(self.name), nameFontSize, color)
        statImg = getCustomFontText(str(self.attack) + '      ' + str(self.curLife), fontSize, color)
        effectImg = getCustomFontText(self.effect, nameFontSize, color)
        costColor = color
        if self.summoningSickness:
            costColor = 'Green'
        costImg = getCustomFontText(str(self.cost), fontSize, costColor)
        return nameImg, statImg, effectImg, costImg, cardImg

    def drawCard(self, canvas, width, outline):
        zones = self.getCardZones(width, outline)
        height = 2 * width
        if self.selected:
            outline = 'yellow'
        elif self.target:
            outline = 'light green'
        elif self.attackedThisTurn == True:
            outline = 'white'
        else:
            outline = outline

        fillColor = 'black'
            
        font = 'system ' + str(int(width * Card.fontSizeRatio))
        nameFont = 'system ' + str(int(width * Card.nameSizeRatio))
        canvas.create_rectangle(self.x - (width/2), self.y - (height/2), self.x + (width/2), self.y + (height/2),
                                fill = fillColor, outline = outline, width = 6)
        #canvas.create_text(self.x - (width/2), self.y - (height/2), text = str(self.cost), font = font, fill = costColor, anchor = 'nw')
        canvas.create_image(self.x - (width/2) + 6, self.y - (height/2) + 6, image = getCachedPhotoImage(zones[3]), anchor = 'nw')
        #canvas.create_text(self.x, self.y - (3/8) * height, text = self.name, font  = nameFont)
        canvas.create_image(self.x, self.y - (3/8) * height, image = getCachedPhotoImage(zones[0]))
        canvas.create_image(self.x, self.y + (1/3) * height, image = getCachedPhotoImage(zones[1]))
        #canvas.create_text(self.x - (width/4), self.y + (height/4), text = str(self.attack), font = font)
        #canvas.create_text(self.x + (width/4), self.y + (height/4), text = str(self.curLife), font = font)
        #canvas.create_text(self.x, self.y, text = self.effect, font = nameFont)
        canvas.create_image(self.x,self.y + (1/4) * height, image = getCachedPhotoImage(zones[2]))
        if zones[4] != None:
            canvas.create_image(self.x,self.y, image = getCachedPhotoImage(zones[4]))
    def createCardFromString(self, string):
        components = string.split(':')
        self.name = components[0]
        self.cost = int(components[1])
        self.attack = int(components[2])
        self.maxLife = int(components[3])
        self.curLife = int(components[4])
        self.effect = components[5]
        self.selected = (components[6] == 'True')
        self.x = int(components[7])
        self.y = int(components[8])
        self.id = int(components[9])
        self.summoningSickness = (components[10] == 'True')
        self.attackedThisTurn = (components[11] == 'True')
    def __repr__(self):
        string = ''
        for key in self.__dict__:
            string = string + str(self.__dict__[key]) + ':'
        return string
