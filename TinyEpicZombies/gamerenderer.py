import pygame, os
from .helperfunctions.deserialisers import deserializeStore
from .helperfunctions.roomrects import genRoomRects, genTlCoords
from .constants import WIDTH, HEIGHT, DISPLAY, CW, CH
from .adjlist import AdjList

class GameRenderer:
    def __init__(self):
        self.cw = CW*WIDTH
        self.ch = CH*HEIGHT
        self.gameboardImg = pygame.image.load(os.path.join("TinyEpicZombies", "assets", "woodBackground.jpg")).convert()
        self.gameboardImg = pygame.transform.scale(self.gameboardImg, (WIDTH, HEIGHT))
        self.storeSurfaces = self.__genStoreSurfaces()
        self.tlCoords = genTlCoords()
        self.roomRects = genRoomRects()
        self.opacity = 50
        self.flag = True

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
    

    def renderGameScreen(self, coordsLst):
        DISPLAY.blit(self.gameboardImg)
        self.__renderStores()
        self.__renderMovementOptions(coordsLst)

    def __renderStores(self):
        for store in range(9):
            DISPLAY.blit(self.storeSurfaces[store], self.tlCoords[store])

    def __renderMovementOptions(self, coordsLst, selected=None):
        if self.flag:
            self.opacity += 2
        else:
            self.opacity -= 2
        
        if self.opacity > 240:
            self.flag = False
        elif self.opacity < 5:
            self.flag = True

        for item in coordsLst:
            store, room = item[0], item[1]
            rect = self.roomRects[store][room]

            surface = pygame.Surface((30,30), pygame.SRCALPHA)
            surface.fill((0,255,0, self.opacity))
            DISPLAY.blit(surface, rect)
            # pygame.display.flip()

            # pygame.draw.rect(DISPLAY, (0,0,255), rect)