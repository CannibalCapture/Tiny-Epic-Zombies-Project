class Store:
    def __init__(self, rooms, storeID, noiseColour, image, tl):
        self.rooms = rooms
        self.storeID = storeID
        self.noiseColour = noiseColour
        self.image = image
        self.tl = tl

    def serialize(self):
        dict = {
            "rooms": [room.serialize() for room in self.rooms],
            "tl": self.tl,
            "storeID": self.storeID,
            "image": self.image,
            "noiseColour": self.noiseColour
        }
        return dict
    
    def deserialize(dict):
        return Store([room.deserialize() for room in dict["rooms"]], dict["storeID"], dict["noiseColour"], dict["image"], dict["tl"])
    
    def getNoiseColour(self):
        return self.noiseColour

    def getStoreID(self):
        return self.storeID
    
    def getRooms(self):
        return self.rooms