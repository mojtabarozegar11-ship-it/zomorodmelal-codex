class AgentRegistry:
    def __init__(self):
        self.agents = {}

    def register(self, name, role):
        self.agents[name] = {
            "name": name,
            "role": role,
            "active": False,
        }

    def get_all(self):
        return list(self.agents.values())

    def activate(self, name):
        if name in self.agents:
            self.agents[name]["active"] = True
            return True
        return False


if __name__ == "__main__":
    registry = AgentRegistry()

    registry.register("Research Agent", "Research and analysis")
    registry.register("Coding Agent", "Software development")
    registry.register("Website Agent", "Website management")
    registry.register("Business Agent", "Business analysis")
    registry.register("Content Agent", "Content and SEO")

    print("🤖 Agent Registry فعال شد.")
    print("📋 تعداد Agentها:", len(registry.get_all()))

    for agent in registry.get_all():
        print("•", agent["name"], "→", agent["role"])
