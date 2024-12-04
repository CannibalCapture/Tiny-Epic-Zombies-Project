from .map import Map
from .adjlist import adjList

class ZombieMap(Map):
    def __init__(self, stores=[]):
        self.stores = stores
        self._initStores()
        self.al = adjList(self.stores)
        self.addEdges()

    def addEdges(self):
        self.al.addEdge((0,0),(0,1))
        self.al.addEdge((0,1),(0,2))
        self.al.addEdge((0,2),(1,0))
        self.al.addEdge((1,0),(1,1))
        self.al.addEdge((1,1),(1,2))
        self.al.addEdge((1,2),(4,1))
        self.al.addEdge((4,1), (4,2))

        self.al.addEdge((2,0),(2,1))
        self.al.addEdge((2,1),(2,2))
        self.al.addEdge((2,2),(5,2))
        self.al.addEdge((5,2),(5,0))
        self.al.addEdge((5,0),(5,1))
        self.al.addEdge((5,1),(4,4))
        self.al.addEdge((4,4), (4,2))

        self.al.addEdge((8,2),(8,1))
        self.al.addEdge((8,1),(8,0))
        self.al.addEdge((8,0),(7,2))
        self.al.addEdge((7,2),(7,1))
        self.al.addEdge((7,1),(7,0))
        self.al.addEdge((7,0),(4,3))
        self.al.addEdge((4,3), (4,2))

        self.al.addEdge((6,2),(6,1))
        self.al.addEdge((6,1),(6,0))
        self.al.addEdge((6,0),(7,2))
        self.al.addEdge((3,2),(3,0))
        self.al.addEdge((3,0),(3,1))
        self.al.addEdge((3,1),(4,0))
        self.al.addEdge((4,0), (4,2))