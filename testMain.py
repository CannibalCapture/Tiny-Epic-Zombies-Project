from TinyEpicZombies.helperfunctions.roomrects import genRoomRects
from TinyEpicZombies.gamemanager import GameManager
# json.dump(manager.serialize(), open("game.json", "w"), indent=2)

# Cards which affect movement will be dealt with in the code for generating a player turn.
# List of status effects [("what it is", "how many turns it will last")]
gm = GameManager()

print(gm.getMap().getAdjList().getAdjList())

# [(4, 3), (6, 2), (7, 1), (7, 2)]