from tkinter import *
# cmu_112_graphics cited from 
# http://www.cs.cmu.edu/~112/notes/notes-animations-part1.html
from cmu_112_graphics import *

class Card(object):
    fontSizeRatio = 0.3
    nameSizeRatio = 0.15
    cardCount =0
    def __init__(self, name = 'none', cost = 0, stats = (0,0), effect = ''):

        
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
                                fill = color, outline = outline)
        canvas.create_text(self.x - (width/2), self.y - (height/2), text = str(self.cost), font = font, fill = 'blue', anchor = 'nw')
        canvas.create_text(self.x, self.y - (3/8) * height, text = self.name, font  = nameFont)
        canvas.create_text(self.x - (width/4), self.y + (height/4), text = str(self.attack), font = font)
        canvas.create_text(self.x + (width/4), self.y + (height/4), text = str(self.curLife), font = font)

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
   
    def __repr__(self):
        string = ''
        for key in self.__dict__:
            string = string + str(self.__dict__[key]) + ':'
        return string
