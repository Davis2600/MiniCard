
from PIL import Image, ImageFont, ImageDraw, ImageTk

import textwrap
import requests
from io import BytesIO
# Cited From http://code.activestate.com/recipes/580778-tkinter-custom-fonts/
# Heavily modified to integrate easily into my program
def getCustomFontText( text, size, fill = 'black'):
    fontPath = 'ARCADECLASSIC.TTF'
    truetypeFont = ImageFont.truetype(fontPath, size)
    width, height = truetypeFont.getsize(text)
    image = Image.new('RGBA', (width, height), color = (0,0,0,0))
    draw = ImageDraw.Draw(image)
    draw.text((0,0), text, font = truetypeFont, fill = fill)
    return image
    
#cited from https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html
def getCachedPhotoImage(image):
    # stores a cached version of the PhotoImage in the PIL/Pillow image
    if ('cachedPhotoImage' not in image.__dict__):
        image.cachedPhotoImage = ImageTk.PhotoImage(image)
    return image.cachedPhotoImage

# loadImage cited from 
# http://www.cs.cmu.edu/~112/notes/notes-animations-part1.html
#heavily modified  
def loadImage(path=None):
    if (path.startswith('http')):
        response = requests.request('GET', path) # path is a URL!
        image = Image.open(BytesIO(response.content))
    else:
        image = Image.open(path)
    return image
cardImageDict = {}
def buildCardDict():
    global cardImageDict
    newtUrl = 'https://i.imgur.com/AuipiOJ.png'
    newtImg = loadImage(newtUrl)
    pallyUrl = 'https://i.imgur.com/ZHWGAmq.png'
    pallyImg = loadImage(pallyUrl)
    minionUrl = 'https://i.imgur.com/xgAWpHJ.png'
    minionImg = loadImage(minionUrl)
    dragonUrl = 'https://i.imgur.com/aXXrvYG.png'
    dragonImg = loadImage(dragonUrl)
    beastUrl = 'https://i.imgur.com/0D7jBmu.png'
    beastImg = loadImage(beastUrl)
    lancerUrl = 'https://i.imgur.com/sRLEuLz.png'
    lancerImg = loadImage(lancerUrl)
    wizardUrl = 'https://i.imgur.com/2lUyb1i.png'
    wizardImg = loadImage(wizardUrl)
    houndUrl = 'https://i.imgur.com/ijXonUT.png'
    houndImg = loadImage(houndUrl)
    trollUrl = 'https://i.imgur.com/euXFjui.png'
    trollImg = loadImage(trollUrl)
    mummyUrl = 'https://i.imgur.com/ZwhCQuS.png'
    mummyImg = loadImage(mummyUrl)
    squidUrl = 'https://i.imgur.com/oVk4QuU.png'
    squidImg = loadImage(squidUrl)
    witchUrl = 'https://i.imgur.com/nHI0UFf.png'
    witchImg = loadImage(witchUrl)
    cardImageDict = {
        'Newt': newtImg,
        'Pally': pallyImg, 
        'Minion': minionImg,
        'Hound': houndImg,
        'Troll': trollImg,
        'Beast': beastImg,
        'Dragon': dragonImg,
        'Squid': squidImg,
        'Lancer':lancerImg,
        'Wizard': wizardImg,
        'Mummy': mummyImg,
        'Witch': witchImg,
    }

#cardImages are created and stored here to avoid confusion
def getCardImage(cardName):

    if cardName not in cardImageDict:
        return None
    return cardImageDict[cardName]
