import pygame, os
import numpy as np
from .constants import CW, CH
from .helperfunctions.deserialisers import deserializeStore
from .helperfunctions.roomrects import genRoomRects, genTlCoords
from .constants import WIDTH, HEIGHT, DISPLAY

class GameRenderer:
    def __init__(self):
        self.cw = CW*WIDTH
        self.ch = CH*HEIGHT
        self.gameboardImg = pygame.image.load(os.path.join("TinyEpicZombies", "assets", "woodBackground.jpg")).convert()
        self.gameboardImg = pygame.transform.scale(self.gameboardImg, (WIDTH, HEIGHT))
        self.storeSurfaces = self.__genStoreSurfaces()
        self.tlCoords = genTlCoords()

    def __genStoreSurfaces(self): #  returns a list of store surfaces
        storeSurfaces = []
        for store in range(9):
            info = deserializeStore(store)
            pathEnd = info["image"]
            rotation = info["rotation"]
            img = pygame.image.load(os.path.join("TinyEpicZombies", "assets", "stores", f"{pathEnd}"))
            img = pygame.transform.scale(img, (self.cw, self.ch))
            img = pygame.transform.rotate(img, rotation)
            storeSurfaces.append(img)
        return storeSurfaces
    

    def renderGameScreen(self):
        DISPLAY.blit(self.gameboardImg)
        self.__renderStores()
        self.__renderMovementOptions()

    def __renderStores(self):
        for store in range(9):
            DISPLAY.blit(self.storeSurfaces[store], self.tlCoords[store])

    def __renderMovementOptions(self):
        roomsLst = genRoomRects()
        rect = pygame.Rect(50,50,40,40)
        for store in range(0,9):
            for room in range(len(deserializeStore(store)["rooms"])):
                rect = roomsLst[store][room]
                pygame.draw.rect(DISPLAY, (0,0,255), rect)