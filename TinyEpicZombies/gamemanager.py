from .player import Player

class GameManager:
    def __init__(self, map, players={}):
        self.players = players # players is a dictionary with key=playerID, value=playerObject
        self.map = map
        self.listeners = []

    def add_listener(self, listener):
        self.listeners.append(listener)
    
    def send_event(self, event):
        for listener in self.listeners:
            listener.on_event(event)

    def createPlayer(self, name, playerID, colour, character, coords):
        player = Player(name, playerID, colour, character, coords)
        self.players[playerID] = player
        player.room = coords # coords (coordinates) will be in the form (storeID, room)
        # Adding a player as a listener to listen for the createPlayer method doesnt work (for somewhat obvious reasons).

    def movePlayer(self, newCoords, player): # newCoords is a tuple containing the storeID and the room in that store.
        if self.map.adjList.validatePlayerMove(player, newCoords):
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
        if self.map.adjList.validatePlayerMove(player, coords) and self.map.stores[s].rooms[r].zombie:
            player.rangedAttack()
            self.map.stores[s].rooms[r].setZombie(False)
            event = {"type":"PLAYER RANGED", "playerID":player.playerID, "coords":coords}
            self.send_event(event)
        else:
            print("Attack failed: Ranged")

