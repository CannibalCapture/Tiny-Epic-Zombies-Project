from .adjList import adjList
from .store import Store

# To access the room at coordinates (a,b): map.stores[a].rooms[b]

class Map: # map will manage the rooms
    def __init__(self, stores=[]):
        self.stores = stores
        self.adjList = adjList(stores)

    def createStore(self, storeID, rooms=[]): # pass in a list of 3 rooms
        self.stores[storeID] = Store(rooms, storeID)