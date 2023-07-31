from . import npc
from . import events
from . import characters
from random import randint

class Coordinates:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return (isinstance(other, Coordinates) and
                self.x == other.x and self.y == other.y)

    def __hash__(self):
        return hash((self.x, self.y))

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __repr__(self):
        return f"({self.x}, {self.y})"

    def left(self):
        return Coordinates(self.x - 1, self.y)

    def right(self):
        return Coordinates(self.x + 1, self.y)

    def up(self):
        return Coordinates(self.x, self.y + 1)

    def down(self):
        return Coordinates(self.x, self.y - 1)


def testCoordinates(c1, c2):
    if c1 == c2:
        print(f"{c1} = {c2}")
    else:
        print(f"{c1} is not equal to {c2}")


testCoordinates(Coordinates(0, 0), Coordinates(5, 0))
testCoordinates(Coordinates(5, 0), Coordinates(5, 0))


class Chamber:
    def __init__(self, coordinates, number, monster: characters.Monster =None):
        self.coordinates = coordinates
        self.number = number
        self.monster = monster

    def __str__(self):
        return (f"chamber {self.number} at {self.coordinates}")

    def __repr__(self):
        return (f"chamber {self.number} at {self.coordinates}")
    
class MoveToChamberEvent(events.Event):
    """Event for moving to chambers"""

    def __init__(self, direction: str, chamber: Chamber):
        self.__direction = direction
        self.chamber = chamber

    def description(self) -> list[str]:
        """returns description of event"""
        return [f"moved {self.__direction} to {self.chamber}."]

class MeetNpcEvent(events.Event):
    """Event for meeting an NPC for the first time"""

    def __init__(self, new_npc: npc.NPC):
        self.npc = new_npc

    def description(self) -> list[str]:
        """returns description of event"""
        return [f"Met new NPC {self.npc.name()}!", f"{self.npc.name().upper()}: {self.npc.greeting()}"]

class MeetMonsterEvent(events.Event):
    """Event for when you see a monster in a room"""
    def __init__(self, new_monster: characters.Monster):
        self.monster = new_monster
    
    def description(self) -> list[str]:
        return [f"You see a {self.monster.name().lower()}.", 
                f"{self.monster.name().upper()}: {self.monster.greeting()}"]

class Dungeon:
    def __init__(self):
        self.chambers = {}
        Dungeon.lastNumber = 0
        self.createChamber(Coordinates(0, 0))

    def createChamber(self, coordinates):
        Dungeon.lastNumber += 1
        chamber = Chamber(coordinates, Dungeon.lastNumber)
        self.chambers[coordinates] = chamber
        return chamber

    def moveToChamber(self, newCoords) -> Chamber:
        if newCoords in self.chambers:
            return self.chambers[newCoords]
        else:
            return self.createChamber(newCoords)

    def moveLeft(self, coordinates) -> MoveToChamberEvent:
        return MoveToChamberEvent("west", self.moveToChamber(coordinates.left()))

    def moveRight(self, coordinates) -> MoveToChamberEvent:
        return MoveToChamberEvent("east", self.moveToChamber(coordinates.right()))

    def moveUp(self, coordinates) -> MoveToChamberEvent:
        return MoveToChamberEvent("north", self.moveToChamber(coordinates.up()))

    def moveDown(self, coordinates) -> MoveToChamberEvent:
        return MoveToChamberEvent("south", self.moveToChamber(coordinates.down()))
    
class Player(characters.Characters):
    def name(self) -> str:
        return "myself"
    

class GameState:
    def __init__(self):
        self.dungeon = Dungeon()
        self.currentCoords = Coordinates(0, 0)
        self.npcs = [npc.Warrior(15, 15), npc.Alchemist(10, 7)]
        self.activeNpcs = {}
        self.monsters = [characters.Monster(5, 5, "Goblin", "pink-monster"), characters.Monster(15, 10, "Troll", "green-monster")]
        self.history = events.History()
        self.myself = Player(10, 10)

    def moveLeft(self):
        event = self.dungeon.moveLeft(self.currentCoords)
        self.move(event)

    def moveRight(self):
        event = self.dungeon.moveRight(self.currentCoords)
        self.move(event)

    def moveUp(self):
        event = self.dungeon.moveUp(self.currentCoords)
        self.move(event)

    def moveDown(self):
        event = self.dungeon.moveDown(self.currentCoords)
        self.move(event)
    
    def move(self, event: MoveToChamberEvent):
        self.history.add_event(event)
        chamber = event.chamber
        print(f"activeNpcs 2 {self.activeNpcs}")
        self.currentCoords = chamber.coordinates
        probability_empty = 1
        probability_npc = 3
        probability_monster = 3
        total_probability = probability_empty + probability_npc + probability_monster
        x = randint(0, total_probability)
        if x <= probability_empty:
            pass
        elif x <= probability_empty + probability_monster:
            chamber.monster = self.add_monster()
        else:
            if len(self.npcs) > len(self.activeNpcs):
                self.addNpc()    
        return chamber
    
    def addNpc(self):
        for current_npc in self.npcs:
            if current_npc.name() in self.activeNpcs:
                continue
            self.activeNpcs[current_npc.name()] = current_npc
            self.history.add_event(MeetNpcEvent(current_npc))
            break
        print(f"activeNpcs {self.activeNpcs}")
        return "hi"
    
    def add_monster(self):
        prototype = self.monsters[randint(0, len(self.monsters) - 1)]
        print(prototype.name())
        print(prototype.image_name)
        monster = characters.Monster(self.modify_stat(prototype.strength), 
                                     self.modify_stat(prototype.health),
                                     prototype.name(), prototype.image_name)
        print(f"Created monster: {monster}")
        self.history.add_event(MeetMonsterEvent(monster))

        return monster
    
    def modify_stat(self, stat: int):
        return randint(0.8 * stat, 1.2 * stat)

    def createMap(self, center, margin):
        result = []
        for y in reversed(range(center.y-margin, center.y+margin+1)):
            row = []
            for x in range(center.x - margin, center.x + margin + 1):
                coordinates = Coordinates(x, y)
                if coordinates in self.dungeon.chambers:
                    row.append(self.dungeon.chambers[coordinates])
                else:
                    row.append(None)
            result.append(row)
        return result

    def createMapString(self, center, margin):
        world = self.createMap(center, margin)
        mapString = ""
        for row in world:
            for chamber in row:
                if chamber:
                    mapString += f" {chamber.number:2} "
                else:
                    mapString += "  x "
            mapString += "\n"
        return mapString
    
    

gameState = None
