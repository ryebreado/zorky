outside = {"name": "outside", "paths": {"N": "entryroom"}}
outside["description"] = "You are outside. There is a house to the north. The door is slightly open."
entryroom = {"name": "entryroom", "paths": {
    "S": "outside", "NE": "tvroom", "W": "kitchen", "N": "stairs"}}
entryroom["description"] = "You have entered the house. To the east is the living room, west to kitchen, north to stairway"
kitchen = {"name": "kitchen", "paths": {
    "N": "bathroom", "NE": "hallway", "E": "entryroom"}}
kitchen["description"] = "You are in a kitchen. There is a refrigerator with a strange smell coming out of it. There is a counter and table."
hallway = {"name": "hallway", "paths": {"E": "tvroom", "SW": "kitchen"}}
hallway["description"] = "You are in a hallway. It is dark...."
tvroom = {"name": "tvroom", "paths": {"W": "hallway", "SW": "entryroom"}}
tvroom["description"] = "There is a big TV in the room. The screen has a large crack in it."

house = {}


def addRoom(room):
    house[room["name"]] = room


addRoom(outside)
addRoom(entryroom)
addRoom(kitchen)
addRoom(hallway)
addRoom(tvroom)


class Room:
    def __init__(self, name, paths, description):
        self.name = name
        self.paths = paths
        self.description = description

    def __str__(self):
        return f"room:{self.name}"

    def __repr__(self):
        return f"room:{self.name}"

    def print(self):
        print(f"You are currently in {self.name}")
        print(f"You are able to go {list(self.paths.keys())}")
        print(self.description)


home = {}
for name in house:
    #  print(name)

    room = Room(name, house[name]["paths"], house[name]["description"])
# room.print()
    home[name] = room
