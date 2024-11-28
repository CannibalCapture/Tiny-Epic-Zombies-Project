from .card import Card, MeleeWeapon, RangedWeapon, BackpackItem
from .weapons import *
from random import randint

class DeckManager:
    def __init__(self):
        self.supplyDeck = []
        self.searchDeck = []
        self.createDecks()

    def createDecks(self): # Decks are not currently randomised - random.shuffle(list) - will do it,
        # but drawing is already randomised. 
        for i in range(6):
            self.supplyDeck.append(Crowbar())
        for i in range(6):
            self.searchDeck.append(golfClub())
    
    def takeSupply(self):
        card = randint(0, len(self.supplyDeck)-1)
        return self.supplyDeck.pop(card) # Both returns and removes the drawn card from the list. 
    
    def takeSearch(self):
        card = randint(0, len(self.searchDeck)-1)
        return self.searchDeck.pop(card)