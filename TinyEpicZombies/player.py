from random import choice
from .listener import Listener
from .eventGenerator import EventGenerator

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
        self.ammo -= 1

    def equipMelee(self, newWeapon):
        self.meleeWeapon = newWeapon

    def equipRanged(self, newWeapon):
        self.rangedWeapon = newWeapon

    def changeAmmo(self, value):
        self.ammo += value

    def on_event(self, event):
        print(event)
        if event['type'] == 'PLAYER MELEE':
            print(f"{self.name} kills a zombie at {self.coords}")
        elif event['type'] == 'PLAYER RANGED':
            print(f"{self.name} kills a zombie from range")
