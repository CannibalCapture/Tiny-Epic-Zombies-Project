import pygame, os
from .helperfunctions.deserialisers import scale
from .constants import WIDTH, HEIGHT
from .eventgenerator import EventGenerator

class Button(EventGenerator):
    def __init__(self):
        pass

    def getImg(self):
        return self.img
    
    def getRect(self):
        return self.rect

    def getState(self):
        return self.state

    def setState(self, value):
        self.state = value

class AttackButton(Button):
    def __init__(self):
        self.pos = (0.92, 0.87)
        self.listeners = []
        self.enabled = True
        self.state = False
        self.updateImg()
        self.rect = self.img.get_rect()
        self.rect.topleft = (self.pos[0]*WIDTH, self.pos[1]*HEIGHT)

    def onClick(self):
        if self.enabled == False:
            return
        
        if self.state == True:
            event = {'type': 'ATTACK OFF'}
            self.state = False
        else:
            event = {'type': 'ATTACK ON'}
            self.state = True
        self.send_event(event)

    def disable(self):
        self.enabled = False
        self.updateImg()

    def enable(self):
        self.enabled = True
        self.updateImg()

    def updateImg(self):
        width, height = 0.05, 0.08 # maybe put in json file
        self.img = pygame.image.load(os.path.join("TinyEpicZombies", "assets", f"attack{self.enabled}.png"))
        self.img = pygame.transform.scale(self.img, (WIDTH*width, HEIGHT*height))
    
    def getEnabled(self):
        return self.enabled
