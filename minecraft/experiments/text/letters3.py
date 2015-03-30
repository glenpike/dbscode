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

def writeText(text, type, pos, zPlane=False, lineSpace=1):
    lines = text.split("\n")
    y = pos.y
    width = 0
    for line in lines:
        pt = makeLine(line, type, point(pos.x, y, pos.z), zPlane)
        y -= pt['h'] + lineSpace
        if width < pt['w']:
            width = pt['w']

    return {'w': width, 'h': pos.y - y }

def makeLine(line, type, pos, zPlane):
    x = pos.x
    y = pos.y
    lineHeight = 0
    letterSpace = 1

    for char in line:
        if ' ' == char:
            x += spaceWidth
        else:
            pt = makeLetter(char, type, point(x, y, pos.z), zPlane)
            if lineHeight < pt['h']:
                lineHeight = pt['h']
            x += pt['w']

        x += letterSpace

    return {'w': x, 'h': lineHeight}

def makeLetter(char, type, pos, zPlane):
    print "char %s", (char)
    letter = None
    try:
       letter = chars[char]
    except KeyError:
       print "char ", char, " does not exist"

    if letter is None:
        letter = chars['A']

    x = pos.x
    y = pos.y
    width = 0
    height = 0
    size = point(1, 1, 1)
    for row in letter:
        for col in row:
            if col == 1:
                if zPlane:
                    box(type, point(pos.z, y, x), size)
                else:
                    box(type, point(x, y, pos.z), size)
            x += 1
        if width < (x - pos.x):
            width = x - pos.x
        x = pos.x
        y -= 1
    # print "letter w ", width, " height ", yPos - y
    return {'w': width, 'h': pos.y - y}

if __name__ == '__main__':
    bulldoze()
    height = 0
    for i in range(0, 10):
        pt = writeText('BABEL', DIAMOND_BLOCK, point(1, height * i, 0), False, 0)
        writeText('BABEL', DIAMOND_BLOCK, point(1, height * i, 0), True, 0)
        writeText('BABEL', DIAMOND_BLOCK, point(1, height * i, pt['w']-1), False, 0)
        writeText('BABEL', DIAMOND_BLOCK, point(1, height * i, pt['w']-1), True, 0)
        height = pt['h']
