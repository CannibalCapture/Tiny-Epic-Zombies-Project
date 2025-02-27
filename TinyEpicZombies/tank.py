import pygame, os
from .button import Button
from .constants import WIDTH, HEIGHT, roomrects

class Tank(Button):
    def __init__(self, ID, startCoords):
        super().__init__("tank",  (0,0), True, False)
        self.coords = startCoords
        self.ID = ID
        self.setCoords(self.coords)
        self.movementOptions = []

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

    def setPos(self, pos):
        pos = list(pos)
        pos[1] -= 0.04*HEIGHT
        pos = tuple(pos)
        self.pos = pos
        self.rect.topleft = (self.pos[0], self.pos[1])

    def setCoords(self, coords):
        self.coords = coords
        self.setPos(roomrects[coords[0]][coords[1]])

    def getMovementOptions(self):
        return self.movementOptions
    
    def setMovementOptions(self, val):
        self.movementOptions = val
    
    def getCoords(self):
        return self.coords
    