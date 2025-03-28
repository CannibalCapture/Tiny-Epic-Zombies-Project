from .room import Room

class Store:
    def __init__(self, rooms, ID, noiseColour, image, tl):
        self.rooms = rooms
        self.ID = ID
        self.noiseColour = noiseColour
        self.image = image
        self.tl = tl
        self.cards = []

    def serialize(self):
        dict = {
            "ID": self.ID,
            "rooms": [room.serialize() for room in self.rooms],
            "tl": self.tl,
            "image": self.image,
            "noiseColour": self.noiseColour
        }
        return dict
    
    def deserialize(dict, gm):
        return Store([Room.deserialize(room, gm) for room in dict["rooms"]], dict["ID"], dict["noiseColour"], dict["image"], dict["tl"])
    
    def addCard(self, card):
        self.cards.append(card)

    def removeCard(self, index):
        return self.cards.pop(index)
    
    def removeBackpackCards(self):
        bpLst = []
        weaponsLst = []
        for card in self.cards:
            if card.getType() == "BACKPACK ITEM":
                bpLst.append(card)
            else:
                weaponsLst.append(card)
        self.cards = weaponsLst
        return bpLst
        

    def removeCardByValue(self, val):
        return self.cards.remove(val)

    def getNoiseColour(self):
        return self.noiseColour

    def setCards(self, value):
        self.cards = value

    def getID(self):
        return self.ID
    
    def getRooms(self):
        return self.rooms
    
    def getCards(self):
        return self.cards