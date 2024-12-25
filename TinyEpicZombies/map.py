from .adjlist import AdjList
from .store import Store
from .room import Room
from .helperfunctions.deserialisers import deserializeStore, deserializeRoom

# To access the room at coordinates (a,b): map.stores[a].rooms[b]

class Map: # map will manage the rooms

    def __init__(self, stores=[]):
        self.stores = stores
        self._initStores()
        self.al = AdjList(stores)
        self.addEdges()

    def serialize(self):
        dict = {
            "stores": [store.serialize() for store in self.stores]
        }
        return dict
    
    def deserialize(dict):
        return Map([store.deserialize() for store in dict["stores"]])

    def createStore(self, storeID): # pass in a list of 3 rooms
        rooms = []
        ds = deserializeStore(storeID)
        for i in range(0,3):
            rooms.append(Room(i, (storeID, i)))
        self.stores.append(Store(rooms, storeID, ds["colour"], ds["image"], tuple(ds["tl"])))

    def createCentreStore(self, storeID=4):
        rooms = []
        for i in range(0,5):
            ds = deserializeStore(4)
            rooms.append(Room(i, (storeID, i)))
        self.stores.append(Store(rooms, storeID, "None", ds["image"], ds["tl"]))

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
        self.al.addEdge((0,0), [(0,1), (0,2)])
        self.al.addEdge((0,1), [(0,0), (0,2), (3,1), (3,2)])
        self.al.addEdge((0,2), [(0,0), (0,1), (3,2), (1,0), (1,1), (1,2)])

        self.al.addEdge((1,0), [(0,2), (1,1), (2,0)])
        self.al.addEdge((1,1), [(1,0), (0,2), (1,2), (2,0), (2,1)])
        self.al.addEdge((1,2), [(1,1), (0,2), (2,1), (4,1)])

        self.al.addEdge((2,0), [(1,0), (1,1), (1,2), (2,1), (2,2)])
        self.al.addEdge((2,1), [(1,1), (1,2), (2,0), (2,2), (5,0)])
        self.al.addEdge((2,2), [(2,0), (2,1), (5,0)])

        self.al.addEdge((3,0), [(3,1), (4,0), (6,0), (6,2)])
        self.al.addEdge((3,1), [(3,0), (3,2), (4,0), (0,1)])
        self.al.addEdge((3,2), [(3,1), (4,0), (0,1), (0,2)])

        self.al.addEdge((4,0), [(3,0), (3,1), (3,2), (4,1), (4,2), (4,3)])
        self.al.addEdge((4,1), [(1,2), (4,0), (4,2), (4,4)])
        self.al.addEdge((4,2), [(4,0), (4,1), (4,3), (4,4)])
        self.al.addEdge((4,3), [(7,1), (7,2), (4,0), (4,2), (4,4)])
        self.al.addEdge((4,4), [(5,0), (5,2), (4,1), (4,2), (4,3)])

        self.al.addEdge((5,0), [(2,1), (2,2), (5,1), (5,2), (4,4)])
        self.al.addEdge((5,1), [(5,0), (5,2)])
        self.al.addEdge((5,2), [(5,0), (5,1), (4,4), (8,0), (8,1), (8,2)])

        self.al.addEdge((6,0), [(3,0), (6,1), (6,2), (7,0), (7,1)])
        self.al.addEdge((6,1), [(6,0), (6,2)])
        self.al.addEdge((6,2), [(6,0), (6,1), (3,0)])

        self.al.addEdge((7,0), [(6,0), (7,1)])
        self.al.addEdge((7,1), [(6,0), (7,0), (7,2), (4,3), (8,2)])
        self.al.addEdge((7,2), [(7,1), (4,3), (8,2)])

        self.al.addEdge((8,0), [(5,2), (8,1)])
        self.al.addEdge((8,1), [(5,2), (8,0), (8,2)])
        self.al.addEdge((8,2), [(5,2), (8,1), (7,1), (7,2)])
    
    def addZombie(self, coords):
        # A* to find next room? (Justify with "useful to have in case of further development / zombies being able to move differently in another gamemode")
        self.stores[coords[0]].rooms[coords[1]].setzombie(True)
        if coords[0] == 4:
            pass # take 1 from the barricade.

    def getAdjList(self):
        return self.al
    
    def shortestPath(self, startCoords, endCoords=(4,2)):
        endCoords = endCoords
        previousNodes = {} # previous node in path
        distances = {} # distances travelled to get to a certain node
        pathCompleted = {} # which paths are completed
        rooms = list(self.al.getAdjList().keys())
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
            connectedRooms = self.al.getMoves(shortestDistRoom)

            for room in connectedRooms: # expand the current room by iterating through the rooms connected to it. 
                if pathCompleted[room] == False:
                    if distances[room] == -1 or (distances[shortestDistRoom] + 1 < distances[room]):
                        distances[room] = distances[shortestDistRoom] + 1
                        previousNodes[room] = shortestDistRoom
            
        room = endCoords
        path = []
        while room != startCoords:
            path.insert(0, room)
            room = previousNodes[room]
        
        return(path, distances[endCoords])
