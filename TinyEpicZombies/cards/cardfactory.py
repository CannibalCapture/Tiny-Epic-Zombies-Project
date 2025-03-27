from .weapons import *
from .backpackitems import *

class CardFactory:
    def __init__(self):
        pass

    def createCard(cardType, colour):
        match cardType:
            case "crowbar":
                return Crowbar(colour)
            case "golfClub":
                return GolfClub(colour)
            case "adrenaline":
                return Adrenaline(colour)