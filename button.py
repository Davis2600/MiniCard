from utilities import *
#class for uniform buttons across my project
class Button(object):
    def __init__(self, text, x, y, width, height, smallText = False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        halfWidth = self.width // 2
        halfHeight = self.height // 2        
        self.lowerX = self.x - halfWidth
        self.upperX = self.x + halfWidth
        self.lowerY = self.y - halfHeight
        self.upperY = self.y + halfHeight
        fontsize = 25
        if smallText == True:
            fontsize = 18
        self.textImg = getCustomFontText(text, fontsize, 'white')
    
    def drawButton(self, canvas):
        halfWidth = self.width // 2
        halfHeight = self.height // 2

        canvas.create_rectangle(self.lowerX, self.lowerY, self.upperX, self.upperY, 
                                fill = 'black', width = 6,  outline = 'white')
        #canvas.create_text(self.x,self.y, text = self.text, font = 'Helvetica 20', fill = 'white')
        canvas.create_image(self.x, self.y, image = getCachedPhotoImage(self.textImg))

    def checkClicked(self, x, y):
        if x < self.upperX and x > self.lowerX and y < self.upperY and y > self.lowerY:
            return True
        else:
            return False
