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
    