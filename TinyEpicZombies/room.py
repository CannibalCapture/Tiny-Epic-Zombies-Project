class Room:
    def __init__(self, roomID, coords, zombie=False, ammoRoom=False):
        self.roomID = roomID
        self.players = []
        self.zombie = zombie
        self.ammoRoom = ammoRoom
        self. coords = coords
        self.playersThisTurn = set()

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