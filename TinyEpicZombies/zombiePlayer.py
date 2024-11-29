from .listener import Listener

class ZombiePlayer(Listener):
    def __init__(self):
        pass

    def on_event(self, event):
        if event['type'] == 'BLUE NOISE':
            print("BLUE NOISE BABY")