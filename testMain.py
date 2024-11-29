from TinyEpicZombies.gamemanager import GameManager

manager = GameManager()
player1 = manager.players[0]
manager.playerSearchStore(player1)

# Plan is to make the decks, then implement noise.
# Cards which affect movement will be dealt with in the code for generating a player turn.P