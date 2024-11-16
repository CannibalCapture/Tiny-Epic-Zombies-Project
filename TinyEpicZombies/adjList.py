class adjList: # The graph is represented by an adjacency list.
    def __init__(self, stores):
        self.adjList = {}
        
    
    def addNode(self, roomID):
        self.adjList[roomID] = []

    def addEdge(self, room1ID, room2ID): # adds an edge between room1 and room2
        self.adjList[room1ID].append(room2ID)

    def getAdjList(self):
        return self.adjList