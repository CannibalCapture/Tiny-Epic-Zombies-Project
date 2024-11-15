from .graph import Graph
from .store import Store

class Map: # map will manage the rooms
    def __init__(self, stores=[]):
        self.stores = stores

    def addStore(self, storeID, rooms=[]): # pass in a list of 3 rooms
        self.stores[storeID] = Store(rooms, storeID)