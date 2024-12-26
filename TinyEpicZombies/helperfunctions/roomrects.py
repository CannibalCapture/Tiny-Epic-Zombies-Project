import pygame
import numpy as np
from .deserialisers import deserializeRoom, deserializeStore, scale

def genRoomRects():
    out = []
    sTl = genTlCoords() # storeTopLeft
    for store in range(0,9):
        out.append([])
        for room in range(len(deserializeStore(store)["rooms"])):
            dRoom = deserializeRoom((store, room)) # deserializedRoom - contains dict with the information from deserialization.
            rCenter = dRoom["centre"] # the point which will become the center of the rendered shape for the room. 
            rCenter = np.array(scale(rCenter))
            storeTl = np.array(sTl[store])
            rCenter = tuple(rCenter + storeTl)
            rect = pygame.Rect(0,0, 30, 30)
            rect.center = rCenter
            out[-1].append(rect)
    return out

def genTlCoords():
    lst = []
    for store in range(9):
        lst.append(scale(deserializeStore(store)["tl"]))
    return lst