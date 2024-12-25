from random import choice
from .listener import Listener
from .eventgenerator import EventGenerator
from .cards.meleeweapon import MeleeWeapon
from .cards.rangedweapon import RangedWeapon

class Player(Listener, EventGenerator):
    def __init__(self, name, playerID, colour, character, coords, meleeWeapon=None, rangedWeapon=None, health=9, ammo=9, moves = 3):
        Listener.__init__(self)
        EventGenerator.__init__(self)
        self.coords = coords
        self.name = name
        self.colour = colour
        self.character = character
        self.meleeWeapon = meleeWeapon
        self.rangedWeapon = rangedWeapon
        self.health = health
        self.ammo = ammo
        self.moves = moves
        self.playerID = playerID

    def serialize(self):
        dict = {
            "coords":[self.coords[0], self.coords[1]],
            "name":self.name,
            "colour":self.colour,
            "character":self.character,
            "rangedweapon": "None" if self.rangedWeapon == None else self.rangedWeapon.serialize(),
            "meleeweapon": "None" if self.meleeWeapon == None else self.meleeWeapon.serialize(),
            "health":self.health,
            "ammo":self.ammo,
            "moves":self.moves,
            "playerID":self.playerID,
        }

        return dict

    def deserialize(dict):
        return Player(dict["name"], dict["playerID"], dict["colour"], dict["character"], tuple(dict["coords"]), 
                      None if  dict["meleeweapon"] == "None" else MeleeWeapon.deserialize(dict["meleeweapon"]),
                      None if  dict["rangedweapon"] == "None" else RangedWeapon.deserialize(dict["rangedweapon"]),
                      dict["health"], dict["ammo"], dict["moves"])

    def move(self, coords):
        self.coords = coords
        
    def meleeAttack(self):
        self.rollMeleeDice()

    def rollMeleeDice(self):
        choices = [0,0,1,2,-1,-1]
        roll = choice(choices)
        if roll >= 0:
            self.takeDamage(roll)
        else:
            self.moves += 1

    def takeDamage(self, value):
        self.health -= value
        if not self.isAlive():
            event = {'type': 'PLAYER DIE', 'playerID': self.playerID}
            self.send_event(event)
    
    def isAlive(self):
        if self.ammo + self.health < 11:
            return False
        return True
    
    def reset(self):
        self.move((0,0)) # move to spawn room
        self.ammo = 9
        self.health = 9
        self.meleeWeapon = None
        self.rangedWeapon = None

    def rangedAttack(self):
        self.changeAmmo(-1)

    def changeAmmo(self, value):
        self.ammo += value

    def equipMelee(self, newWeapon):
        self.meleeWeapon = newWeapon

    def equipRanged(self, newWeapon):
        self.rangedWeapon = newWeapon
    
    def getMelee(self):
        return self.meleeWeapon
    
    def getRanged(self):
        return self.rangedWeapon
    
    def getID(self):
        return self.playerID
    
    def getCoords(self):
        return self.coords
    
    def getMoves(self):
        return self.moves

    def on_event(self, event):
        print(event)
        if event['type'] == 'PLAYER MELEE':
            print(f"{self.name} kills a zombie at {self.coords}")
        elif event['type'] == 'PLAYER RANGED':
            print(f"{self.name} kills a zombie from range")
