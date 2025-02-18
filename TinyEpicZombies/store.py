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
            "rooms": [room.serialize() for room in self.rooms],
            "tl": self.tl,
            "ID": self.ID,
            "image": self.image,
            "noiseColour": self.noiseColour
        }
        return dict
    
    def deserialize(dict):
        return Store([room.deserialize() for room in dict["rooms"]], dict["ID"], dict["noiseColour"], dict["image"], dict["tl"])
    
    def addCard(self, card):
        self.cards.append(card)

    def removeCard(self, index):
        return self.cards.pop(index)

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