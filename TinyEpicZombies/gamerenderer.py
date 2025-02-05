import pygame, os
from .helperfunctions.deserialisers import deserializeStore
from .helperfunctions.roomrects import genRoomRects, genTlCoords
from .listener import Listener
from .map import Map
from .constants import WIDTH, HEIGHT, DISPLAY, CW, CH, COLOURS

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
        self.playerCardShown = True
        self.turn = 0
        self.map = None
        self.opacity = 88
        self.flag = True
        img = pygame.image.load(os.path.join("TinyEpicZombies", "assets", "icons", "ammo.jpg"))
        img = pygame.transform.scale(img, (0.02*WIDTH, 0.02*HEIGHT))
        self.ammo = img
        img = pygame.image.load(os.path.join("TinyEpicZombies", "assets", "icons", "health.png"))
        img = pygame.transform.scale(img, (0.02*WIDTH, 0.03*HEIGHT))
        self.health = img


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
            self.mode = "move"
        if event['type'] == 'PLAYER RANGED' or event['type'] == 'PLAYER MELEE':
            if event['moves'] != 0:
                self.mode = "move"
        if event['type'] == 'OPEN CARD':
            self.playerCardShown = True
        if event['type'] == 'CLOSE CARD':
            self.playerCardShown = False
        if event['type'] == 'PLAYER MOVED':
            if event['moves'] == 0:
                self.mode = None

    def renderGameBoard(self):
        DISPLAY.blit(self.gameboardImg)
        self.__renderStores()
        self.__renderZombies()
        self.__renderPlayers()
        self.__renderPlayerCards()
        self.__renderFoundCards()
        self.__renderButtons()
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
            tl = self.roomRects[coord[0]][coord[1]].topleft # pulls the top left coordinate of the room the player is in. 
            img = pygame.image.load(os.path.join("TinyEpicZombies", "assets", "avatars", f"{player.getCharacter()}.png"))
            img = pygame.transform.scale(img, (0.04*WIDTH, 0.06*HEIGHT))
            DISPLAY.blit(img, tl)

    def __renderFoundCards(self):
        storeID = self.players[self.turn].getCoords()[0] # gets store the player is in. 
        store = self.map.getStores()[storeID]
        try:
            for i in range (len(store.getCards())):
                card = store.getCards()[i]
                pathEnd = card.getImg()
                img = pygame.image.load(os.path.join("TinyEpicZombies", "assets", "cards", pathEnd))
                img = pygame.transform.scale(img, (0.17*WIDTH, 0.4*HEIGHT))
                DISPLAY.blit(img, (0.01*WIDTH, (0.3+(0.1*i))*HEIGHT))
        except:
            pass

    def __renderPlayerCards(self):
        cWidth = 1.6*CW

        if self.playerCardShown:
            player = self.players[self.turn]
            img = player.getImg()
            x, y = WIDTH*(1 - cWidth), 0
            DISPLAY.blit(img, (x, y))
            img = self.ammo

            x += WIDTH*cWidth - WIDTH*cWidth/9.8*(player.getAmmoMissing() + 1)
            y += HEIGHT*0.025
            DISPLAY.blit(img, (x, y))

            img = self.health
            x = WIDTH*(1 - cWidth) + WIDTH*cWidth/9.8*(player.getHealthMissing())
            DISPLAY.blit(img, (x, y))


    def __renderZombies(self):
        zombieRooms = self.map.getZombieRooms()
        for coord in zombieRooms:
            tl = self.roomRects[coord[0]][coord[1]].topleft # pulls the top left coordinate of the room the player is in. 
            img = pygame.image.load(os.path.join("TinyEpicZombies", "assets", "zombie.png"))
            img = pygame.transform.scale(img, (0.03*WIDTH, 0.04*HEIGHT))
            DISPLAY.blit(img, tl)

    def __renderAttackMode(self, turn):
        zombieRooms = self.map.getZombieRooms()
        player = self.players[turn]
        movementOptions = player.getMovementOptions().copy() # .copy() ensures player.movementOptions is passed by value. By reference would alter the player's movement options, allowing them to move to the space they already occupy. 
        movementOptions.append(player.getCoords())
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