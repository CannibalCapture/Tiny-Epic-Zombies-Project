import pygame
import numpy as np
from .deserialisers import deserializeRoom, deserializeStore, scale
from ..constants import WIDTH, HEIGHT

def genRoomRects():
    out = []
    sTl = genTlCoords()
    for store in range(0,9):
        out.append([])
        for room in range(len(deserializeStore(store)["rooms"])):
            dRoom = deserializeRoom((store, room))
            rCenter = dRoom["centre"]
            rCenter = np.array(scale(rCenter))
            storeTl = np.array(sTl[store])
            rCenter = tuple(rCenter + storeTl)
            rect = pygame.Rect(0,0, 20, 20)
            rect.center = rCenter
            out[-1].append(rect)
    return out

def genTlCoords():
    lst = []
    for store in range(9):
        lst.append(tuple(np.multiply((WIDTH, HEIGHT), deserializeStore(store)["tl"])))
    return lst