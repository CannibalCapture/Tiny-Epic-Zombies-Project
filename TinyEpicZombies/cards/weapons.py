from .card import MeleeWeapon, RangedWeapon
from ..assets.weapons import *
from ..listener import Listener

# Implement events for listeners into a weapons factory class. 

class Crowbar(MeleeWeapon):
    def __init__(self, image=""):
        super().__init__()
        self.image = "crowbar.jpg"

    def crowbarMove(self, player, coords): # Needs to be updated to ensure the store moved to is adjacent. 
        if coords[1] == 0: # Ensures player is moving to an entrance room. 
            return True
        return False
    
    def serialize(self):
        dict = {
            "image": self.image
        }
        return dict
    
    def deserialize(dict):
        return

class golfClub(MeleeWeapon):
    def __init__(self, image=""):
        super().__init__()


# Add a ranged weapon