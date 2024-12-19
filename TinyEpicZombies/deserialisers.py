import os
import json

def deserializeCollider(coords):
    store, room = coords[0], coords[1]
    with open(os.path.join("TinyEpicZombies","jsonfiles", "roompoints.json")) as file:
        data = json.loads("".join(file.readlines()))
        return(data["stores"][f"store{store}"]["rooms"][f"room{room}"]["collider"])