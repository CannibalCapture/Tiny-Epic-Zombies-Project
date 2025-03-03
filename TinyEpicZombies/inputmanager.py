from .helperfunctions.deserialisers import deserializeStore
from .helperfunctions.roomrects import genRoomRects
from .listener import Listener
from .map import Map

class InputManager(Listener):
    def __init__(self):
        self.lastClickedRoom = None
        self.buttons = []
        self.tanks = []
        self.player = None
        self.map = None
        self.mode = "NORMAL"

    def on_event(self, event):
        if event['type'] == 'PICKUP STORE CARDS':
            self.mode = "PICKUP"
        if event['type'] == 'TURN CHANGE':
            self.player = event['player']
        if event['type'] == 'EXIT MENU':
            self.mode = "NORMAL"

    def collisions(self, pos):
        dict = {}
        if self.mode == "NORMAL":
            buttonReturn, lcr, tankCollisions = self.buttonCollisions(pos), self.roomCollisions(pos), self.tankCollisions(pos)
            dict = dict | lcr | buttonReturn | tankCollisions
        elif self.mode == "PICKUP":
            buttonReturn, cardColl = self.buttonCollisions(pos), self.cardCollisions(pos)
            dict = buttonReturn | cardColl
        return dict

    def roomCollisions(self, pos): # returns last clicked room's coordinates
        rectsLst = genRoomRects()
        dict = {}
        for store in range(0,9):
            for room in range(len(deserializeStore(store)["rooms"])):
                rect = rectsLst[store][room]
                collide = rect.collidepoint(pos)
                if collide:
                    lastClickedRoom = (store, room)
                    dict["lastClickedRoom"] = lastClickedRoom
                    return dict
        return dict

    def buttonCollisions(self, pos): # Executes onClick methods for all pressed buttons and returns the state of any button which has just been pressed. 
        for button in self.buttons:
            if button.getRect().collidepoint(pos):
                mode = button.onClick() # if a button is clicked and returns a change in mode, this function will return which mode has been returned. 
                if mode:
                    return mode
        return {}
    
    def tankCollisions(self, pos):
        output = {}
        for tank in self.tanks:
            if tank.getRect().collidepoint(pos):
                output = tank.onClick()
        
        return output
    
    def cardCollisions(self, pos):
        store = self.map.getStores()[self.player.getCoords()[0]]
        cardCount = len(store.getCards())
        cards = store.getCards()
        out = {}
        for i in range(cardCount):
            card = cards[i]
            if card.getRect().collidepoint(pos):
                out["lastClickedCard"] = card
        return out

    def getLastClickedRoom(self):
        return self.lastClickedRoom
    
    def addButton(self, button):
        self.buttons.append(button)

    def addTank(self, tank):
        self.tanks.append(tank)

    def addMap(self, value:Map):
        self.map = value