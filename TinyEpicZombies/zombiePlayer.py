from .listener import Listener

class ZombiePlayer(Listener):
    def __init__(self):
        pass
        # self.map = map

    def on_event(self, event):
        if event['type'] == 'BLUE NOISE':
            print("BLUE NOISE")
    
    def placeZombie(self, number):
        for i in range(number):
            pass