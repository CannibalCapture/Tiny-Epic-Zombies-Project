from random import choice
import pygame, os
from .listener import Listener
from .eventGenerator import EventGenerator
from .cards.card import Card
from .constants import CW, CH, WIDTH, HEIGHT

class Player(Listener, EventGenerator):
    def __init__(self, name, ID, colour, character, coords, meleeWeapon=None, rangedWeapon=None, healthMissing=0, ammoMissing=0, moves = 3):
        Listener.__init__(self)
        EventGenerator.__init__(self)
        self.coords = coords
        self.name = name
        self.colour = colour
        self.meleeWeapon = meleeWeapon
        self.rangedWeapon = rangedWeapon
        self.inventory = []
        self.healthMissing = healthMissing
        self.ammoMissing = ammoMissing
        self.moves = moves
        self.movementOptions = None
        self.ID = ID
        self.character = character
        self.alive = True
        img = pygame.image.load(os.path.join("TinyEpicZombies", "assets", "avatars",f"{self.character}.png"))
        img = pygame.transform.scale(img, (0.04*WIDTH, 0.06*HEIGHT))
        self.img = img
        img = pygame.image.load(os.path.join("TinyEpicZombies", "assets", "characters",f"{self.character}Card.jpg"))
        img = pygame.transform.scale(img, ((CW*1.6)*WIDTH, (CH*1.6)*HEIGHT))
        self.cardImg = img

    def serialize(self):
        dict = {
            "coords":[self.coords[0], self.coords[1]],
            "name":self.name,
            "colour":self.colour,
            "character":self.character,
            "rangedweapon": "None" if self.rangedWeapon == None else self.rangedWeapon.serialize(),
            "meleeweapon": "None" if self.meleeWeapon == None else self.meleeWeapon.serialize(),
            "healthMissing":self.healthMissing,
            "ammoMissing":self.ammoMissing,
            "moves":self.moves,
            "ID":self.ID,
        }

        return dict

    def deserialize(dict):
        return Player(dict["name"], dict["ID"], dict["colour"], dict["character"], tuple(dict["coords"]),None, None, dict["healthMissing"], dict["ammoMissing"], dict["moves"])

    def move(self, coords):
        self.coords = coords
        
    def meleeAttack(self):
        self.rollMeleeDice()

    def addCard(self, val):
        self.inventory.append(val)

    def rollMeleeDice(self):
        choices = [0,0,1,2,-1,-1]
        roll = choice(choices)
        if roll >= 0:
            self.takeDamage(roll)
        else:
            self.moves += 1

    def takeDamage(self, value):
        self.healthMissing += value
        if not self.isAlive():
            self.alive = False
            print("player died", self.character, self.ID)

    
    def isAlive(self):
        if self.ammoMissing + self.healthMissing > 8:
            return False
        return True
    
    def reset(self):
        self.move((4,2)) # move to spawn room
        self.ammoMissing = 0
        self.healthMissing = 0
        self.meleeWeapon = None
        self.rangedWeapon = None
        self.alive = True

    def rangedAttack(self):
        self.changeAmmo(1)

    def changeAmmo(self, value):
        self.ammoMissing += value
        if not self.isAlive():
            self.alive = False
            print("player died", self.character, self.ID)
    
    def on_event(self, event):
        if event['type'] == 'PLAYER MELEE':
            pass
        elif event['type'] == 'PLAYER RANGED':
            pass

    def setMeleeWeapon(self, newWeapon):
        self.meleeWeapon = newWeapon

    def setRangedWeapon(self, newWeapon):
        self.rangedWeapon = newWeapon
    
    def getMeleeWeapon(self):
        return self.meleeWeapon
    
    def getRangedWeapon(self):
        return self.rangedWeapon
    
    def getID(self):
        return self.ID

    def getInventory(self):
        return self.inventory
    
    def getAlive(self):
        return self.alive

    def getCoords(self):
        return self.coords
    
    def getColour(self):
        return self.colour
    
    def getCharacter(self):
        return self.character
    
    def getMoves(self):
        return self.moves # the number of times the player may move each turn. 

    def getMovementOptions(self):
        return self.movementOptions
    
    def getCardImg(self):
        return self.cardImg
    
    def getImg(self):
        return self.img

    def getAmmoMissing(self):
        return self.ammoMissing

    def getHealthMissing(self):
        return self.healthMissing

    def setMovementOptions(self, lstValue):
        self.movementOptions = lstValue

    def setAlive(self, val):
        self.alive = val
