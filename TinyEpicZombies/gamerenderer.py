import pygame
import os
from .constants import WIDTH, HEIGHT, peNames, rotations, CW, CH, tlCoords, DISPLAY, roomCoords

class GameRenderer:
    def __init__(self):
        self.gameboardImg = pygame.image.load(os.path.join("TinyEpicZombies", "assets", "woodBackground.jpg")).convert()
        self.gameboardImg = pygame.transform.scale(self.gameboardImg, (WIDTH, HEIGHT))
        self.lst = self._genStoreSurfaces()

    def renderGameScreen(self):
        DISPLAY.fill((0, 0, 0))
        DISPLAY.blit(self.gameboardImg)
        self.renderStores()
        # self.renderMovementOptions()

    def _genStoreSurfaces(self): #  returns a list of store surfaces
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
        for i in range(len(self.lst)):
            DISPLAY.blit(self.lst[i], tlCoords[i])

    def renderMovementOptions(self):
        for store in roomCoords:
            pass
                # pygame.draw.circle(DISPLAY, (0,255,0), (room[0], room[1]), 50)
