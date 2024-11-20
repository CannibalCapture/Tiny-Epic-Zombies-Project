from .listener import Listener

class Player(Listener):
    def __init__(self, name, playerID, colour, character, coords, meleeWeapon=None, rangedWeapon=None, health=9, ammo=9, moves = 3):
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
        pass

    def rangedAttack(self):
        pass

    def setmeleeWeapon(self, newWeapon):
        self.meleeWeapon = newWeapon

    def setrangedWeapon(self, newWeapon):
        self.rangedWeapon = newWeapon

    def changeAmmo(self, value):
        self.ammo += value

    def on_event(self, event):
        print(event)
        if event['type'] == 'PLAYER MELEE':
            print(f"{self.name} kills a zombie at {self.coords}")
        elif event['type'] == 'PLAYER RANGED':
            print(f"{self.name} kills a zombie from range")