from .card import Card
import pygame, os
from ..constants import WIDTH, HEIGHT

# Implement events for listeners?

class Crowbar(Card):
    def __init__(self, colour):
        super().__init__(colour, "MELEE WEAPON", "crowbar")

    def load_image(self):
        width, height = 0.17, 0.4
        img = pygame.image.load(os.path.join("TinyEpicZombies", "assets", "cards", "crowbar.jpg"))
        img = pygame.transform.scale(img, (width*WIDTH, height*HEIGHT))
        self.img = img

    def validateCrowbarMove(self, coords): # Needs to be updated to ensure the store moved to is adjacent. 
        if coords[1] == 0: # Ensures player is moving to an entrance room. 
            return True
        return False
    

class golfClub(Card):
    def __init__(self, colour):
        super().__init__(colour, "MELEE WEAPON", "golfClub")
        self.load_image()

    def load_image(self):
        width, height = 0.17, 0.4
        img = pygame.image.load(os.path.join("TinyEpicZombies", "assets", "cards", "golfClub.jpg"))
        img = pygame.transform.scale(img, (width*WIDTH, height*HEIGHT))
        self.img = img
# Add a ranged weapon