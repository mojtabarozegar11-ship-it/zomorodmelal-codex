"""Memory abstraction."""
class MemoryStore:
    def __init__(self) -> None:
        self.short_term: list[dict] = []
        self.long_term: list[dict] = []
    def remember_short(self,item:dict)->None: self.short_term.append(item)
    def remember_long(self,item:dict)->None: self.long_term.append(item)
    def recent(self,limit:int=20)->list[dict]: return self.short_term[-limit:]
