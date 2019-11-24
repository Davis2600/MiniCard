from tkinter import *
# cmu_112_graphics cited from 
# http://www.cs.cmu.edu/~112/notes/notes-animations-part1.html
from cmu_112_graphics import *

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
                                fill = color, outline = outline)
        canvas.create_text(self.x - (width/2), self.y - (height/2), text = str(self.cost), font = font, fill = 'blue', anchor = 'nw')
        canvas.create_text(self.x, self.y - (3/8) * height, text = self.name, font  = nameFont)
        canvas.create_text(self.x - (width/4), self.y + (height/4), text = str(self.attack), font = font)
        canvas.create_text(self.x + (width/4), self.y + (height/4), text = str(self.curLife), font = font)