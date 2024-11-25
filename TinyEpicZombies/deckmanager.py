from .card import *
from random import randint

class DeckManager:
    def __init__(self):
        self.supplyDeck = []
        self.searchDeck = []
        self.createDecks()

    def createDecks(self): # Decks are not currently randomised. 
        for i in range(6):
            self.supplyDeck.append(MeleeWeapon())
        for i in range(6):
            self.searchDeck.append(MeleeWeapon())
    
    def drawSupply(self):
        card = randint(0, len(self.supplyDeck))
        return self.supplyDeck.pop(card) # Both returns and removes the drawn card from the list. 
    
    def drawSearch(self):
        card = randint(0, len(self.searchDeck))
        return self.searchDeck.pop(card)