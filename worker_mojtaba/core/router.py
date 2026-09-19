"""Capability router."""
class Router:
    def route(self, intent:str, available_tools:list[str])->str:
        return intent if intent in available_tools else "text_model"
