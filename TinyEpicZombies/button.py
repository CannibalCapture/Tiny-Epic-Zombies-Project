import pygame, os
from .helperfunctions.deserialisers import scale
from .constants import WIDTH, HEIGHT

class Button:
    def __init__(self):
        width = 0.05
        height = 0.08
        self.pos = (0.92, 0.87)
        self.img = pygame.image.load(os.path.join("TinyEpicZombies", "assets", "attack.jpg")).convert()
        self.img = pygame.transform.scale(self.img, (WIDTH*width, HEIGHT*height))
        self.rect = self.img.get_rect()
        self.rect.topleft = (self.pos[0]*WIDTH, self.pos[1]*HEIGHT)
    
    def onClick(self):
        print("Clicked")

    def getImg(self):
        return self.img
    
    def getRect(self):
        return self.rect
