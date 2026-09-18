class MasterCycleValidator:
    def validate(self, cycle):
        return {
            "valid": cycle is not None,
            "cycle": cycle
        }
