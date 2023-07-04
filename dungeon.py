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
    def __init__(self, coordinates, number):
        self.coordinates = coordinates
        self.number = number

    def __str__(self):
        return (f"chamber {self.number} at {self.coordinates}")

    def __repr__(self):
        return (f"chamber {self.number} at {self.coordinates}")


room = Chamber(Coordinates(1, 1), 5)
print(room)


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

    def moveToChamber(self, newCoords):
        if newCoords in self.chambers:
            return self.chambers[newCoords]
        else:
            return self.createChamber(newCoords)

    def moveLeft(self, coordinates):
        return self.moveToChamber(coordinates.left())

    def moveRight(self, coordinates):
        return self.moveToChamber(coordinates.right())

    def moveUp(self, coordinates):
        return self.moveToChamber(coordinates.up())

    def moveDown(self, coordinates):
        return self.moveToChamber(coordinates.down())


class GameState:
    def __init__(self):
        self.dungeon = Dungeon()
        self.currentCoords = Coordinates(0, 0)

    def moveLeft(self):
        chamber = self.dungeon.moveLeft(self.currentCoords)
        self.currentCoords = chamber.coordinates
        return chamber

    def moveRight(self):
        chamber = self.dungeon.moveRight(self.currentCoords)
        self.currentCoords = chamber.coordinates
        return chamber

    def moveUp(self):
        chamber = self.dungeon.moveUp(self.currentCoords)
        self.currentCoords = chamber.coordinates
        return chamber

    def moveDown(self):
        chamber = self.dungeon.moveDown(self.currentCoords)
        self.currentCoords = chamber.coordinates
        return chamber

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
        map = self.createMap(center, margin)
        mapString = ""
        for row in map:
            for chamber in row:
                if chamber:
                    mapString += f" {chamber.number:2} "
                else:
                    mapString += f"  x "
            mapString += "\n"
        return mapString


gameState = GameState()
gameState.moveLeft()
gameState.moveUp()
print(gameState.currentCoords)
print(gameState.dungeon.chambers)
print(gameState.createMapString(Coordinates(0, 0), 2))
