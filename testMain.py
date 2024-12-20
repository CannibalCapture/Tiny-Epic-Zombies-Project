from TinyEpicZombies.helperfunctions.roomrects import genRoomRects
from TinyEpicZombies import inputmanager
import numpy as np
# json.dump(manager.serialize(), open("game.json", "w"), indent=2)

# Cards which affect movement will be dealt with in the code for generating a player turn.
# List of status effects [("what it is", "how many turns it will last")]

print(tuple(np.multiply((5,5), (6,5))))