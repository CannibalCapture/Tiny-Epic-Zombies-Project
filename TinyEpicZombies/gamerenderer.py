import pygame, os
from .helperfunctions.deserialisers import deserializeStore
from .helperfunctions.roomrects import genRoomRects, genTlCoords
from .constants import WIDTH, HEIGHT, DISPLAY, CW, CH

class GameRenderer:
    def __init__(self):
        self.cw = CW*WIDTH
        self.ch = CH*HEIGHT
        self.gameboardImg = pygame.image.load(os.path.join("TinyEpicZombies", "assets", "woodBackground.jpg")).convert()
        self.gameboardImg = pygame.transform.scale(self.gameboardImg, (WIDTH, HEIGHT))
        self.storeSurfaces = self.__genStoreSurfaces()
        self.tlCoords = genTlCoords()
        self.roomRects = genRoomRects()
        self.buttons = []
        self.players = []
        self.opacity = 88
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
    
    def renderGameScreen(self, zombieRooms=None, movementOptions=None, selected=None):
        DISPLAY.blit(self.gameboardImg)
        self.__renderStores()
        self.__renderZombies(zombieRooms)
        self.__renderMovementOptions(movementOptions, selected)
        self.__renderButtons()
        self.__renderPlayers()
    
    def renderMovementOptions(self, coordsLst, selected=None):
        self.__renderMovementOptions(coordsLst)
    
    def __renderPlayers(self):
        for player in self.players:
            coord = player.getCoords()
            rect = self.roomRects[coord[0]][coord[1]]
            surface = pygame.Surface((18,18), pygame.SRCALPHA)
            surface.fill((255,0,0))
            DISPLAY.blit(surface, rect)

    def __renderZombies(self, coordsLst, rect=pygame.Rect):
        for coord in coordsLst:
            rect = self.roomRects[coord[0]][coord[1]]
            surface = pygame.Surface((18,18), pygame.SRCALPHA)
            surface.fill((0,80,0))
            DISPLAY.blit(surface, rect)

    def __renderButtons(self):
        for button in self.buttons:
            img = button.getImg()
            tl = button.getRect().topleft
            DISPLAY.blit(img, (tl))

    def __renderStores(self):
        for store in range(9):
            DISPLAY.blit(self.storeSurfaces[store], self.tlCoords[store])

    def __renderMovementOptions(self, coordsLst, selected=None): # coordsLst are the coordinates available for moving to
        for coord in coordsLst:
            opacity = 80
            if coord == selected:
                opacity = 50
            rect = self.roomRects[coord[0]][coord[1]]

            surface = pygame.Surface((30,30), pygame.SRCALPHA)
            surface.fill((0,0,255, opacity))
            DISPLAY.blit(surface, rect)
    
    def addButton(self, button):
        self.buttons.append(button)

    def addPlayer(self, player):
        self.players.append(player)