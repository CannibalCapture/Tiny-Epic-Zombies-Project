from .adjlist import adjList
from .store import Store
from .room import Room
from .constants import COLOURS

# To access the room at coordinates (a,b): map.stores[a].rooms[b]

class Map: # map will manage the rooms
    def __init__(self, stores=[]):
        self.stores = stores
        self._initStores()
        self.al = adjList(stores)
        self.addEdges()

    def createStore(self, storeID): # pass in a list of 3 rooms
        rooms = []
        for i in range(0,3):
            rooms.append(Room(i, (storeID, i)))
        self.stores.append(Store(rooms, storeID, COLOURS[i]))

    def createCentreStore(self, storeID=4):
        rooms = []
        for i in range(0,5):
            rooms.append(Room(i, (storeID, i)))
        self.stores.append(Store(rooms, storeID, "None"))

    def _initStores(self):
        for i in range(0,4):
            self.createStore(i)
        self.createCentreStore(4) # This is here because the centre room has 5 rooms instead of 3. 
        for j in range(5,9):
            self.createStore(j)
        
    def returnStores(self):
        out = []
        for store in self.stores:
            out.append(store.storeID)
        return out

    def addEdges(self): # Adds edges (left to right, top to bottom on the image)
        self.al.addEdge((0,0),(0,1))
        self.al.addEdge((0,0),(3,1))
        self.al.addEdge((0,1),(0,2))
        self.al.addEdge((0,2),(1,0))
        self.al.addEdge((1,0),(1,1))
        self.al.addEdge((1,0),(2,0))
        self.al.addEdge((1,1),(1,2))
        self.al.addEdge((1,1),(2,0))
        self.al.addEdge((1,2),(2,0))
        self.al.addEdge((1,2),(2,1))
        self.al.addEdge((2,0),(2,1))
        self.al.addEdge((2,0),(2,2))
        self.al.addEdge((2,1),(2,2))
        self.al.addEdge((2,1),(5,0))
        self.al.addEdge((2,2),(5,0))
        self.al.addEdge((3,0),(3,1))
        self.al.addEdge((3,0),(3,2))
        self.al.addEdge((3,1),(4,0))
        self.al.addEdge((3,2),(4,0))
        self.al.addEdge((3,2),(6,0))
        self.al.addEdge((3,2),(6,1))
        self.al.addEdge((3,2),(6,2))
        self.al.addEdge((4,0),(4,2))
        self.al.addEdge((4,1),(4,2))
        self.al.addEdge((4,2),(4,4))
        self.al.addEdge((4,2),(4,3))
        self.al.addEdge((4,3),(7,0))
        self.al.addEdge((4,3),(7,2))
        self.al.addEdge((4,4),(5,0))
        self.al.addEdge((4,4),(5,1))
        self.al.addEdge((5,0),(5,1))
        self.al.addEdge((5,0),(5,2))
        self.al.addEdge((5,1),(5,2))
        self.al.addEdge((5,1),(8,0))
        self.al.addEdge((5,1),(8,2))
        self.al.addEdge((5,2),(5,1))
        self.al.addEdge((6,0),(6,1))
        self.al.addEdge((6,1),(6,2))
        self.al.addEdge((6,2),(7,0))
        self.al.addEdge((6,2),(7,1))
        self.al.addEdge((7,0),(7,1))
        self.al.addEdge((7,0),(7,2))
        self.al.addEdge((7,1),(7,2))
        self.al.addEdge((7,2),(8,0))
        self.al.addEdge((7,2),(8,1))
        self.al.addEdge((8,0),(8,1))
        self.al.addEdge((8,0),(8,2))
        self.al.addEdge((8,1),(8,2))
    
    def addZombie(self, coords):
        # A* to find next room? (Justify with "useful to have in case of further development / zombies being able to move differently in another gamemode")
        self.stores[coords[0]].rooms[coords[1]].setzombie(True)
        if coords[0] == 4:
            pass # take 1 from the barricade.
    
    def shortestPath(self, startCoords, endCoords=(4,2)):
        endCoords = endCoords
        previousNodes = {} # previous node in path
        distances = {} # distances travelled to get to a certain node
        pathCompleted = {} # which paths are completed
        rooms = list(self.al.returnAdjList().keys())
        shortestDistRoom = (0,0)

        for room in rooms:
            pathCompleted[room] = False
            distances[room] = -1
            previousNodes[room] = None
        
        distances[startCoords] = 0

        while pathCompleted[endCoords] == False:
        # for i in range(2):
            shortestDist = float('inf')
            
            for room in rooms:
                # if a node has not been expanded and it has the shortest distance remaining, we select it as the current room. 
                if pathCompleted[room] == False and distances[room] < shortestDist and distances[room] != -1:
                    shortestDist = distances[room]
                    shortestDistRoom = room

            pathCompleted[shortestDistRoom] = True
            connectedRooms = self.al.returnMoves(shortestDistRoom)

            for room in connectedRooms: # expand the current room by iterating through the rooms connected to it. 
                if pathCompleted[room] == False:
                    if distances[room] == -1 or (distances[shortestDistRoom] + 1 < distances[room]):
                        distances[room] = distances[shortestDistRoom] + 1
                        previousNodes[room] = shortestDistRoom
            
        print(distances[endCoords])
        room = endCoords
        path = []
        while room != startCoords:
            path.insert(0, room)
            room = previousNodes[room]
        
        print(path)
