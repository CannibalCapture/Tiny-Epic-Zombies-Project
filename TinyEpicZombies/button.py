import pygame, os
from .helperfunctions.deserialisers import scale
from .constants import WIDTH, HEIGHT
from .eventgenerator import EventGenerator

class Button(EventGenerator):
    def __init__(self):
        width, height = 0.05, 0.08
        self.pos = (0.92, 0.87)
        self.img = pygame.image.load(os.path.join("TinyEpicZombies", "assets", "attack.jpg")).convert()
        self.img = pygame.transform.scale(self.img, (WIDTH*width, HEIGHT*height))
        self.rect = self.img.get_rect()
        self.rect.topleft = (self.pos[0]*WIDTH, self.pos[1]*HEIGHT)
        self.listeners = []
        self.state = False
    
    def onClick(self):
        if self.state:
            event = {'type': 'ATTACK OFF'}
            self.state = False
        else:
            event = {'type': 'ATTACK ON'}
            self.state = True
        self.send_event(event)

    def send_event(self, event):
        for listener in self.listeners:
            listener.on_event(event)


    def getImg(self):
        return self.img
    
    def getRect(self):
        return self.rect
