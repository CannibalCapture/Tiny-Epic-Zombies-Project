import pygame, os
from .helperfunctions.deserialisers import deserializeStore
from .helperfunctions.roomrects import genRoomRects, genTlCoords
from .listener import Listener
from .map import Map
from .constants import WIDTH, HEIGHT, DISPLAY, CW, CH

class GameRenderer(Listener):
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
        self.mode = "move"
        self.turn = 0
        self.map = None
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
    
    def on_event(self, event):
        if event['type'] == 'MODE CHANGE':
            self.mode = event['mode']
        if event['type'] == 'TURN CHANGE':
            self.turn = event['turn']
        if event['type'] == 'PLAYER RANGED' or event['type'] == 'PLAYER MELEE':
            self.mode = "move"

    # def renderGameScreen(self, movementOptions=None, selected=None):
    #     zombieRooms = self.map.getZombieRooms()
    #     if self.mode == "attack":
    #         self.__renderAttackMode(zombieRooms, movementOptions)
    #     else:
    #         self.__renderMovementOptions(movementOptions, selected)

    def renderGameBoard(self):
        DISPLAY.blit(self.gameboardImg)
        self.__renderStores()
        self.__renderZombies()
        self.__renderButtons()
        self.__renderPlayers()
        self.renderOverlay()

    def addMap(self, value:Map):
        self.map = value

    def renderOverlay(self):
        if self.mode == "move":
            self.__renderMovementOptions(self.turn)
        if self.mode == "attack":
            self.__renderAttackMode(self.turn)
    
    def __renderPlayers(self):
        for player in self.players:
            coord = player.getCoords()
            rect = self.roomRects[coord[0]][coord[1]]
            surface = pygame.Surface((18,18), pygame.SRCALPHA)
            surface.fill((255,0,0))
            DISPLAY.blit(surface, rect)
        
    def __renderPlayerCard(self):
        ammo = pygame.image.load(os.path.join("TinyEpicZombies", "assets", "ammo.jpg"))
        health = pygame.image.load(os.path.join("TinyEpicZombies", "assets", "health.jpg"))
        # show the whole player card

    def __renderZombies(self):
        zombieRooms = self.map.getZombieRooms()
        for coord in zombieRooms:
            rect = self.roomRects[coord[0]][coord[1]]
            rect = rect.scale_by(0.5)
            surface = pygame.Surface((15,15), pygame.SRCALPHA)
            surface.fill((0,80,0))
            DISPLAY.blit(surface, rect)

    def __renderAttackMode(self, turn):
        zombieRooms = self.map.getZombieRooms()
        player = self.players[turn]
        movementOptions = player.getMovementOptions()
        # ask james about the below (rendering an attack box over zombie in room w/ player)
        # print(movementOptions)
        # movementOptions.insert(0, player.getCoords())
        # print(movementOptions)
        for coord in movementOptions:
            if coord in zombieRooms:
                rect = self.roomRects[coord[0]][coord[1]]
                surface = pygame.Surface((30,30), pygame.SRCALPHA)
                surface.fill((255,0,0, 80))
                DISPLAY.blit(surface, rect)

    def __renderButtons(self):
        for button in self.buttons:
            img = button.getImg()
            tl = button.getRect().topleft
            DISPLAY.blit(img, (tl))

    def __renderStores(self):
        for store in range(9):
            DISPLAY.blit(self.storeSurfaces[store], self.tlCoords[store])

    def __renderMovementOptions(self, turn): # coordsLst are the coordinates available for moving to
        coordsLst = self.players[turn].getMovementOptions()
        for coord in coordsLst:
            opacity = 80
            rect = self.roomRects[coord[0]][coord[1]]

            surface = pygame.Surface((30,30), pygame.SRCALPHA)

            surface.fill((0,0,255, opacity))
            DISPLAY.blit(surface, rect)

    def addButton(self, button):
        self.buttons.append(button)

    def addPlayer(self, player):
        self.players.append(player)