from .player import Player
from .listener import Listener
from .eventgenerator import EventGenerator
from .map import Map
from .deckmanager import DeckManager
from .inputmanager import InputManager
from .gamerenderer import GameRenderer
from .helperfunctions.deserialisers import deserializeGame
from .button import AttackButton, MoveButton, OpenCardButton, EndTurnButton

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
        self.player = None
        self.turnEnded = False
        self.movesRemaining = 0
        self.mode = "move"
        self.map = Map()
        self.dm = DeckManager()
        self.im = InputManager()
        self.renderer = GameRenderer()
        self._initListeners()
        self._initGame()
    
    def on_event(self, event):
        if event['type'] == 'PLAYER DIE':
            self.respawns -= 1
            if self.respawns < 0:
                pass # check if game is over
            else:
                self.players[event['playerID']].reset()
        
    def setMode(self, mode):
        self.mode = mode
        event = {'type':'MODE CHANGE', 'mode':mode}
        self.send_event(event)

    def onClick(self, pos):
        coll = self.im.collisions(pos)
        lcr = coll["lastClickedRoom"]
        mode = coll["mode"]
        type = coll["type"]

        # if they clicked on a room
        if lcr:
            # and attack mode is on
            if self.mode == "attack":
                if lcr == self.player.getCoords():
                    self.playerMelee(self.player)
                else:
                    self.playerRanged(self.player, lcr)
            else:
                self.movePlayer(self.player, lcr)

        if mode:
            self.setMode(mode)

        if type:
            dict = {'type':type}
            if dict['type'] == 'END TURN':
                self.zombieTurn()
                self.nextTurn()
            self.send_event(dict)

    def zombieTurn(self):
        zombies = 1 # zombies is the number of zombies added to each store which matches the type of noise the player made
        routes = []

        storeColour = self.player.getCoords()[0]
        storeColour = self.map.getStores()[storeColour].getNoiseColour() # gets the colour of the store the player is currently in
        lastNoise = 'PURPLE' # noise made by the player *NOT CURRENTLY IMPLEMENTED*
        if storeColour == lastNoise:
            zombies = 2
        
        storesLst = self.map.getStores()
        for store in storesLst:
            if storeColour == None:
                break
            if store.getNoiseColour() == storeColour:
                sp = self.map.shortestPath((store.getStoreID(), 0), zombie=True)
                routes.append(sp)
        for i in range(zombies):
            spawnLocations = []
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
                    print("deplete barricade") # deplete the barricade
                else:
                    self.map.addZombie(coord)
                if coord != self.getPlayer(self.turn).getCoords(): # if the zombie spawns on a player
                    pass # overrun
        return

    def nextTurn(self):
        self.movesRemaining = self.player.getMoves()
        if self.turn == len(self.players) - 1:
            self.turn = 0
        else:
            self.turn += 1
        self.player = self.getPlayer(self.turn)
        event = {'type':'TURN CHANGE', 'turn':self.turn}
        self.send_event(event)
        self.turnEnded = False

    def _initListeners(self):
        self.add_listener(self.renderer)
        self.add_listener(self.im)

    def _initGame(self):
        # players = int(input("How many players? [2/3/4]\n"))
        chars = ["teenager", "doctor"]
        players = 2
        for i in range(players):
            # name = input(f"What is player {i}'s name?\n")
            name = f"Toby{i}"
            char = chars[i]
            self.createPlayer(name, i, "PURPLE", char, tuple(deserializeGame()["constants"]["spawn"]))
        
        self.setMode("move")
        
        self.player = self.players[0]
        self.nextTurn()
        self.addAttackButton()
        self.addMoveButton()
        self.addOpenCardButton()
        self.addEndTurnButton()
        self.renderer.addMap(self.map)

    def addAttackButton(self):
        attackButton = AttackButton()
        self.renderer.addButton(attackButton)
        self.im.addButton(attackButton)
        self.add_listener(attackButton)
        attackButton.enable()

    def addMoveButton(self):
        moveButton = MoveButton()
        self.renderer.addButton(moveButton)
        self.im.addButton(moveButton)
        self.add_listener(moveButton)
        moveButton.enable()
    
    def addEndTurnButton(self):
        etButton = EndTurnButton()
        self.renderer.addButton(etButton)
        self.im.addButton(etButton)
        self.add_listener(etButton)

    def addOpenCardButton(self):
        ocButton = OpenCardButton()
        self.renderer.addButton(ocButton)
        self.im.addButton(ocButton)
        self.add_listener(ocButton)
        ocButton.enable()

    def createPlayer(self, name, playerID, colour, character, coords):
        player = Player(name, playerID, colour, character, coords)
        self.players[playerID] = player
        player.move(coords) # coordinates will be in the form (storeID, room)
        self.add_listener(player)
        player.add_listener(self)
        self.renderer.addPlayer(player)
        self.updateMovementOptions(player)

    def movePlayer(self, player, newCoords): # newCoords is a tuple containing the storeID and the room in that store.
        if self.map.al.validatePlayerMove(player, newCoords) and self.movesRemaining != 0:
            oldStoreID, oldRoom = player.coords[0], player.coords[1]
            newStoreID, newRoom = newCoords[0], newCoords[1]
            self.map.stores[oldStoreID].rooms[oldRoom].removePlayer(player) # remove player from old room
            self.map.stores[newStoreID].rooms[newRoom].addPlayer(player) # add player to new room

            player.move(newCoords) # update player's coordinates attributes
            self.updateMovementOptions(player)

            self.movesRemaining -= 1
            event = {"type":"PLAYER MOVED", "playerID":player.playerID, "coords":player.coords, "moves":self.movesRemaining}
            self.send_event(event)

        else:
            print("Invalid move")

    def playerMelee(self, player):
        room = self.map.getRoom(player.getCoords())
        if room.getZombie():
            player.meleeAttack()
            self.map.removeZombie(room.getCoords())
            event = {"type":"PLAYER MELEE", "playerID":player.playerID, "coords":player.getCoords(), "moves":self.movesRemaining}
            self.send_event(event)
            self.mode = "move"
        else:
            print("Attack failed: No available target")
    
    def playerRanged(self, player, coords):
        room = self.map.getRoom(coords)
        if room.getZombie() and (coords in player.getMovementOptions() or coords == player.getCoords()):
            player.rangedAttack()
            self.map.removeZombie(coords)
            event = {"type":"PLAYER RANGED", "playerID":player.playerID, "coords":coords, "moves":self.movesRemaining}
            self.send_event(event)
            self.mode = "move"
        else:
            print("Attack failed: Ranged")

    def playerSearchStore(self, player):
        player.equipMelee(self.dm.drawSearch())
        noiseColour = self.map.stores[player.coords[0]].noiseColour
        event = {"type":f"{noiseColour} NOISE", "playerID":player.playerID, "coords":player.coords}
        self.send_event(event)

    def renderGameScreen(self):
        self.renderer.renderGameBoard()

    def playerCoords(self):
        coords = [player.getCoords() for player in self.players]
        out = []
        for coord in coords:
            out.append(self.map.getRoom(coord))

    def addZombie(self, coords):
        self.map.addZombie(coords)
    
    def updateMovementOptions(self, player):
        player.setMovementOptions(self.map.getMovementOptions(player.getCoords()))
    
    def disableButton(self, button):
        self.buttons[button].disable()

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