from .cards.weapons import *
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
        self.supplyDeck.append(Crowbar("GREEN"))
        self.supplyDeck.append(golfClub("ORANGE"))
        self.supplyDeck.append(golfClub("BLUE"))
        self.supplyDeck.append(golfClub("GREEN"))
        
        self.searchDeck.append(Crowbar("BLUE"))
        self.searchDeck.append(Crowbar("RED"))
        self.searchDeck.append(Crowbar("GREEN"))
        self.searchDeck.append(golfClub("ORANGE"))
        self.searchDeck.append(golfClub("BLUE"))
        self.searchDeck.append(golfClub("GREEN"))

    def serialize(self):
        dict = {
            "supplyDeck": self.supplyDeck,
            "searchDeck": self.searchDeck
        }
        return dict

    def deserialize(dict):
        return DeckManager([card.deserialize() for card in dict["supplyDeck"]], [card.deserialize() for card in dict["searchDeck"]])
    
    def drawSupply(self):
        card = randint(0, len(self.supplyDeck)-1)
        return self.supplyDeck.pop(card) # Both returns and removes the drawn card from the list. 
    
    def drawSearch(self):
        card = randint(0, len(self.searchDeck)-1)
        return self.searchDeck.pop(card)