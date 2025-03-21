from .card import Card
import pygame, os
from ..constants import WIDTH, HEIGHT

class Adrenaline(Card):
    def __init__(self, colour):
        super().__init__(colour, "BACKPACK ITEM", "adrenaline")
        self.load_image()
    
    def load_image(self):
        width, height = 0.17, 0.4
        img = pygame.image.load(os.path.join("TinyEpicZombies", "assets", "cards", "adrenaline.jpg"))
        img = pygame.transform.scale(img, (width*WIDTH, height*HEIGHT))
        self.img = img