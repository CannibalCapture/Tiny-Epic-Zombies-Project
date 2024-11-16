from .player import Player

class GameManager:
    def __init__(self, map, players={}):
        self.players = players # players is a dictionary with key=playerID, value=playerObject
        self.map = map
        self.listeners = []

    def add_listener(self, listener):
        self.listeners.append(listener)
    
    def send_event(self, event):
        for listener in self.listeners:
            listener.on_event(event)

    def createPlayer(self, name, playerID, colour, character, coords):
        player = Player(name, playerID, colour, character, coords)
        self.players[playerID] = player
        storeID = coords[0]
        room = coords[1]
        player.room = coords # coords (coordinates) will be in the form (storeID, room)
        # Adding a player as a listener to listen for the createPlayer method doesnt work (for somewhat obvious reasons).

    def movePlayer(self, newCoords, player): # newCoords is a tuple containing the storeID and the room in that store.
        oldStoreID = player.coords[0]
        oldRoom = player.coords[1]
        newStoreID = newCoords[0]
        newRoom = newCoords[1]
        self.map.stores[oldStoreID].rooms[oldRoom].removePlayer(player) # remove player from old room
        self.map.stores[newStoreID].rooms[newRoom].addPlayer(player) # add player to new room
        player.move(newCoords) # update player's coordinates attributes
        event = {"type":"PLAYER MOVED", "playerID":player.playerID, "coords":player.coords}
        self.send_event(event)