import pygame, os
from .helperfunctions.deserialisers import deserializeStore
from .constants import WIDTH, HEIGHT
from .eventGenerator import EventGenerator
from .listener import Listener

class Button(EventGenerator, Listener):
    def __init__(self, ID, pos, enabled, state):
        self.ID = ID
        self.enabled = enabled
        self.state = state
        self.enabled_img = None
        self.disabled_img = None
        self.load_images()
        self.rect = self.getImg().get_rect() if self.getImg() else pygame.Rect(0, 0, 0, 0)
        self.setPos(pos)
        self.rect.topleft = (self.pos[0]*WIDTH, self.pos[1]*HEIGHT)

    def load_images(self):
        pass

    def disable(self):
        self.enabled = False
        self.state = False
        #self.updateImg()

    def enable(self):
        self.enabled = True
        #self.updateImg()

    def on_event(self, event):
        if event['type'] == 'MODE CHANGE' and event['mode'] != self.ID:
            self.state = False
    
    def onClick(self):
        pass

    def updateImg():
        pass

    def getEnabled(self):
        return self.enabled

    def getImg(self):
        if self.enabled:
            return self.enabled_img
        else:
            return self.disabled_img
    
    def getRect(self):
        return self.rect

    def getState(self):
        return self.state
    
    def getID(self):
        return self.ID
    
    def getPos(self):
        return self.pos
    
    def setPos(self, pos):
        self.pos = pos
        self.rect.topleft = (self.pos[0]*WIDTH, self.pos[1]*HEIGHT)

    def setState(self, value):
        self.state = value

class AttackButton(Button):
    def __init__(self):
        super().__init__("attackButton", (0.92, 0.87), True, False)

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

    def load_images(self):
        width, height = 0.05, 0.08 # maybe put in json file
        self.enabled_img = pygame.image.load(os.path.join("TinyEpicZombies", "assets", "buttons", "attackTrue.png"))
        self.enabled_img = pygame.transform.scale(self.enabled_img, (WIDTH*width, HEIGHT*height))
        self.disabled_img = pygame.image.load(os.path.join("TinyEpicZombies", "assets","buttons", "attackFalse.png"))
        self.disabled_img = pygame.transform.scale(self.disabled_img, (WIDTH*width, HEIGHT*height))

class MoveButton(Button):
    def __init__(self):
        super().__init__("move",  (0.84, 0.87), True, False)

    def load_images(self):
        width, height = 0.05, 0.08 # maybe put in json file
        self.enabled_img = pygame.image.load(os.path.join("TinyEpicZombies", "assets", "buttons", "moveTrue.png"))
        self.enabled_img = pygame.transform.scale(self.enabled_img, (WIDTH*width, HEIGHT*height))
        self.disabled_img = pygame.image.load(os.path.join("TinyEpicZombies", "assets", "buttons", "moveFalse.png")) # change to moveFalse when it exists
        self.disabled_img = pygame.transform.scale(self.disabled_img, (WIDTH*width, HEIGHT*height))

    def on_event(self, event):
        if event['type'] == 'PLAYER MOVED':
            if event['moves'] == 0:
                self.disable()
        if event['type'] == 'TURN CHANGE':
            self.enable()

    def getImg(self):
        if self.enabled==True:
            return self.enabled_img
        else:
            return self.disabled_img
    def onClick(self):
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
        super().__init__("openCard", (0.96, 0.02), True, True)

    def load_images(self):
        width, height = 0.03, 0.048
        self.enabled_img = pygame.image.load(os.path.join("TinyEpicZombies", "assets", "buttons", "downArrow.png"))
        self.enabled_img = pygame.transform.scale(self.enabled_img, (WIDTH*width, HEIGHT*height))
        self.disabled_img = pygame.image.load(os.path.join("TinyEpicZombies", "assets", "buttons", "upArrow.png"))
        self.disabled_img = pygame.transform.scale(self.disabled_img, (WIDTH*width, HEIGHT*height))

    def onClick(self):
        if not self.enabled:
            return
        else:
            if self.state:
                self.state = False
                return {'type':'CLOSE CARD'}
            else:
                self.state = True
                return {'type':'OPEN CARD'}

    def getImg(self):
            if self.state:
                return self.enabled_img
            else:
                return self.disabled_img

class EndTurnButton(Button):
    def __init__(self):
        super().__init__("endTurn", (0.90, 0.67), True, True)

    def load_images(self):
        width, height = 0.1, 0.16
        self.enabled_img = pygame.image.load(os.path.join("TinyEpicZombies", "assets", "buttons", "endTurn.png"))
        self.enabled_img = pygame.transform.scale(self.enabled_img, (WIDTH*width, HEIGHT*height))
        self.disabled_img = pygame.image.load(os.path.join("TinyEpicZombies", "assets", "buttons", "empty.png"))
        self.disabled_img = pygame.transform.scale(self.disabled_img, (WIDTH*width, HEIGHT*height))

    def onClick(self):
        return {'type':'END TURN'}
    
