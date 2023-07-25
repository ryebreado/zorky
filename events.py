"""This is the module for history and events of the game"""

class Event:
    def description(self) -> list[str]:
        """Description of the Event"""
        return ["Undefined Event"]
    
class History:
    """History of Past Events"""
    def __init__(self):
        self.__events = []
        
    def add_event(self, event: Event):
        """Adds event to the end of event list"""
        self.__events.append(event)

    def most_recent_events(self, count: int) -> list[Event]:
        """Returns most recent events"""
        return self.__events[-count:]