class NPC:
    def __init__(self, name, strength, health):
        self.name = name
        self.strength = strength
        self.health = health

    def __str__(self):
        return f"{self.name}: Strength: {self.strength}, Health: {self.health}"
