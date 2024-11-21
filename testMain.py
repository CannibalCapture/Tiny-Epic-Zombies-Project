from TinyEpicZombies.store import Store
from TinyEpicZombies.gamemanager import GameManager
from TinyEpicZombies.room import Room
from TinyEpicZombies.map import Map

room1 = Room(0, (0,0), False, False)
room2 = Room(1, (0,1), True, False)
room3 = Room(2, (0,2), True, True)
store1 = Store([room1, room2, room3], 0)

gameMap = Map([store1])
manager = GameManager(gameMap)
manager.createPlayer("Toby", 0, "Blue", "Musician", (0,0))
player1 = manager.players[0]
manager.add_listener(player1)

al = manager.map.adjList
al.addEdge((0,0), (0,1))
al.addEdge((0,0), (0,2))
al.addEdge((0,1), (0,2))
al.addEdge((0,2), (0,1))

manager.movePlayer((0,1), player1)
manager.playerRanged(player1, (0,2))

player1.takeDamage(10)

# Plan is to make the decks, then implement noise.