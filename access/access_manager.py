"""Compatibility facade for the canonical autonomous_core access manager."""

from autonomous_core.access_manager import AccessManager


__all__ = ["AccessManager"]


if __name__ == "__main__":
    manager = AccessManager()
    print("Access Manager compatibility facade فعال است.")
    print(manager.status())
