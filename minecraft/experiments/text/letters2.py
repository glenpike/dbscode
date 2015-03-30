from dbscode_minecraft import  *
from pixelfont_04B_03 import chars
from matrix import R_2vect
from numpy import matrix, array, zeros, int8

"""
Simple functions to write text in Minecraft

Also uses a "font" which is an object containing a
2D list for each char.  This could be refined
to generate the characters on the fly and
with varying sizes, but the font object is quite
a nice thing for learners to see.
"""
spaceWidth = 4;

#These are the default horizontal and vertical directions
#for text...
defaultH = array([1, 0, 0], int)
defaultV =  array([0, -1, 0], int)
rotH = None
rotV = None
rotEqual = False

def calculateRotations(h, v):
    global defaultH, defaultV, rotH, rotV

    #Check that h and v are not equal (they must be orthoganal)
    newH = array(h, int)
    newV =  array(v, int)

    #if (newH == defaultH).all() && (newV == defaultV).all():
        #reset the matrices to identity?

    rotH = zeros(shape=(3,3), dtype=int8)
    rotV = zeros(shape=(3,3), dtype=int8)

    R_2vect(rotH, defaultH, newH);
    R_2vect(rotV, defaultV, newV);

    rotEqual = (rotH == rotV).all()
    print "rotH\n", rotH, "\nrotV\n", rotV
    print "Rotation matrices are same? ", rotEqual

def writeText(text, type, pos, h, v):
    calculateRotations(h, v)
    lines = text.split("\n")
    y = pos.y
    lineSpace = 1
    for line in lines:
        pt = makeLine(line, type, point(pos.x, y, pos.z))
        y -= pt['h'] + lineSpace

    return pt

def makeLine(line, type, pos):
    x = pos.x
    y = pos.y
    lineHeight = 0
    letterSpace = 1

    for char in line:
        if ' ' == char:
            x += spaceWidth
        else:
            pt = makeLetter(char, type, point(x, y, pos.z))
            if lineHeight < pt['h']:
                lineHeight = pt['h']
            x += pt['w']

        x += letterSpace

    return {'w': x, 'h': lineHeight}

def makeLetter(char, type, pos):
    global rotH, rotV, rotEqual

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
    z = pos.z
    width = 0
    height = 0
    size = point(1, 1, 1)
    for row in letter:
        for col in row:
            if col == 1:
                #We rotate the coordinates with our matrix
                localPos = array([x, y, z], int)
                rotPos = None
                if rotEqual == True:
                    rotPos = rotH.dot(localPos)
                else:
                    rotPos = rotV.dot(rotH.dot(localPos))
                print "x ", x, " y ", y, " rot ", rotPos
                box(type, point(rotPos[0], rotPos[1], rotPos[2]), size)
            x += 1
        if width < (x - pos.x):
            width = x - pos.x
        x = pos.x
        y -= 1
    # print "letter w ", width, " height ", yPos - y
    return {'w': width, 'h': pos.y - y}

if __name__ == '__main__':
    bulldoze()
    #directions match default
    writeText('SKI', GOLD_BLOCK, point(0, 10, 0), [1, 0, 0], [0, -1, 0])
    #lying down text - works
    writeText('SKI', MELON, point(0, 0, 0), [1, 0, 0], [0, 0, 1])
    #going into the picture - wrong, it flips it on the "x-axis" too
    writeText('SKI', DIAMOND_BLOCK, point(10, -10, 0), [0, 0, 1], [0, 1, 0])
