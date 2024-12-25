class Room:
    def __init__(self, roomID, coords, players=[], zombie=False, ammoRoom=False, playersThisTurn=set()):
        self.roomID = roomID
        self.players = players
        self.zombie = zombie
        self.ammoRoom = ammoRoom
        self.coords = coords
        self.playersThisTurn = playersThisTurn

    def serialize(self):
        dict = {
            "roomID": self.roomID,
            "players": self.players,
            "zombie": self.zombie,
            "ammoRoom": self.ammoRoom,
            "coords": list(self.coords),
            "playersThisTurn": self.playersThisTurn
        }
        return dict

    def deserialize(dict):
        return Room(dict["roomID"], tuple(dict["coords"]), dict["players"], dict["zombie"], dict["ammoRoom"], set(dict["playersThisTurn"]))

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