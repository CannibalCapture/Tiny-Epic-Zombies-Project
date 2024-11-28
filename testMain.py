from TinyEpicZombies.store import Store
from TinyEpicZombies.gamemanager import GameManager
from TinyEpicZombies.room import Room
from TinyEpicZombies.map import Map
from TinyEpicZombies.deckmanager import DeckManager

gameMap = Map()
manager = GameManager(gameMap)
# manager.createPlayer("Toby", 0, "Blue", "Musician", (0,0))
player1 = manager.players[0]
manager.add_listener(player1)

# dm.takeSupply()

manager.movePlayer((4,3), player1)
# print(manager.map.al.returnAdjList())
# # manager.playerRanged(player1, (0,2))

# Plan is to make the decks, then implement noise.
# Cards which affect movement will be dealt with in the code for generating a player turn.