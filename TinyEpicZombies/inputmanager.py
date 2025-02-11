from .helperfunctions.deserialisers import deserializeStore
from .helperfunctions.roomrects import genRoomRects
from .listener import Listener

class InputManager(Listener):
    def __init__(self):
        self.lastClickedRoom = None
        self.buttons = []
        self.mode = "NORMAL"

    def collisions(self, pos):
        if self.mode == "NORMAL":
            dict = {"mode": None, "lastClickedRoom": None, 'type': None}
            buttonReturn, lcr = self.buttonCollisions(pos), self.roomCollisions(pos)
            dict = dict | lcr | buttonReturn
            return dict
        elif self.mode == "":
            pass

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
        dict["lastClickedRoom"] = None
        return dict

    def buttonCollisions(self, pos): # Executes onClick methods for all pressed buttons and returns the state of any button which has just been pressed. 
        for button in self.buttons:
            if button.getRect().collidepoint(pos):
                mode = button.onClick() # if a button is clicked and returns a change in mode, this function will return which mode has been returned. 
                if mode:
                    return mode
        return {}
    
    def getLastClickedRoom(self):
        return self.lastClickedRoom
    
    def addButton(self, button):
        self.buttons.append(button)