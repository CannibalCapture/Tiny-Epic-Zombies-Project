from .gamemanager import GameManager

class Room:
    def __init__(self, roomID, coords, players=[], zombie=False, ammoRoom=False):
        self.roomID = roomID
        self.players = players
        self.zombie = zombie
        self.ammoRoom = ammoRoom
        self.coords = coords
        self.playersThisTurn = set() # player ids or player objects?

    def serialize(self):
        dict = {
            "roomID": self.roomID,
            "players": [player.returnID() for player in self.players],
            "zombie": self.zombie,
            "ammoRoom": self.ammoRoom,
            "coords": list(self.coords),
            "playersThisTurn": list(self.playersThisTurn) # do a similar thing as done with serialising players ^
        }

    def deserialize(dict):
        gameManager = GameManager.getInstance()
        # deserialize playersThisTurn
        return Room(dict["roomID"], dict["coords"], [gameManager.getPlayer(playerID) for playerID in dict["players"]], dict["zombie"], dict["ammoRoom"])

    def addPlayer(self, player):
        self.players.append(player)
        if self.ammoRoom and player not in self.playersThisTurn:
            player.changeAmmo(1)
        self.playersThisTurn.add(player)

    def endOfTurn(self):
        self.playersThisTurn.clear()

    def removePlayer(self, player):
        if player in self.players:
            self.players.remove(player)

    def returnPlayers(self):
        return [player.name for player in self.players]
    
    def setZombie(self, value):
        self.zombie = value

    def getZombie(self):
        return self.zombie