"""Implementation of all Characters"""
class Characters:
    """Base class for all NPCs: defines name, strength, and health"""
    def __init__(self, strength: int, health: int):
        self.strength = strength
        self.health = health

    def __str__(self):
        return f"{self.name()}: Strength: {self.strength}, Health: {self.health}"    

    def __repr__(self):
        return f"{self.name()}: Strength: {self.strength}, Health: {self.health}"
    
    def can_heal(self) -> bool:
        """Determines whether a specific character can heal other characters"""
        return False
    
    def can_attack(self) -> bool:
        """Determines whether a specific character can attack other characters"""
        return True
    
    def name(self) -> str:
        """Returns name of character"""
        return "character"

class Monster(Characters):
    """Class for monsters"""
    def __init__(self, strength: int, health: int, monster_name: str, image_name: str):
        super().__init__(strength, health)
        self.monster_name = monster_name
        self.image_name = image_name
    
    def greeting(self) -> str:
        return "I am going to destroy you!!"
    
    def name(self) -> str:
        return self.monster_name