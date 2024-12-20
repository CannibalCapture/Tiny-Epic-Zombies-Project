import pygame
import numpy as np
from .deserialisers import deserializeRoom, deserializeTl

def genRoomRects():
    out = []
    for store in range(0,9):
        out.append([])
        for room in range(0,3):
            screenCoords = deserializeRoom((store, room))["collider"]
            storeTl = deserializeTl(store)
            tl, br = tuple(screenCoords[0]), tuple(screenCoords[1])
            rect = pygame.Rect(0,0,20,20)
            rect.topleft = tl
            rect.bottomright = br
            out[-1].append(rect)
    return out