class StoreCardsButton(Button): # show all cards attatched to a specific store. 
    def __init__(self, store):
        super().__init__("storeCards", (0,0), True, False)
        dStore = deserializeStore(store)
        self.store = store
        self.setPos(tuple(dStore["tl"]))

    def load_images(self):
        width, height = 0.025, 0.040
        self.enabled_img = pygame.image.load(os.path.join("TinyEpicZombies", "assets", "buttons", "downArrowGreen.png"))
        self.enabled_img = pygame.transform.scale(self.enabled_img, (WIDTH*width, HEIGHT*height))
        self.disabled_img = pygame.image.load(os.path.join("TinyEpicZombies", "assets", "buttons", "downArrowGrey.png"))
        self.disabled_img = pygame.transform.scale(self.disabled_img, (WIDTH*width, HEIGHT*height))

    def onClick(self):
        if not self.enabled:
            return
        else:
            if self.state:
                self.state = False
                return {'type':'HIDE CARDS', 'store':self.store}
            else:
                self.state = True
                return {'type':'SHOW CARDS', 'store':self.store}
            
    def on_event(self, event):
        if event['type'] == 'SHOW CARDS':
            if event['store'] != self.store:
                self.state = False 
        if event['type'] == 'TURN CHANGE':
            if event['player'].getCoords()[0] == self.store:
                self.state = True
            else:
                self.state = False


    def getImg(self):
        if self.state:
            return self.enabled_img
        else:
            return self.disabled_img
            
class PickupStoreCardsButton(Button):
    def __init__(self):
        super().__init__("pickupStoreCards", (0.80, 0.67), False, False)

    def load_images(self):
        width, height = 0.1, 0.16
        self.enabled_img = pygame.image.load(os.path.join("TinyEpicZombies", "assets", "buttons", "upArrowGreen.png"))
        self.enabled_img = pygame.transform.scale(self.enabled_img, (WIDTH*width, HEIGHT*height))
        self.disabled_img = pygame.image.load(os.path.join("TinyEpicZombies", "assets", "buttons", "upArrowGrey.png"))
        self.disabled_img = pygame.transform.scale(self.disabled_img, (WIDTH*width, HEIGHT*height))

    def onClick(self):
        if not self.enabled:
            return
        else:
            self.disable()
            return {'type':'PICKUP STORE CARDS'}
        
    def on_event(self, event):
        if event['type'] == 'PLAYER MOVED' and event['moves'] == 0:
            self.enable()
        if event['type'] == 'TURN CHANGE':
            self.disable()

class ExitMenuButton(Button): # Returns to gameboard screen
    def __init__(self):
        super().__init__("exitMenu", (0.2, 0.2), False, False)

    def onClick(self):
        if not self.enabled:
            return
        else:
            self.disable()
            return {'type':'EXIT MENU'}
    
    def on_event(self, event):
        if event['type'] == 'PICKUP STORE CARDS' or event['type'] == 'OPEN INVENTORY':
            self.enable()
        
    def load_images(self):
        width, height = 0.1, 0.16
        self.enabled_img = pygame.image.load(os.path.join("TinyEpicZombies", "assets", "buttons", "endTurn.png"))
        self.enabled_img = pygame.transform.scale(self.enabled_img, (WIDTH*width, HEIGHT*height))
        self.disabled_img = pygame.image.load(os.path.join("TinyEpicZombies", "assets", "buttons", "empty.png"))
        self.disabled_img = pygame.transform.scale(self.disabled_img, (WIDTH*width, HEIGHT*height))

    def getImg(self):
        if self.enabled:
            return self.enabled_img
        else:
            return self.disabled_img

class TestButton(Button):
    def __init__(self):
        super().__init__("exitMenu", (0.8, 0.2), True, False)

    def onClick(self):
        if not self.enabled:
            return
        else:
            return {'type':'TEST BUTTON'}
    
    def load_images(self):
        width, height = 0.1, 0.16
        self.enabled_img = pygame.image.load(os.path.join("TinyEpicZombies", "assets", "buttons", "endTurn.png"))
        self.enabled_img = pygame.transform.scale(self.enabled_img, (WIDTH*width, HEIGHT*height))
        self.disabled_img = self.enabled_img

class InventoryButton(Button):
    def __init__(self):
        super().__init__("inventory", (0.90, 0.47), True, False)

    def onClick(self):
        if not self.enabled:
            return
        else:
            if self.state:
                return
            else:
                return {'type': 'OPEN INVENTORY'}
    
    def on_event(self, event):
        if event['type'] == 'EXIT MENU':
            self.state = False
            
    def load_images(self):
        width, height = 0.06, 0.12
        self.enabled_img = pygame.image.load(os.path.join("TinyEpicZombies", "assets", "buttons", "backpack.png"))
        self.enabled_img = pygame.transform.scale(self.enabled_img, (WIDTH*width, HEIGHT*height))
        self.disabled_img = self.enabled_img # to be changed I suppose
