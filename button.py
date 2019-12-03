class Button(object):
    def __init__(self, text, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.color = color
        halfWidth = self.width // 2
        halfHeight = self.height // 2        
        self.lowerX = self.x - halfWidth
        self.upperX = self.x + halfWidth
        self.lowerY = self.y - halfHeight
        self.upperY = self.y + halfHeight
    
    def drawButton(self, canvas):
        halfWidth = self.width // 2
        halfHeight = self.height // 2

        canvas.create_rectangle(self.lowerX, self.lowerY, self.upperX, self.upperY, 
                                fill = self.color, width = 6,  outline = 'black')
        canvas.create_text(self.x,self.y, text = self.text, font = 'Helvetica 20')


    def checkClicked(self, x, y):
        if x < self.upperX and x > self.lowerX and y < self.upperY and y > self.lowerY:
            print('True')
            return True
        else:
            print('False')
            return False
