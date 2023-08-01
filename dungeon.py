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
    def __init__(self, coordinates, number, monster: characters.Monster = None):
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


class MonsterBlockEvent(events.Event):
    """"Event for when you try to move without defeating monster"""

    def description(self):
        return ["The monster blocks your path!", "It doesnt look you can leave without defeating the monster."]
    
class NoTargetAttackEvent(events.Event):
    """Event for when you attack with no target"""

    def description(self):
        return ["You attacked the air! You did 0 dmg D:"]
    
class AttackEvent(events.Event):
    """Event for when you attack a monster"""
    def __init__(self, attacker: characters.Character, target: characters.Character, dmg_taken: int):
        self.attacker = attacker
        self.target = target
        self.dmg_taken = dmg_taken
        
    def description (self):
        return [f"{self.attacker.name()} swung and hit {self.target.name()} for {self.dmg_taken} damage!"]

class MonsterKilledEvent(events.Event):
    "Event for when monster is killed (0 HP)"
    def __init__(self, monster: characters.Monster):
        self.monster = monster

    def description(self):
        return [f"{self.monster.name()} was defeated!"]


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


class Player(characters.Character):
    def name(self) -> str:
        return "Hero"


class GameState:
    def __init__(self):
        self.dungeon = Dungeon()
        self.currentCoords = Coordinates(0, 0)
        self.npcs = [npc.Warrior(4, 15), npc.Alchemist(2, 7)]
        self.activeNpcs = {}
        self.monsters = [characters.Monster(
            5, 5, "Goblin", "pink-monster"), characters.Monster(3, 20, "Troll", "green-monster")]
        self.history = events.History()
        self.myself = Player(3, 10)

    def moveLeft(self):
        if self.move_allowed():
            event = self.dungeon.moveLeft(self.currentCoords)
            self.move(event)

    def moveRight(self):
        if self.move_allowed():
            event = self.dungeon.moveRight(self.currentCoords)
            self.move(event)

    def moveUp(self):
        if self.move_allowed():
            event = self.dungeon.moveUp(self.currentCoords)
            self.move(event)

    def moveDown(self):
        if self.move_allowed():
            event = self.dungeon.moveDown(self.currentCoords)
            self.move(event)

    def move_allowed(self) -> bool:
        """Checks if we are allowed to move rooms"""
        chamber = self.dungeon.chambers[self.currentCoords]
        if chamber.monster:
            self.history.add_event(MonsterBlockEvent())
            return False
        else:
            return True
    
    def move(self, event: MoveToChamberEvent): 
        chamber = event.chamber
        self.history.add_event(event)
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

    def attack(self):
        """attacks monster if present"""
        chamber = self.dungeon.chambers[self.currentCoords]
        if not chamber.monster:
            self.history.add_event(NoTargetAttackEvent())
            return
        monster = chamber.monster
        monster.current_health -= self.myself.strength
        if monster.current_health <= 0:
            self.history.add_event(MonsterKilledEvent(monster))
            chamber.monster = None
            return
        self.history.add_event(AttackEvent(self.myself, monster, self.myself.strength))

        
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
    
    def modify_stat(self,stat: int):
        return randint(int(0.8* stat), int(1.2 * stat))

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
