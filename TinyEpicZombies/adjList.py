class AdjList: # The graph is represented by an adjacency list.

    def __init__(self, stores):
        self.adjList = {}
        self.createAdjList(stores)

    def createAdjList(self, stores):
        for store in stores:
            for room in store.rooms:
                self.addNode(room.coords)
    
    def addNode(self, coords):
        self.adjList[coords] = []

    def addEdge(self, r1Coords, roomsLst): # adds an edge between room1 and the rooms in roomsLst
        for item in roomsLst:
            try:
                room, store = item[0], item[1]
                self.adjList[r1Coords].append((room, store))
            except:
                pass
        
    def validatePlayerMove(self, player, coords):
        if coords in self.adjList[player.getCoords()]:
            return True
        return False

    def getMoves(self, coords):
        return self.adjList[coords]

    def getAdjList(self):
        return self.adjList