from .helperfunctions.deserialisers import deserializeStore
from .helperfunctions.roomrects import genRoomRects

class InputManager:
    def __init__(self):
        self.lastClickedRoom = None

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
        return self.lastClickedRoom
    
    def getLastClickedRoom(self):
        return self.lastClickedRoom