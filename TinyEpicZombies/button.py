import pygame, os
from .helperfunctions.deserialisers import scale
from .constants import WIDTH, HEIGHT
from .eventgenerator import EventGenerator
from .listener import Listener

class Button(EventGenerator, Listener):
    def __init__(self):
        pass

    def disable(self):
        self.enabled = False
        self.state = False
        self.updateImg()

    def enable(self):
        self.enabled = True
        self.updateImg()

    def on_event(self, event):
        if event['type'] == 'MODE CHANGE' and event['mode'] != self.ID:
            self.state = False
    
    def onClick(self):
        pass

    def updateImg():
        pass

    def getImg(self):
        return self.img
    
    def getRect(self):
        return self.rect

    def getState(self):
        return self.state
    
    def getID(self):
        return self.ID

    def setState(self, value):
        self.state = value

class AttackButton(Button):
    def __init__(self):
        self.pos = (0.92, 0.87)
        self.listeners = []
        self.enabled = True
        self.state = False
        self.ID = "attack"
        self.updateImg()
        self.rect = self.img.get_rect()
        self.rect.topleft = (self.pos[0]*WIDTH, self.pos[1]*HEIGHT)

    def onClick(self):
        if not self.enabled:
            return
        else:
            if self.state:
                self.state = False
                return None
            else:
                self.state = True
                return "attack"

    def on_event(self, event):
        if event['type'] == 'PLAYER MELEE' or event['type'] == 'PLAYER RANGED':
            self.disable()
        elif event['type'] == 'PLAYER MOVED':
            self.enable()
        super().on_event(event)

    def updateImg(self):
        width, height = 0.05, 0.08 # maybe put in json file
        if self.enabled:
            self.img = pygame.image.load(os.path.join("TinyEpicZombies", "assets", "buttons", "attackTrue.png"))
        else:
            self.img = pygame.image.load(os.path.join("TinyEpicZombies", "assets","buttons", "attackFalse.png"))

        self.img = pygame.transform.scale(self.img, (WIDTH*width, HEIGHT*height))
    
    def getEnabled(self):
        return self.enabled

class MoveButton(Button):
    def __init__(self):
        self.pos = (0.84, 0.87)
        self.listeners = []
        self.enabled = True
        self.state = False
        self.ID = "move" # the mode which the button represents
        self.updateImg()
        self.rect = self.img.get_rect()
        self.rect.topleft = (self.pos[0]*WIDTH, self.pos[1]*HEIGHT)
    
    def updateImg(self):
        width, height = 0.05, 0.08 # maybe put in json file
        if self.enabled:
            self.img = pygame.image.load(os.path.join("TinyEpicZombies", "assets", "buttons", "healthTrue.png"))
        else:
            self.img = pygame.image.load(os.path.join("TinyEpicZombies", "assets", "buttons", "healthFalse.png"))

        self.img = pygame.transform.scale(self.img, (WIDTH*width, HEIGHT*height))
    
    def onClick(self):
        if not self.enabled:
            return
        else:
            if self.state:
                self.state = False
                return None
            else:
                self.state = True
                return self.ID