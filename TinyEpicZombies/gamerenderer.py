import pygame
import os
from .constants import WIDTH, HEIGHT, peNames, rotations, CW, CH, tlCoords, DISPLAY

class GameRenderer:
    def __init__(self): # maybe use a dictionary to return buttons and images to main. {"button":pygame_gui.elements.UIButton...}
        self.gameboardImg = pygame.image.load(os.path.join("TinyEpicZombies", "assets", "woodBackground.jpg")).convert()
        self.gameboardImg = pygame.transform.scale(self.gameboardImg, (WIDTH, HEIGHT))
        self.lst = self._genStoreSurfaces()

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

    def renderGameScreen(self):
        DISPLAY.fill((0, 0, 0))
        DISPLAY.blit(self.gameboardImg)
        self.renderStores()
