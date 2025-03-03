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
        self.load_images()
        self.storeSurfaces = self.__genStoreSurfaces()
        self.tlCoords = genTlCoords()
        self.roomRects = genRoomRects()
        self.buttons = []
        self.players = []
        self.tanks = []
        self.mode = "move"
        self.turn = 0
        self.opacity = 88
        self.player = None
        self.map = None
        self.shownPickupCards = False # contains the store which we will render the pickup cards for
        self.selectedTank = 0
        self.playerCardShown = True
        self.pickupWeaponChoice = False
        self.inventoryShown = False
        self.flag = True

    def load_images(self):
        img = pygame.image.load(os.path.join("TinyEpicZombies", "assets", "woodBackground.jpg")).convert()
        img = pygame.transform.scale(img, (WIDTH, HEIGHT))
        self.gameboardImg = img
        img = pygame.image.load(os.path.join("TinyEpicZombies", "assets", "icons", "ammo.jpg"))
        img = pygame.transform.scale(img, (0.02*WIDTH, 0.02*HEIGHT))
        self.ammo = img
        img = pygame.image.load(os.path.join("TinyEpicZombies", "assets", "icons", "health.png"))
        img = pygame.transform.scale(img, (0.02*WIDTH, 0.03*HEIGHT))
        self.health = img
        img = pygame.image.load(os.path.join("TinyEpicZombies", "assets", "zombie.png"))
        img = pygame.transform.scale(img, (0.03*WIDTH, 0.04*HEIGHT))
        self.zombie = img
        # img = pygame.image.load(os.path.join("TinyEpicZombies", "assets", "tank.png"))
        # img = pygame.transform.scale(img, (0.03*WIDTH, 0.08*HEIGHT))
        # self.tank = img

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
        match event['type']:
            case 'MODE CHANGE':
                self.mode = event['mode']
            case 'TURN CHANGE':
                self.nextTurn(event['turn'])
                self.mode = "move"
            case 'PLAYER RANGED' | 'PLAYER MELEE':
                if event['moves'] != 0:
                    self.mode = "move"
                else:
                    self.mode = None
            case 'OPEN CARD':
                self.playerCardShown = True
            case 'CLOSE CARD':
                self.playerCardShown = False
            case 'PLAYER MOVED' | 'TANK MOVED':
                moves = event['moves']
                if moves == 0:
                    self.mode = None
            case 'SHOW CARDS':
                self.shownPickupCards = event['store']
            case 'EXIT MENU':
                self.pickupWeaponChoice = False
                self.shownPickupCards = None
                self.inventoryShown = False
                self.iCards = []
            case 'PICKUP STORE CARDS':
                self.pickupWeaponChoice = True
                self.shownPickupCards = None
            case 'OPEN INVENTORY':
                self.inventoryShown = True

    def renderGameBoard(self):
        DISPLAY.blit(self.gameboardImg)
        self.__renderStores()
        self.__renderZombies()
        self.__renderTanks()
        self.__renderPlayers()
        self.__renderPlayerCards()
        self.__renderPickupCards()
        self.__renderButtons()
        self.renderOverlay()
        self.__renderPickupWeaponChoice()
        self.__renderInventory()

    def renderOverlay(self):
        if self.mode == "move" or self.mode == "move tank":
            self.__renderMovementOptions(self.turn)
        if self.mode == "attack":
            self.__renderAttackMode(self.turn)

    def addiCard(self, val):
        self.iCards.append(val)
        
    def __renderInventory(self):
        if not self.inventoryShown:
            return
        
        self.__renderMenuShadow()
        self.__renderExitMenuButton()

        cardsLst = self.player.getInventory()
        for i in range(len(cardsLst)):
            card = cardsLst[i]
            img = card.getImg()

            width, height = 0.2, 0.4
            card.setPos((((1-len(cardsLst)*width)/2 + width*i), (0.5-(height/2))))
            pos = card.getPos()
            pos = (pos[0]*WIDTH, pos[1]*HEIGHT)

            DISPLAY.blit(img, pos)
    
    def __renderPlayers(self):
        lst = []
        adj = 0
        for player in self.players:
            coord = player.getCoords()
            adj += (lst.count(coord))
            lst.append(coord)
            tl = self.roomRects[coord[0]][coord[1]].topleft # pulls the top left coordinate of the room the player is in
            tl = (tl[0] + adj*0.008*WIDTH, tl[1])
            img = player.getImg()
            
            DISPLAY.blit(img, tl)


    def __renderPickupCards(self): # Game breaks when the deck runs out of cards currently

        if self.shownPickupCards == None:
            return

        store = self.map.getStores()[self.shownPickupCards]
        if len(store.getCards()) > 0:
            for i in range(len(store.getCards())):
                card = store.getCards()[i]
                img = card.getImg()
                DISPLAY.blit(img, (0.01*WIDTH, (0.3+(0.1*i))*HEIGHT))

    def __renderPlayerCards(self):
        cWidth = 1.6*CW

        if self.playerCardShown:
            player = self.players[self.turn]
            img = player.getCardImg()
            x, y = WIDTH*(1 - cWidth), 0
            DISPLAY.blit(img, (x, y))

            img = self.ammo
            x += WIDTH*cWidth - WIDTH*cWidth/9.8*(player.getAmmoMissing() + 1)
            y += HEIGHT*0.025
            DISPLAY.blit(img, (x, y))

            img = self.health
            x = WIDTH*(1 - cWidth) + WIDTH*cWidth/9.8*(player.getHealthMissing())
            DISPLAY.blit(img, (x, y))

    def __renderMenuShadow(self):
        # Darkening effect on the background
        surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA) 
        surface.fill((0,0,0, 80))
        DISPLAY.blit(surface, (0,0))
    
    def __renderExitMenuButton(self):
        button = self.buttons[5] # rerendering the exit menu button over the menu shadow. 
        img = button.getImg()
        tl = button.getPos()
        DISPLAY.blit(img, (tl[0]*WIDTH, tl[1]*HEIGHT))


    def __renderPickupWeaponChoice(self):
        if not self.pickupWeaponChoice:
            return
        
        self.__renderMenuShadow()

        store = self.map.getStores()[self.player.getCoords()[0]]
        width, height = 0.17, 0.4
        cardCount = len(store.getCards())
        # cardCount = len(self.iCards)

        self.__renderExitMenuButton()

        for i in range(cardCount):
            card = store.getCards()[i]
            # card = self.iCards[i]
            img = card.getImg()

            width = 0.2
            card.setPos((((1-cardCount*width)/2 + width*i), (0.5-(height/2))))
            pos = card.getPos()
            pos = (pos[0]*WIDTH, pos[1]*HEIGHT)

            DISPLAY.blit(img, pos)

    def __renderZombies(self):
        zombieRooms = self.map.getZombieRooms()
        for coord in zombieRooms:
            tl = self.roomRects[coord[0]][coord[1]].topleft # pulls the top left coordinate of the room the player is in. 
            DISPLAY.blit(self.zombie, tl)

    def __renderTanks(self):
        for tank in self.tanks:
            coord = tank.getPos()
            # print(tank.getID(), tank.getRect())
            tl = (coord[0], coord[1]) # pulls the top left coordinate of the room the player is in.
            DISPLAY.blit(tank.getImg(), tl)

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
            tl = button.getPos()
            DISPLAY.blit(img, (tl[0]*WIDTH, tl[1]*HEIGHT))

    def __renderStores(self):
        for store in range(9):
            DISPLAY.blit(self.storeSurfaces[store], self.tlCoords[store])

    def __renderMovementOptions(self, turn): # coordsLst are the coordinates available for moving to
        opacity = 80

        if self.mode == "move tank":
            colour = (0,255,0, opacity)
            selectedEntity = self.tanks[self.selectedTank]
        elif self.mode == "move":
            colour = (0,0,255, opacity)
            selectedEntity = self.players[turn]

        coordsLst = selectedEntity.getMovementOptions()
        for coord in coordsLst:
            rect = self.roomRects[coord[0]][coord[1]]

            surface = pygame.Surface((30,30), pygame.SRCALPHA)

            surface.fill(colour)
            DISPLAY.blit(surface, rect)
    
    def updateBarricade(self, val):
        offset = 0
        for i in range(val):
            pass
            

    def addButton(self, button):
        self.buttons.append(button)

    def addPlayer(self, player):
        self.players.append(player)

    def setSelectedTank(self, tank):
        self.selectedTank = tank

    def nextTurn(self, turn):
        self.turn = turn
        self.player = self.players[turn]
        self.mode = "move"
        self.shownPickupCards = self.player.getCoords()[0]

    def addMap(self, value:Map):
        self.map = value

    def addTank(self, tank):
        self.tanks.append(tank)