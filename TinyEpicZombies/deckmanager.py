from .card import *
from random import randint

class DeckManager:
    def __init__(self):
        self.supplyDeck = []
        self.searchDeck = []
        self.createDecks()

    def createDecks(self): # Decks are not currently randomised - random.shuffle(list) - will do it,
        # but drawing is already randomised. 
        for i in range(6):
            self.supplyDeck.append(MeleeWeapon())
        for i in range(6):
            self.searchDeck.append(MeleeWeapon())
    
    def drawSupply(self):
        card = randint(0, len(self.supplyDeck)-1)
        return self.supplyDeck.pop(card) # Both returns and removes the drawn card from the list. 
    
    def drawSearch(self):
        card = randint(0, len(self.searchDeck)-1)
        return self.searchDeck.pop(card)