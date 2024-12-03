from .player import Player
from .listener import Listener
from .eventgenerator import EventGenerator
from .map import Map
from .deckmanager import DeckManager
from .zombieplayer import ZombiePlayer
from .constants import COLOURS, CENTRE_ROOM

class GameManager(Listener, EventGenerator):
    def __init__(self, respawns=3, players=dict()):
        Listener.__init__(self)
        EventGenerator.__init__(self)
        self.players = players # players is a dictionary with key=playerID, value=playerObject
        self.map = Map()
        self.dm = DeckManager()
        self.zp = ZombiePlayer()
        self.respawns = respawns
        self._initGame()
        self._initListeners()

    def on_event(self, event):
        super().on_event(event)
        if event['type'] == 'PLAYER DIE':
            self.respawns -= 1
            if self.respawns < 0:
                pass # check if game is over
            else:
                self.players[event['playerID']].reset()
        
    def playerTurn(self, player):
        for move in range(1, 4):
            print(f"Enter the coordinates you would like to move to. ({move}/3)")
            a = int(input("Enter store\n"))
            b = int(input("Enter room\n"))
            moveCoords = (a,b)
            self.movePlayer(player, moveCoords)

    def _initListeners(self):
        self.add_listener(self.zp)

    def _initGame(self):
        players = int(input("How many players? [2/3/4]\n"))
        for i in range(players):
            name = input(f"What is {COLOURS[i]} player's name?\n")
            self.createPlayer(name, i, COLOURS[i], "character", CENTRE_ROOM)
        # self.createPlayer("toby", 0, "BLUE", "Medic", (0,0))

    def createPlayer(self, name, playerID, colour, character, coords):
        player = Player(name, playerID, colour, character, coords)
        self.players[playerID] = player
        player.move(coords) # coordinates will be in the form (storeID, room)
        self.add_listener(player)
        player.add_listener(self)

    def movePlayer(self, player, newCoords): # newCoords is a tuple containing the storeID and the room in that store.
        if self.map.al.validatePlayerMove(player, newCoords):
            oldStoreID, oldRoom = player.coords[0], player.coords[1]
            newStoreID, newRoom = newCoords[0], newCoords[1]
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

    def playerSearchStore(self, player):
        player.equipMelee(self.dm.drawSearch())
        noiseColour = self.map.stores[player.coords[0]].noiseColour
        event = {"type":f"{noiseColour} NOISE", "playerID":player.playerID, "coords":player.coords}
        self.send_event(event)
    
    def addZombie(self, coords):
        self.map.addZombie(coords)