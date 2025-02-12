from .player import Player
from .listener import Listener
from .eventgenerator import EventGenerator
from .map import Map
from .deckmanager import DeckManager
from .inputmanager import InputManager
from .gamerenderer import GameRenderer
from .helperfunctions.deserialisers import deserializeGame
from .button import AttackButton, MoveButton, OpenCardButton, EndTurnButton, StoreCardsButton, PickupStoreCardsButton, ExitMenuButton, TestButton

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
        self.player = None
        self.turnEnded = False
        self.movesRemaining = 0
        self.noise = None
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
                self.players[event['ID']].reset()
        
    def setMode(self, mode):
        self.mode = mode
        event = {'type':'MODE CHANGE', 'mode':mode}
        self.send_event(event)

    def onClick(self, pos):
        coll = self.im.collisions(pos)
        try:
            keys = [*coll]
        except:
            keys = []

        # if they clicked on a room
        if "lastClickedRoom" in keys: # and attack mode is on
            lcr = coll["lastClickedRoom"]
            if self.mode == "attack":
                if lcr == self.player.getCoords():
                    self.playerMelee(self.player)
                else:
                    self.playerRanged(self.player, lcr)
            else:
                self.movePlayer(self.player, lcr)

        if "mode" in keys:
            mode = coll["mode"]
            self.setMode(mode)

        if "type" in keys:
            if coll['type'] == 'END TURN':
                print("end turn gm")
                self.playerSearchStore()
                self.zombieTurn()
                self.nextTurn()
            
            if coll['type'] == 'PICKUP STORE CARDS':
                self.pickupStoreCards()
            
            if coll['type'] == 'TEST BUTTON': #################################################################
                # store = self.renderer.map.getStores()[self.renderer.shownPickupCards]
                # print(store.getCards(), len(store.getCards()))
                pass
            
            self.send_event(coll)

        
    def pickupStoreCards(self):
        player = self.player
        store = self.map.getStores()[player.getCoords()[0]]
        cards = store.getCards()
        for i in range(len(cards)):
            card = cards[i]
            if card.getType() == "MELEE WEAPON" or card.getType() == "RANGED WEAPON":
                pass
            else:
                store.removeCard(i)
                # ask if they would like to replace their current weapon with the new one. 
            # elif card.getType():
                # pass # other card types to be added.
        # add store's revealed cards to player inventory. 

    def exitMenu(self):
        event = {'type':'EXIT MENU'}
        self.send_event(event)


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
        event = {'type':'TURN CHANGE', 'turn':self.turn, 'player':self.player}
        self.send_event(event)
        self.turnEnded = False

    def revealCard(self):
        pass

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
        self.addButtons()
        self.renderer.addMap(self.map)
        self.im.addMap(self.map)

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

    def playerSearchStore(self):
        player = self.player
        coords = player.getCoords()
        card = self.dm.drawSearch()
        # print(self.map.getStores()[coords[0]].getID())
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
            print("Invalid move")

    def playerMelee(self, player):
        room = self.map.getRoom(player.getCoords())
        if room.getZombie():
            player.meleeAttack()
            self.map.removeZombie(room.getCoords())
            event = {"type":"PLAYER MELEE", "ID":player.ID, "coords":player.getCoords(), "moves":self.movesRemaining}
            self.send_event(event)
            self.mode = "move"
        else:
            print("Attack failed: No available target")
    
    def playerRanged(self, player, coords):
        room = self.map.getRoom(coords)
        if room.getZombie() and (coords in player.getMovementOptions() or coords == player.getCoords()):
            player.rangedAttack()
            self.map.removeZombie(coords)
            event = {"type":"PLAYER RANGED", "ID":player.ID, "coords":coords, "moves":self.movesRemaining}
            self.send_event(event)
            self.mode = "move"
        else:
            print("Attack failed: Ranged")


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

    def getPlayer(self, ID):
        return self.players[ID]

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