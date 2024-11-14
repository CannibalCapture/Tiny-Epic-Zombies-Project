from room import Room
from gamemanager import GameManager

class Store:
    def __init__(self, rooms, storeID):
        self.rooms = rooms
        self.storeID = storeID

room1 = Room(0, False, False)
room2 = Room(1, True, False)
room3 = Room(2, False, True)
store1 = Store([room1, room2, room3], 0)
manager = GameManager({})
manager.addPlayer("p1", 0, "Blue", "Musician", (0,0))