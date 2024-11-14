from TinyEpicZombies.store import Store
from TinyEpicZombies.gamemanager import GameManager
from TinyEpicZombies.store import Store
from TinyEpicZombies.room import Room

room1 = Room(0, False, False)
room2 = Room(1, True, False)
room3 = Room(2, False, True)
store1 = Store([room1, room2, room3], 0)
manager = GameManager({})
manager.addPlayer("p1", 0, "Blue", "Musician", (0,0))