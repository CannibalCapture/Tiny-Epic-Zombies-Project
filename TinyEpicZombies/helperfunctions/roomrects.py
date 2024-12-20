import pygame
import numpy as np
from .deserialisers import deserializeRoom, deserializeStore
from ..constants import WIDTH, HEIGHT

def genRoomRects():
    out = []
    sTl = genTlCoords()
    for store in range(0,9):
        out.append([])
        for room in range(0,3):
            screenCoords = deserializeRoom((store, room))["collider"]
            storeTl = np.array(sTl[store])
            screenCoords[0], screenCoords[1] = np.array(screenCoords[0]), np.array(screenCoords[1])
            tl = tuple(screenCoords[0] + storeTl)
            br = tuple(screenCoords[1] + storeTl)
            rect = pygame.Rect(0,0,20,20)
            rect.topleft = tl
            rect.bottomright = br
            out[-1].append(rect)
    return out

def genTlCoords():
    lst = []
    for store in range(9):
        lst.append(tuple(np.multiply((WIDTH, HEIGHT), deserializeStore(store)["tl"])))
    return lst