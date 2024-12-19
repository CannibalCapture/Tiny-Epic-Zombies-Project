import pygame
import os
from .constants import WIDTH, HEIGHT, peNames, rotations, CW, CH, tlCoords, DISPLAY, roomCoords
from .deserialisers import deserializeCollider

class GameRenderer:
    def __init__(self):
        self.gameboardImg = pygame.image.load(os.path.join("TinyEpicZombies", "assets", "woodBackground.jpg")).convert()
        self.gameboardImg = pygame.transform.scale(self.gameboardImg, (WIDTH, HEIGHT))
        self.storeSurfaces = self.__genStoreSurfaces()

    def renderGameScreen(self):
        DISPLAY.blit(self.gameboardImg)
        self.renderStores()
        self.renderMovementOptions()

    def __genStoreSurfaces(self): #  returns a list of store surfaces
        storeSurfaces = []
        for i in range(9):
            pathEnd = peNames[i]
            rotation = rotations[i]
            img = pygame.image.load(os.path.join("TinyEpicZombies", "assets", "stores", f"{pathEnd}"))
            img = pygame.transform.scale(img, (CW, CH))
            img = pygame.transform.rotate(img, rotation)
            storeSurfaces.append(img)
        return storeSurfaces
    
    def renderStores(self):
        for i in range(len(self.storeSurfaces)):
            DISPLAY.blit(self.storeSurfaces[i], tlCoords[i])

    def renderMovementOptions(self):
        rect = pygame.Rect(50,50,40,40)
        for store in range(0,9):
            for room in range(0,3):
                coords = (store, room)
                points = deserializeCollider(coords)
                tl = ((tlCoords[store][0] + points[0][0]), (tlCoords[store][1] + points[0][1]))
                rect.topleft = tl
                pygame.draw.rect(DISPLAY, (0,0,255), rect)