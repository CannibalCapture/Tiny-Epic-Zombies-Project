from .player import Player

class GameManager:
    def __init__(self, map, players={}):
        self.players = players # players is a dictionary with key=playerID, value=playerObject
        self.map = map

    def createPlayer(self, name, playerID, colour, character, coords):
        player = Player(name, playerID, colour, character, coords)
        self.players[playerID] = player
        storeID = coords[0]
        room = coords[1]
        player.room = coords # coords (coordinates) will be in the form (storeID, room)

    def movePlayer(self, newCoords, player):
        oldStoreID = player.coords[0]
        oldRoom = player.coords[1]
        newStoreID = newCoords[0]
        newRoom = newCoords[1]
        self.map.stores[oldStoreID].rooms[oldRoom].removePlayer(player)
        self.map.stores[newStoreID].rooms[newRoom].addPlayer(player)
        player.move(newCoords)