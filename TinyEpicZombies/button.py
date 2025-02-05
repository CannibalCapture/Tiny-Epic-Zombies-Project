import pygame, os
from .helperfunctions.deserialisers import deserializeStore
from .constants import WIDTH, HEIGHT
from .eventgenerator import EventGenerator
from .listener import Listener

class Button(EventGenerator, Listener):
    def __init__(self):
        pass

    def disable(self):
        self.enabled = False
        self.state = False
        self.updateImg()

    def enable(self):
        self.enabled = True
        self.updateImg()

    def on_event(self, event):
        if event['type'] == 'MODE CHANGE' and event['mode'] != self.ID:
            self.state = False
    
    def onClick(self):
        pass

    def updateImg():
        pass

    def getImg(self):
        return self.img
    
    def getRect(self):
        return self.rect

    def getState(self):
        return self.state
    
    def getID(self):
        return self.ID

    def setState(self, value):
        self.state = value

class AttackButton(Button):
    def __init__(self):
        self.pos = (0.92, 0.87)
        self.ID = "attack"
        self.enabled = True
        self.state = False
        self.updateImg()
        self.rect = self.img.get_rect()
        self.rect.topleft = (self.pos[0]*WIDTH, self.pos[1]*HEIGHT)

    def onClick(self):
        if not self.enabled:
            return
        else:
            if self.state:
                self.state = False
                return {"mode":None}
            else:
                self.state = True
                return {"mode":"attack"}

    def on_event(self, event):
        if event['type'] == 'PLAYER MELEE' or event['type'] == 'PLAYER RANGED':
            self.disable()
        elif event['type'] == 'PLAYER MOVED' or event['type'] == 'TURN CHANGE':
            self.enable()
        super().on_event(event)

    def updateImg(self):
        width, height = 0.05, 0.08 # maybe put in json file
        if self.enabled:
            self.img = pygame.image.load(os.path.join("TinyEpicZombies", "assets", "buttons", "attackTrue.png"))
        else:
            self.img = pygame.image.load(os.path.join("TinyEpicZombies", "assets","buttons", "attackFalse.png"))

        self.img = pygame.transform.scale(self.img, (WIDTH*width, HEIGHT*height))
    
    def getEnabled(self):
        return self.enabled

class MoveButton(Button):
    def __init__(self):
        self.pos = (0.84, 0.87)
        self.ID = "move" # the mode which the button represents
        self.enabled = True
        self.state = False
        self.updateImg()
        self.rect = self.img.get_rect()
        self.rect.topleft = (self.pos[0]*WIDTH, self.pos[1]*HEIGHT)
    
    def updateImg(self):
        width, height = 0.05, 0.08 # maybe put in json file
        if self.enabled: # can probably go in parent class
            self.img = pygame.image.load(os.path.join("TinyEpicZombies", "assets", "buttons", "moveTrue.png"))
        else:
            self.img = pygame.image.load(os.path.join("TinyEpicZombies", "assets", "buttons", "moveFalse.png"))

        self.img = pygame.transform.scale(self.img, (WIDTH*width, HEIGHT*height))
    
    def onClick(self): # toggling on / off states could go in parent class
        if not self.enabled:
            return
        else:
            if self.state:
                self.state = False
                return {"mode":None}
            else:
                self.state = True
                return {"mode":"move"}
    

class OpenCardButton(Button):
    def __init__(self):
        self.pos = (0.96, 0.02)
        self.ID = "openCard" # the mode which the button represents
        self.enabled = True
        self.state = True
        self.updateImg()
        self.rect = self.img.get_rect()
        self.rect.topleft = (self.pos[0]*WIDTH, self.pos[1]*HEIGHT)

    def updateImg(self):
        width, height = 0.03, 0.048 # maybe put in json file
        if self.state: # can probably go in parent class
            self.img = pygame.image.load(os.path.join("TinyEpicZombies", "assets", "buttons", "downArrow.png"))
        else:
            self.img = pygame.image.load(os.path.join("TinyEpicZombies", "assets", "buttons", "upArrow.png"))

        self.img = pygame.transform.scale(self.img, (WIDTH*width, HEIGHT*height))

    def onClick(self):
        if not self.enabled:
            return
        else:
            if self.state:
                self.state = False
                self.updateImg()
                return {'type':'CLOSE CARD'}
            else:
                self.state = True
                self.updateImg()
                return {'type':'OPEN CARD'}

class EndTurnButton(Button):
    def __init__(self):
        self.pos = (0.90, 0.67)
        width, height = 0.1, 0.16
        self.ID = "endTurn"
        self.enabled = True
        self.state = True
        self.img = pygame.image.load(os.path.join("TinyEpicZombies", "assets", "buttons", "endTurn.png"))
        self.img = pygame.transform.scale(self.img, (WIDTH*width, HEIGHT*height))
        self.rect = self.img.get_rect()
        self.rect.topleft = (self.pos[0]*WIDTH, self.pos[1]*HEIGHT)

    def onClick(self):
        return {'type':'END TURN'}
    
class StoreCardsButton(Button):
    def __init__(self, store):
        dStore = deserializeStore(store)
        self.store = store
        self.pos = tuple(dStore["tl"])
        self.enabled = True
        self.state = False
        width, height = 0.03, 0.03
        self.img = pygame.image.load(os.path.join("TinyEpicZombies", "assets", "buttons", "downArrow.png"))
        self.img = pygame.transform.scale(self.img, (WIDTH*width, HEIGHT*height))
        self.rect = self.img.get_rect()
        self.rect.topleft = (self.pos[0]*WIDTH, self.pos[1]*HEIGHT)

    def onClick(self):
        if not self.enabled:
            return
        else:
            if self.state:
                self.state = False
                self.updateImg()
                return {'type':'HIDE CARDS'}
            else:
                self.state = True
                self.updateImg()
                return {'type':'SHOW CARDS'}