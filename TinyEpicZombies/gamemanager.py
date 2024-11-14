from player import Player

class GameManager:
    def __init__(self, map, players={}):
        self.players = players # players is a dictionary with key=playerID, value=playerObject
        self.map = map

    def addPlayer(self, name, playerID, colour, character, coords):
        player = Player(name, playerID, colour, character)
        self.players[playerID] = player
        storeID = coords[0]
        room = coords[1]
        player.room = coords # coords (coordinates) will be in the form (storeID, room)
        print(self.players)