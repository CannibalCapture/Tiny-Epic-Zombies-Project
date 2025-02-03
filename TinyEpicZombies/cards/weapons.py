from .card import Card, MeleeWeapon, RangedWeapon

# Implement events for listeners into gameManager?

class Crowbar(MeleeWeapon):
    def __init__(self, colour):
        self.img = "crowbar.jpg"
        self.ID = "crowbar"
        super().__init__(colour)

    def validateCrowbarMove(self, coords): # Needs to be updated to ensure the store moved to is adjacent. 
        if coords[1] == 0: # Ensures player is moving to an entrance room. 
            return True
        return False
    
    def serialize(self):
        dict = {"image": self.img}
        return dict
    
    def deserialize(dict):
        return

class golfClub(MeleeWeapon):
    def __init__(self, colour):
        self.img = "golfClub.jpg"
        self.ID = "golfClub"
        super().__init__(colour)


# Add a ranged weapon