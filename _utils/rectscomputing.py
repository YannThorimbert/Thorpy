"""Old and not used"""

from pygame import Rect


def get_rel_pos_topleft(parent, child):
    dx = child.x - parent.x
    dy = child.y - parent.y
    return (dx, dy)


def getRectsSizes(rects):
    r = list([])
    for rect in rects:
        r.append(Rect((0,0), rect.size))
    return r

def getRectsSizes2(rects):
    r = list([])
    for rect in rects:
        r.append(Rect((0,0), rect.size))
    return r

def centerRect(fixed, toMove):
    toMove.center = fixed.center

def add(r1, r2):
    return Rect(r1.x + r2.x, r1.y + r2.y)

def getCorners(r):
    return [r.topleft, r.topright, r.bottomleft, r.bottomright]

def cut_static(home, visitor):
    if not home.colliderect(visitor):
        return []
    #left
    w = visitor.left - home.left
    left = Rect(home.topleft, (w,home.h))
    #right
    w = home.right - visitor.right
    x = visitor.right
    right = Rect((x,home.top), (w,home.h))
    #top
    h = visitor.top - home.top
    x = visitor.left
    top = Rect((x,home.top), (visitor.w, h))
    #bottom
    h = home.bottom - visitor.bottom
    bottom = Rect(visitor.bottomleft, (visitor.w, h))

    parts = [left, right, top, bottom]
    toReturn = []
    for part in parts:
        if part.w > 0 and part.h > 0:
            toReturn.append(part)
    return toReturn

def rectSet(rectList):
    """Returns a list of rect without doublons"""
    toReturn = []
    for rect in rectList:
        if rect not in toReturn:
            toReturn.append(rect)
    return toReturn

def sameCorners(r1, r2):
    """Returns number of corners shared"""
    counter = 0
    for corner1 in getCorners(r1):
        for corner2 in getCorners(r2):
            if corner1 == corner2:
                counter += 1
    return counter

def sameDimensions(r1, r2):
    return (r1.w == r2.w) + (r1.h == r2.h)

def get_top_coords(rect):
    bottomleft = (rect.left, rect.bottom-2)
    topleft = (rect.left, rect.top)
    topright = (rect.right-1, rect.top)
    return (bottomleft,topleft, topright)

def get_bottom_coords(rect):
    bottomleft = (rect.left, rect.bottom-1)
    bottomright = (rect.right-1, rect.bottom-1)
    topright = (rect.right-1, rect.top)
    return (bottomleft, bottomright, topright)

##ALIGNEMENTS##

def alignV(elements, value):
    for elt in elements:
        elt.center = (value, elt.centery)

def alignLeft(elements, value):
    for elt in elements:
        elt.topleft = (value, elt.top)

def alignRight(elements, value):
    for elt in elements._elements:
        elt.topright = (value, elt.top)

def alignH(elements, value):
    for elt in elements:
        elt.center = (elt.centerx, value)

def alignTop(elements, value):
    for elt in elements:
        elt.topleft = (elt.left, value)

def alignBottom(elements, value):
    for elt in elements:
        elt.bottomleft = (elt.left, value)

def spaceX(elements, x0=-5, gap=5):
    """Changes the horizontal coordinates of all <elements> to make them
    spaced of <gap> each other, beginning at <x0> coordinate"""
    previousX = x0
    for elt in elements:
        elt.left = previousX + gap
        previousX = elt.right

def spaceY(elements, y0=-5, gap=5):
    """Changes the vertical coordinates of all <elements> to make them
    spaced of <gap> each other, beginning at <y0> coordinate"""
    previousY = y0
    for elt in elements:
        elt.top = previousY + gap
        previousY = elt.bottom
