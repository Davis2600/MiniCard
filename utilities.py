
from PIL import Image, ImageFont, ImageDraw, ImageTk

import textwrap

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