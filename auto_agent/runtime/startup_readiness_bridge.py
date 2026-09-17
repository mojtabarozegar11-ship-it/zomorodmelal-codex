"""Bridge production readiness checks into startup flow."""


def check_startup_readiness(checks):
    return all(checks)
