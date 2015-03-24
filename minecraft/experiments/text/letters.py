from dbscode_minecraft import  *
from pixelfont_04B_03 import chars

"""
Simple functions to write text in Minecraft

This only works in the x-plane - need to figure out
how to make it directional.

Also uses a "font" which is an object containing a
2D list for each char.  This could be refined
to generate the characters on the fly and
with varying sizes, but the font object is quite
a nice thing for learners to see.
"""
spaceWidth = 4;

def writeText(text, type, xPos, yPos, zPos):
    lines = text.split("\n")
    x = xPos
    y = yPos
    lineSpace = 1
    for line in lines:
        pt = makeLine(line, type, x, y, zPos)
        y -= pt['h'] + lineSpace

    return pt

def makeLine(line, type, xPos, yPos, zPos):
    x = xPos
    y = yPos
    lineHeight = 0
    letterSpace = 1

    for char in line:
        if ' ' == char:
            x += spaceWidth
        else:
            pt = makeLetter(char, type, x, y, zPos)
            if lineHeight < pt['h']:
                lineHeight = pt['h']
            x += pt['w']

        x += letterSpace

    return {'w': x, 'h': lineHeight}

def makeLetter(char, type, xPos, yPos, zPos):
    print "char %s", (char)
    letter = None
    try:
       letter = chars[char]
    except KeyError:
       print "char ", char, " does not exist"

    if letter is None:
        letter = chars['A']
    x = xPos
    y = yPos
    width = 0
    height = 0
    size = point(1, 1, 1)
    for row in letter:
        for col in row:
            if col == 1:
                box(type, point(x, y, zPos), size)
            x += 1
        if width < (x - xPos):
            width = x - xPos
        x = xPos
        y -= 1
    # print "letter w ", width, " height ", yPos - y
    return {'w': width, 'h': yPos - y}

if __name__ == '__main__':
    bulldoze()
    writeText('SKI IS ACE', DIAMOND_BLOCK, 0, 10, 0)
