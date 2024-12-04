from TinyEpicZombies.gamemanager import GameManager
from TinyEpicZombies.zombiemap import ZombieMap

manager = GameManager()
player1 = manager.players[0]
# manager.playerSearchStore(player1)
manager.zm.shortestPath((0,0))
# Plan is to make the decks, then implement noise.
# Cards which affect movement will be dealt with in the code for generating a player turn.