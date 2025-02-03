class Card:
    def __init__(self, colour, player=-1):
        self.colour = colour

    def serialize(self):
        return "no serialise method defined"
    
    def deserialize(dict):
        return "no deserialise method defined"
    
    def getColour(self):
        return self.colour
    
    def getID(self):
        return self.ID
    
    def getImg(self):
        return self.img
    
class MeleeWeapon(Card):
    def __init__(self, colour):
        self.type = "MELEE WEAPON"
        super().__init__(colour)

    def serialize(self):
        return { "type": self.type }

    def deserialize(dict):
        return MeleeWeapon()

class RangedWeapon(Card):
    def __init__(self):
        self.type = "RANGED WEAPON"

    def serialize(self):
        return { "type": self.type }
    
    def deserialize(dict):
        return RangedWeapon()