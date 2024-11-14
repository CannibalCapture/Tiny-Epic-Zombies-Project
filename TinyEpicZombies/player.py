class Player():
    def __init__(self, name, playerID, colour, character, meleeWeapon=None, rangedWeapon=None, health=9, ammo=9, moves = 3):
        self.room = None
        self.name = name
        self.colour = colour
        self.character = character
        self.meleeWeapon = meleeWeapon
        self.rangedWeapon = rangedWeapon
        self.health = health
        self.ammo = ammo
        self.moves = moves
        self.playerID = playerID

    def move(self, room):
        self.room.removePlayer(self)
        self.room = room
        self.room.addPlayer(self)
        
    def meleeAttack(self):
        pass

    def rangedAttack(self, targetRoom):
        pass

    def setmeleeWeapon(self, newWeapon):
        self.meleeWeapon = newWeapon

    def setrangedWeapon(self, newWeapon):
        self.rangedWeapon = newWeapon

    def changeAmmo(self, value):
        self.ammo += value

    def on_event(self, event):
        print(event)