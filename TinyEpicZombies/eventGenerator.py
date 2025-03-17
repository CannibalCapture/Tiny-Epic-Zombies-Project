class EventGenerator:
    def __init__(self):
        self.listeners = []

    def add_listener(self, listener):
        self.listeners.append(listener)
    
    def send_event(self, event):
        # print(event)
        for listener in self.listeners:
            listener.on_event(event)
            
