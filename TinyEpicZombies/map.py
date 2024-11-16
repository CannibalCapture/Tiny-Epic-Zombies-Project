from .adjList import adjList
from .store import Store

class Map: # map will manage the rooms
    def __init__(self, stores=[]):
        self.stores = stores
        self.adjList = adjList(stores)

    def linkStoreLeft(self, store1, store2, value): # room2 is to the left of room1
        self.graph.addEdge(store1, store2, value)

    def addStore(self, storeID, rooms=[]): # pass in a list of 3 rooms
        self.stores[storeID] = Store(rooms, storeID)