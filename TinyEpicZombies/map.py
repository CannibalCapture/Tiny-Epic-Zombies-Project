from .graph import Graph

class Map: # map will manage the rooms
    def __init__(self, stores={}):
        self.stores = stores

    def addStore(self, storeID, store):
        self.stores[storeID] = store