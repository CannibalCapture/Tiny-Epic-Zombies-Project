# from .helperfunctions.deserialisers import deserializeCollider
from .helperfunctions.roomrects import genRoomRects

class InputManager:
    def __init__(self):
        pass
        
    def roomCollisions(self, pos):
        for store in range(9):
            for room in range(3):
                coords = (store, room)
                # screenCoords = deserializeCollider(coords)
                # tl, br = tuple(screenCoords[0]), tuple(screenCoords[1])
                # rect = pygame.Rect(topleft=tl, bottomright=br)
                rectsLst = genRoomRects()
                rect = rectsLst[store][room]
                collide = rect.collidepoint(pos)
                # if collide:
                #     print(f"collision with {coords}")
                # else:
                #     print(f"no collision at {pos}")