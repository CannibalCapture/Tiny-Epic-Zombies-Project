from .player import Player
from .listener import Listener
from .eventGenerator import EventGenerator
from .constants import COLOURS, CENTRE_ROOM

class GameManager(Listener, EventGenerator):
    def __init__(self, map, players=dict()):
        Listener.__init__(self)
        EventGenerator.__init__(self)
        self.players = players # players is a dictionary with key=playerID, value=playerObject
        self.map = map
        self.respawns = 3
        self._initGame()

    def on_event(self, event):
        super().on_event(event)
        if event['type'] == 'PLAYER DIE':
            self.respawns -= 1
            if self.respawns < 0:
                pass # check if game is over
            else:
                self.players[event['playerID']].reset()

    def _initGame(self):
        players = int(input("How many players? [1/2/3/4]\n"))
        for i in range(players):
            name = input(f"What is {COLOURS[i]} player's name?\n")
            self.createPlayer(name, i, COLOURS[i], "character", CENTRE_ROOM)

    def createPlayer(self, name, playerID, colour, character, coords):
        player = Player(name, playerID, colour, character, coords)
        self.players[playerID] = player
        player.room = coords # coordinates will be in the form (storeID, room)
        player.add_listener(self)

    def movePlayer(self, newCoords, player): # newCoords is a tuple containing the storeID and the room in that store.
        if self.map.al.validatePlayerMove(player, newCoords):
            oldStoreID = player.coords[0]
            oldRoom = player.coords[1]
            newStoreID = newCoords[0]
            newRoom = newCoords[1]
            self.map.stores[oldStoreID].rooms[oldRoom].removePlayer(player) # remove player from old room
            self.map.stores[newStoreID].rooms[newRoom].addPlayer(player) # add player to new room

            player.move(newCoords) # update player's coordinates attributes

            event = {"type":"PLAYER MOVED", "playerID":player.playerID, "coords":player.coords}
            self.send_event(event)

        else:
            print("Invalid move")


    def playerMelee(self, player):
        cs = player.coords[0] # Current store
        cr = player.coords[1] # Current room within the store
        if self.map.stores[cs].rooms[cr].zombie:
            player.meleeAttack()
            self.map.stores[cs].rooms[cr].setZombie(False)
            event = {"type":"PLAYER MELEE", "playerID":player.playerID, "coords":player.coords}
            self.send_event(event)
        else:
            print("Attack failed: No available target")
            print(self.map.stores[cs].rooms[cr].coords)
    
    def playerRanged(self, player, coords):
        s = player.coords[0] # Store being shot into
        r = player.coords[1] # Room being shot into
        if self.map.al.validatePlayerMove(player, coords) and self.map.stores[s].rooms[r].zombie:
            player.rangedAttack()
            self.map.stores[s].rooms[r].setZombie(False)
            event = {"type":"PLAYER RANGED", "playerID":player.playerID, "coords":coords}
            self.send_event(event)
        else:
            print("Attack failed: Ranged")

