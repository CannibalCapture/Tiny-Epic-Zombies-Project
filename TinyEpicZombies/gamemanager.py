from .player import Player
from .listener import Listener
from .eventgenerator import EventGenerator
from .map import Map
from .deckmanager import DeckManager
from .inputmanager import InputManager
from .gamerenderer import GameRenderer
from .helperfunctions.deserialisers import deserializeGame


class GameManager(Listener, EventGenerator):

    instance = None

    def getInstance():
        if GameManager.instance == None:
            GameManager.instance = GameManager()
        return GameManager.instance

    def __init__(self, respawns=3, players=dict()):
        Listener.__init__(self)
        EventGenerator.__init__(self)
        self.players = players # players is a dictionary with key=playerID, value=playerObject
        self.respawns = respawns
        self.turn = 0 # playerID representing which player's turn it is currently
        self.movesRemaining = 0
        self.map = Map()
        self.dm = DeckManager()
        self.im = InputManager()
        self.renderer = GameRenderer()
        self._initGame()
        self._initListeners()
    
    def serialize(self):
        dict = {
            "players": { id: player.serialize() for id, player in self.players.items() },
            "playerTurn": self.turn,
            "respawns": self.respawns
        }
        return dict

    def deserialize(dict):
        gameManager = GameManager.getInstance()
        gameManager.setPlayers({ id: Player.deserialize(dict["Players"][id]) for id in dict["players"]} )

        gameManager.setMap(Map.deserialize())
        gameManager.setDM(DeckManager.deserialize())

    def on_event(self, event):
        super().on_event(event)

        if event['type'] == 'PLAYER DIE':
            self.respawns -= 1
            if self.respawns < 0:
                pass # check if game is over
            else:
                self.players[event['playerID']].reset()
        
    def playerTurn(self, player=0):
        if self.movesRemaining != 0:
            pass
        else:
            print(self.zombieTurn())

            # zombie turn
            
            self.nextTurn()
            self.movesRemaining = self.players[self.turn].getMoves()

    def zombieTurn(self):
        zombies = 1 # zombies is the number of zombies added to each store which matches the type of noise the player made
        routes = []
        spawnLocations = []

        storeColour = self.players[self.turn].getCoords()[0] # gets ID of store that the player is in
        storeColour = self.map.getStores()[storeColour].getNoiseColour()
        lastNoise = 'PURPLE' # noise made by the player *NOT CURRENTLY IMPLEMENTED*
        if storeColour == lastNoise:
            zombies = 2
        
        storesLst = self.map.getStores()
        for store in storesLst:
            if store.getNoiseColour() == storeColour:
                sp = self.map.shortestPath((store.getStoreID(), 0), zombie=True)
                routes.append(sp)

        for route in routes:
            for coord in route:
                zombieAtCoord = self.map.getStores()[coord[0]].getRooms()[coord[1]].getZombie()
                if zombieAtCoord:
                    pass
                else:
                    break

            spawnLocations.append(coord)

            for coord in spawnLocations:
                if coord == (4,2):
                    pass # deplete the barricade
                else:
                    self.map.getRoom(coord).setZombie(True)

        return 

    def onClick(self, pos):
        coll = self.im.roomCollisions(pos)
        if coll:
            self.movePlayer(self.getPlayer(0), coll)

    def nextTurn(self):
        if self.turn == len(self.players) - 1:
            self.turn = 0
        else:
            self.turn += 1

    def _initListeners(self):
        pass

    def _initGame(self):
        # players = int(input("How many players? [2/3/4]\n"))
        players = 1
        for i in range(players):
            # name = input(f"What is player {i}'s name?\n")
            name = "Toby"
            self.createPlayer(name, i, "BLUE", "character", tuple(deserializeGame()["constants"]["spawn"]))
        
        self.movesRemaining = self.getPlayer(self.turn).getMoves()


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

            self.movesRemaining -= 1


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

    def renderGameScreen(self):
        player = self.getPlayer(self.turn)
        moveOptions = self.getMap().getAdjList().getMoves(player.getCoords())
        self.renderer.renderGameScreen(moveOptions)
        
    def addZombie(self, coords):
        self.map.addZombie(coords)
        # make noise
    
    def givePos(self):
        pass

    def getPlayer(self, playerID):
        return self.players[playerID]

    def getMap(self):
        return self.map

    def setPlayers(self, playersDict):
        self.players = playersDict
    
    def setMap(self, map):
        self.map = map
    
    def setDM(self, dm):
        self.dm = dm