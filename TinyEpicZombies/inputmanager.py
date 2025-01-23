from .helperfunctions.deserialisers import deserializeStore
from .helperfunctions.roomrects import genRoomRects

class InputManager:
    def __init__(self):
        self.lastClickedRoom = None
        self.buttons = []

    def collisions(self, pos):
        dict = {}
        self.buttonCollisions(pos)
        dict["lastClickedRoom"] = self.roomCollisions(pos)
        return dict

    def roomCollisions(self, pos):
        rectsLst = genRoomRects()
        for store in range(0,9):
            for room in range(len(deserializeStore(store)["rooms"])):
                rect = rectsLst[store][room]
                collide = rect.collidepoint(pos)
                if collide:
                    self.lastClickedRoom = (store, room)
                    return self.lastClickedRoom
        self.lastClickedRoom = None  
        return

    def buttonCollisions(self, pos):
        for button in self.buttons:
            if button.getRect().collidepoint(pos):
                button.onClick()
    
    def getLastClickedRoom(self):
        return self.lastClickedRoom
    
    def addButton(self, button):
        self.buttons.append(button)