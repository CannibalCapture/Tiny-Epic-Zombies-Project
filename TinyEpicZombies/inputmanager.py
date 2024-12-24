from .helperfunctions.deserialisers import deserializeStore
from .helperfunctions.roomrects import genRoomRects

class InputManager:
    def __init__(self):
        pass
        
    def roomCollisions(self, pos):
        print(pos)
        rectsLst = genRoomRects()
        for store in range(0,9):
            for room in range(len(deserializeStore(store)["rooms"])):
                rect = rectsLst[store][room]
                # print(f"({store},{room}): {rect.center}")
                collide = rect.collidepoint(pos)
                if collide:
                    return (store, room)
        return None