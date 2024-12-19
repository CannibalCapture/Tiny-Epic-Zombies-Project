from .meleeweapon import MeleeWeapon
from .rangedweapon import RangedWeapon
from ..assets.weapons import *

# Implement events for listeners into gameManager?

class Crowbar(MeleeWeapon):
    def __init__(self):
        super().__init__()
        self.image = "crowbar.jpg"

    def validateCrowbarMove(self, coords): # Needs to be updated to ensure the store moved to is adjacent. 
        if coords[1] == 0: # Ensures player is moving to an entrance room. 
            return True
        return False
    
    def serialize(self):
        dict = {"image": self.image}
        return dict
    
    def deserialize(dict):
        return

class golfClub(MeleeWeapon):
    def __init__(self):
        super().__init__()
        self.image = "golfClub.jpg"


# Add a ranged weapon