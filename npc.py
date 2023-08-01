"""Implementation of all NPCs"""
from . import characters

class NPC (characters.Character):
    """Base class for all NPCs: defines name, strength, and health"""
    
    def greeting(self) -> str:
        """Returns string greeting when met for the first time"""
        return "Nice to meet you!"
    
    def name(self) -> str:
        """Returns name of NPC"""
        return "NPC"
    
class Alchemist(NPC):
    """Alchemist, a specific type of NPC which heals other characters"""
    def can_heal(self) -> bool:
        return True
    
    def greeting(self) -> str:
        return "Need some support? I'm here to help!"
    
    def name(self) -> str:
        return "alchemist"

class Warrior(NPC):
    """Warrior, a specific type of NPC who helps attack and is strong at attacking"""
    def greeting(self) -> str:
        return "I bet you need help, weakling. I can kill those monsters for you."
    
    def name(self) -> str:
        return "warrior"