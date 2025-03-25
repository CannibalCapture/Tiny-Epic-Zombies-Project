import pygame, os
from .button import Button
from .constants import WIDTH, HEIGHT, roomrects, OFFSETS

class Tank(Button):
    def __init__(self, ID, startCoords, movementOptions=[]):
        super().__init__("tank",  (0,0), True, False)
        self.coords = startCoords
        self.ID = ID
        self.setCoords(self.coords)
        self.movementOptions = movementOptions

    def serialize(self):
        dict = {
            "ID": self.ID,
            "coords": self.coords,
            "movementOptions": self.movementOptions
        }
        return dict

    def deserialize(dict):
        return Tank(dict["ID"], dict["coords"], dict["movementOptions"])

    def load_images(self):
        self.enabled_img = pygame.image.load(os.path.join("TinyEpicZombies", "assets", "tank.png"))
        self.enabled_img = pygame.transform.scale(self.enabled_img, (0.03*WIDTH, 0.08*HEIGHT))
        self.disabled_img = self.enabled_img

    def on_event(self, event):
        if event['type'] == 'PLAYER MOVED':
            if event['moves'] == 0:
                self.disable()
        if event['type'] == 'TURN CHANGE':
            self.enable()

    def onClick(self):
        if not self.enabled:
            return
        else:
            return {"mode":"move tank", "tank":self.ID}

    def setPos(self, pos, offset=[0,0]):
        pos = list(pos)
        pos[1] -= 0.04*HEIGHT
        pos[0] += offset[0]*WIDTH
        pos[1] += offset[1]*HEIGHT
        pos = tuple(pos)
        self.pos = pos
        self.rect.topleft = (self.pos[0], self.pos[1])
        # self.rect.topleft = (self.pos[0] + offset[0]*WIDTH, self.pos[1] + offset[1]*HEIGHT)

    def getPos(self):
        return self.rect.topleft

    def setCoords(self, coords):
        self.coords = coords
        ofs = (0,0)
        for offset in OFFSETS:
            if coords in OFFSETS[offset]:
                ofs = offset
        self.setPos(roomrects[coords[0]][coords[1]], list(ofs))


    def getMovementOptions(self):
        return self.movementOptions
    
    def setMovementOptions(self, val):
        self.movementOptions = val
    
    def getCoords(self):
        return self.coords
    