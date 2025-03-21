from .cards.weapons import *
from .cards.backpackitems import *
from random import randint

class DeckManager:
    def __init__(self, supplyDeck=[], searchDeck=[]):
        self.supplyDeck = supplyDeck
        self.searchDeck = searchDeck
        self.createDecks()

    def createDecks(self): # Decks are not currently randomised - random.shuffle(list) - will do it,
        # but drawing is already randomised. 
        
        self.supplyDeck.append(Crowbar("BLUE"))
        self.supplyDeck.append(Crowbar("RED"))
        self.supplyDeck.append(GolfClub("ORANGE"))
        self.supplyDeck.append(GolfClub("GREEN"))
        self.supplyDeck.append(Revolver("BLUE"))
        self.supplyDeck.append(Revolver("GREEN"))
        
        self.searchDeck.append(Crowbar("BLUE"))
        self.searchDeck.append(Crowbar("RED"))
        self.searchDeck.append(GolfClub("ORANGE"))
        self.searchDeck.append(GolfClub("GREEN"))
        self.searchDeck.append(Revolver("GREEN"))
        self.searchDeck.append(Revolver("BLUE"))
        self.searchDeck.append(Adrenaline("ORANGE"))
        self.searchDeck.append(Adrenaline("GREEN"))
        self.searchDeck.append(Adrenaline("BLUE"))
        self.searchDeck.append(Adrenaline("PURPLE"))

    def serialize(self):
        dict = {
            "supplyDeck": self.supplyDeck,
            "searchDeck": self.searchDeck
        }
        return dict

    def deserialize(dict):
        return DeckManager([card.deserialize() for card in dict["supplyDeck"]], [card.deserialize() for card in dict["searchDeck"]])

    def drawSupply(self):
        if len(self.supplyDeck) != 0:
            card = randint(0, len(self.supplyDeck)-1)
            return self.supplyDeck.pop(card) # Both returns and removes the drawn card from the list. 
        else:
            pass
    
    def drawSearch(self):
        if len(self.searchDeck) != 0:
            card = randint(0, len(self.searchDeck)-1)
            out = self.searchDeck.pop(card)
        else:
            out = 0 # end game after 1 more turn
        return out