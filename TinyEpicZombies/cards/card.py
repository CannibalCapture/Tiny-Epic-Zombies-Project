from ..constants import WIDTH, HEIGHT
import pygame, os

class Card:
    def __init__(self, colour, type, ID, player=None):
        self.colour = colour
        self.type = type
        self.img = None
        self.ID = ID
        self.player = player
        self.rect = self.getImg().get_rect() if self.getImg() else pygame.Rect(0, 0, 0, 0)

    def load_image(self):
        pass

    def setPos(self, pos):
        self.pos = pos
        self.rect = self.getImg().get_rect()
        self.rect.topleft = (self.pos[0]*WIDTH, self.pos[1]*HEIGHT)

    def serialize(self):
        return "no serialise method defined"
    
    def deserialize(dict):
        return "no deserialise method defined"
    
    def getColour(self):
        return self.colour
    
    def getPos(self):
        return self.pos
    
    def getID(self):
        return self.ID

    def getImg(self):
        return self.img
    
    def getImg(self):
        return self.img
    
    def getType(self):
        return self.type
    
    def getRect(self):
        return self.rect