class EngineValidator:
    def validate(self, components):
        result = {}
        for name, available in components.items():
            result[name] = bool(available)
        return {
            "status": "ready" if all(result.values()) else "incomplete",
            "components": result
        }
