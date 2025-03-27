import os
import json

class Room:
    def __init__(self, roomID, coords, players=[], zombie=False, ammoRoom=False, playersThisTurn=set(), tank=False):
        self.roomID = roomID
        self.players = players
        self.zombie = zombie
        self.tank = tank
        self.ammoRoom = ammoRoom
        self.coords = coords
        self.playersThisTurn = playersThisTurn

    def serialize(self):
        dict = {
            "roomID": self.roomID,
            "players": [player.getID() for player in self.players],
            "zombie": self.zombie,
            "tank": self.tank,
            "ammoRoom": self.ammoRoom,
            "coords": list(self.coords),
            "playersThisTurn": [player.getID() for player in self.playersThisTurn]
        }
        return dict

    def deserialize(dict, gm):
        playersLst = [gm.getPlayer(playerID) for playerID in dict["players"]]
        pttLst = [gm.getPlayer(playerID) for playerID in dict["playersThisTurn"]]
        return Room(dict["roomID"], tuple(dict["coords"]), playersLst, dict["zombie"], dict["ammoRoom"], set(pttLst), dict["tank"])
   
    
    def deserializeRoom(coords):
        store, room = coords[0], coords[1]
        with open(os.path.join("TinyEpicZombies","jsonfiles", "roompoints.json")) as file:
            data = json.loads("".join(file.readlines()))
            return(data["stores"][f"store{store}"]["rooms"][f"room{room}"])


    def addPlayer(self, player):
        self.players.append(player)
        if self.ammoRoom and player not in self.playersThisTurn:
            player.changeAmmo(1)
        self.playersThisTurn.add(player)

    def endOfTurn(self):
        self.playersThisTurn.clear()

    def removePlayer(self, player):
        # print(f"removing {player.getID()} from room")
        # print(f"room contains {', '.join([str(p.getID()) for p in self.players])}")
        if player in self.players:
            self.players.remove(player)
        # print(f"room now contains {', '.join([str(p.getID()) for p in self.players])}")

    def returnPlayers(self):
        return [player.name for player in self.players]
    
    def setZombie(self, value):
        self.zombie = value

    def getZombie(self):
        return self.zombie
    
    def getCoords(self):
        return self.coords
    
    def setTank(self, value):
        self.tank = value

    def getTank(self):
        return self.tank