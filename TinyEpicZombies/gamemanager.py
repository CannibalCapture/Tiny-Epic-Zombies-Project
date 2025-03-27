from .player import Player
from .listener import Listener
from .eventGenerator import EventGenerator
from .map import Map
from .deckmanager import DeckManager
from .inputmanager import InputManager
from .gamerenderer import GameRenderer
from .helperfunctions.deserialisers import deserializeGame
from .button import AttackButton, MoveButton, OpenCardButton, EndTurnButton, StoreCardsButton, PickupStoreCardsButton, ExitMenuButton, TestButton, InventoryButton
from .tank import Tank

class GameManager(Listener, EventGenerator):

    instance = None

    def getInstance():
        if GameManager.instance == None:
            GameManager.instance = GameManager()
        return GameManager.instance

    def __init__(self, respawns=3, players=dict()):
        Listener.__init__(self)
        EventGenerator.__init__(self)
        self.players = players # players is a dictionary with key=player ID, value=playerObject
        self.respawns = respawns
        self.turn = 0 # player ID representing which player's turn it is currently
        self.runGame = True
        self.player = None
        self.turnEnded = False
        self.movesRemaining = 0
        self.barricade = 0
        self.tanksRemaining = 4
        self.noise = None
        self.tanks = []
        self.selectedTank = None
        self.mode = "move"
        self.map = Map()
        self.dm = DeckManager()
        self.im = InputManager()
        self.renderer = GameRenderer()
        self._initListeners()
        self.addButtons()
        self.renderer.addMap(self.map)
        self.im.addMap(self.map)
        self._initTanks()

    def deserialize(dict):
        gameManager = GameManager.getInstance()
        gameManager.setRenderer(GameRenderer.deserialize(dict["renderer"]))

        for player in dict["players"]:
            p = dict["players"][player]
            gameManager.createPlayer(p["name"], p["ID"], p["colour"], p["character"], tuple(p["coords"]))

        gameManager.setMap(Map.deserialize(dict["map"], gameManager))
        gameManager.setDM(DeckManager.deserialize(dict["deckManager"]))
        gameManager.setIM(InputManager.deserialize(dict["inputManager"]))

        gameManager.setTanks([Tank.deserialize(tank) for tank in dict["tanks"]])
        gameManager._initListeners()
        gameManager.addButtons()
        gameManager.renderer.addMap(gameManager.map)
        gameManager.im.addMap(gameManager.map)
        gameManager._initTanks()
        gameManager.player = gameManager.players[0]
        gameManager.nextTurn()

    def serialize(self):
        dict = {
            "players": { id: player.serialize() for id, player in self.players.items() },
            "turn": self.turn,
            "respawns": self.respawns,
            "movesRemaining": self.movesRemaining,
            "noise": self.noise,
            "tanks": [tank.serialize() for tank in self.tanks],
            "map": self.map.serialize(),
            "renderer": self.renderer.serialize(),
            "deckManager": self.dm.serialize(),
            "inputManager": self.im.serialize()
        }
        return dict
    
    def on_event(self, event):
        if event['type'] == 'PLAYER DIE':
            self.respawns -= 1
            if self.respawns < 0:
                pass # check if game is over
            else:
                self.players[event['ID']].reset()

    def setMode(self, mode):
        self.mode = mode
        event = {'type':'MODE CHANGE', 'mode':mode}
        self.send_event(event)

    def onClick(self, pos):
        if not self.runGame:
            return
        coll = self.im.collisions(pos)
        try:
            keys = [*coll]
        except:
            keys = []

        if "mode" in keys:
            mode = coll["mode"]
            self.setMode(mode)
            if self.mode == "move tank":
                self.selectedTank = coll["tank"]
                self.renderer.setSelectedTank(coll["tank"])

        # if they clicked on a room
        if "lastClickedRoom" in keys:
            lcr = coll["lastClickedRoom"]
            if self.mode == "attack":
                if lcr == self.player.getCoords():
                    self.playerMelee(self.player)
                else:
                    self.playerRanged(self.player, lcr)
            elif self.mode == "move":
                self.movePlayer(self.player, lcr)
            elif self.mode == "move tank":
                self.moveTank(lcr)
        
        if "lastClickedCard" in keys:
            lcc = coll['lastClickedCard']
            if lcc.getType() == "MELEE WEAPON":
                self.player.setMeleeWeapon(lcc)
            elif lcc.getType() == "RANGED WEAPON":
                self.player.setRangedWeapon(lcc)
            store = self.map.getStores()[self.player.getCoords()[0]]
            store.removeCardByValue(lcc)

        if "type" in keys:
            if coll['type'] == 'END TURN':
                self.playerSearchStore()
                self.zombieTurn()
                self.nextTurn()
            
            if coll['type'] == 'EXIT MENU':
                self.exitMenu()
            
            if coll['type'] == 'PICKUP STORE CARDS':
                self.pickupStoreCards()

            if coll['type'] == 'OPEN INVENTORY':
                pass

            if coll['type'] == 'GAME OVER':
                pass
            
            if coll['type'] == 'TEST BUTTON': ###########################################################################
                for tank in self.tanks:
                    print(tank.getPos())
                    print(tank.getRect())
                    print(self.tanksRemaining)
            
            self.send_event(coll)
        

    def onKeyPress(self, key):
        pass

    def gameOver(self, wl):
        if wl:
            print("PLAYERS WIN")
        else:
            print("ZOMBIES WIN")

        self.runGame = False
        
    def pickupStoreCards(self):
        player = self.player
        store = self.map.getStores()[player.getCoords()[0]]
        bpCards = store.removeBackpackCards()
        for card in bpCards:
            player.addCard(card)

    def exitMenu(self):
        pass

    def zombieTurn(self):
        zombies = 1 # zombies is the number of zombies added to each store which matches the type of noise the player made
        routes = []

        storeColour = self.player.getCoords()[0]
        storeColour = self.map.getStores()[storeColour].getNoiseColour() # gets the colour of the store the player is currently in
        if storeColour == self.noise:
            zombies = 2
        
        storesLst = self.map.getStores()
        for store in storesLst:
            if storeColour == None:
                break
            if store.getNoiseColour() == storeColour:
                sp = self.map.shortestPath((store.getID(), 0), zombie=True)
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
                    self.barricade -= 1
                    self.renderer.updateBarricade(self.barricade)
                else:
                    self.map.addZombie(coord)
                if coord != self.getPlayer(self.turn).getCoords(): # if the zombie spawns on a player
                    self.player.takeDamage(1)
        return

    def nextTurn(self):
        self.movesRemaining = self.player.getMoves()
        if self.turn == len(self.players) - 1:
            self.turn = 0
        else:
            self.turn += 1
        self.player = self.getPlayer(self.turn)
        event = {'type':'TURN CHANGE', 'turn':self.turn, 'player':self.player}
        self.send_event(event)
        self.mode = "move"
        self.turnEnded = False

    def revealCard(self):
        pass

    def _initListeners(self):
        self.add_listener(self.renderer)
        self.add_listener(self.im)

    def initGame(self, selectedChars):
        for i in range(len(selectedChars)):
            name = f"Player {i}"
            char = selectedChars[i]
            self.createPlayer(name, i, "PURPLE", char, tuple(deserializeGame()["constants"]["spawn"]))
        
        self.setMode("move")
        
        self.player = self.players[0]
        self.nextTurn()

    def _initTanks(self):
        tankSpawns = [(0,0), (2,2), (6,2), (8,0)]
        for i in range(4):
            tank = Tank(i, tankSpawns[i])
            self.renderer.addTank(tank)
            self.im.addTank(tank)
            self.updateMovementOptions(tank)
            self.tanks.append(tank)

    def addButton(self, button, store=None):
        if button == "attack":
            button = AttackButton()
        elif button == "move":
            button = MoveButton()
        elif button == "endTurn":
            button = EndTurnButton()
        elif button == "openCard":
            button = OpenCardButton()
        elif button == "pickupStoreCards":
            button = PickupStoreCardsButton()
        elif button == "showStoreCards":
            button = StoreCardsButton(store)
        elif button == "exitMenu":
            button = ExitMenuButton()
        elif button == "test":
            button = TestButton()
        elif button == "inventory":
            button = InventoryButton()

        self.renderer.addButton(button)
        self.im.addButton(button)
        self.add_listener(button)

    def addButtons(self):
        self.addButton("attack")
        self.addButton("move")
        self.addButton("endTurn")
        self.addButton("openCard")
        self.addButton("pickupStoreCards")
        self.addButton("exitMenu")
        self.addButton("test")
        self.addButton("inventory")
        for i in range(9):
            self.addButton("showStoreCards", i)
    
    def createPlayer(self, name, ID, colour, character, coords):
        player = Player(name, ID, colour, character, coords)
        self.players[ID] = player
        player.move(coords) # coordinates will be in the form (ID, room)
        self.add_listener(player)
        player.add_listener(self)
        self.renderer.addPlayer(player)
        self.updateMovementOptions(player)

    def playerSearchStore(self): # this is the player drawing a card and putting it face up next to the store they ended their turn in
        player = self.player
        coords = player.getCoords()
        card = self.dm.drawSearch()
        if card == 0:
            event = {'type':'GAME OVER'}
            self.send_event(event)
            self.gameOver()
            return
        self.map.getStores()[coords[0]].addCard(card)
        self.noise = card.getColour()
        event = {"type":"NOISE","colour":card.getColour(), "ID":player.getID(), "coords":coords, "card":card.getID()}
        self.send_event(event)

    def movePlayer(self, player, newCoords): # newCoords is a tuple containing the ID and the room in that store.
        if self.map.al.validatePlayerMove(player, newCoords) and self.movesRemaining != 0:
            oldStoreID, oldRoom = player.coords[0], player.coords[1]
            newStoreID, newRoom = newCoords[0], newCoords[1]
            self.map.stores[oldStoreID].rooms[oldRoom].removePlayer(player) # remove player from old room
            self.map.stores[newStoreID].rooms[newRoom].addPlayer(player) # add player to new room

            player.move(newCoords) # update player's coordinates attributes
            self.updateMovementOptions(player)

            self.movesRemaining -= 1
            event = {"type":"PLAYER MOVED", "ID":player.ID, "coords":player.coords, "moves":self.movesRemaining}
            self.send_event(event)

        else:
            return "invalid move"
    
    def moveTank(self, newCoords):
        tank = self.tanks[self.selectedTank]
        if self.map.al.validatePlayerMove(tank, newCoords) and self.movesRemaining != 0:
            tank.setCoords(newCoords)
            self.updateMovementOptions(tank)
        
            self.movesRemaining -= 1
            event = {"type":"TANK MOVED", "ID":tank.getID(), "coords":tank.getCoords(), "moves":self.movesRemaining}
            self.send_event(event)

            if newCoords == (4,2):
                self.tanksRemaining -= 1
                if self.tanksRemaining == 0:
                    self.gameOver(1)

    def playerMelee(self, player):
        room = self.map.getRoom(player.getCoords())
        if room.getZombie():
            player.meleeAttack()
            self.map.removeZombie(room.getCoords())
            event = {"type":"PLAYER MELEE", "ID":player.ID, "coords":player.getCoords(), "moves":self.movesRemaining}
            self.send_event(event)
            self.mode = "move"
        else:
            return "Attack failed: No available target"
    
    def playerRanged(self, player, coords):
        room = self.map.getRoom(coords)
        if room.getZombie() and (coords in player.getMovementOptions() or coords == player.getCoords()):
            player.rangedAttack()
            self.map.removeZombie(coords)
            event = {"type":"PLAYER RANGED", "ID":player.ID, "coords":coords, "moves":self.movesRemaining}
            self.send_event(event)
            self.mode = "move"
        else:
            return "Attack failed: Ranged"

    def renderGameScreen(self):
        if self.runGame:
            self.renderer.renderGameBoard()

    def addZombie(self, coords):
        self.map.addZombie(coords)
    
    def updateMovementOptions(self, player):
        player.setMovementOptions(self.map.getMovementOptions(player.getCoords()))

    def getPlayer(self, ID):
        return self.players[ID]

    def getMap(self):
        return self.map
    
    def setTanks(self, lstVal):
        self.tanks = lstVal
    
    def setIM(self, im):
        self.im = im

    def setPlayers(self, playersDict):
        self.players = playersDict
    
    def setMap(self, map):
        self.map = map
    
    def setRenderer(self, renderer):
        self.renderer = renderer

    def setRunGame(self, val):
        self.runGame = val

    def getRunGame(self):
        return self.runGame
    
    def setDM(self, dm):
        self.dm = dm