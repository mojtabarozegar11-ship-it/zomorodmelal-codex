"""Phase 1 database preparation helper.

Runs only local Django database preparation.
No AI provider dependency.
"""


def migration_plan():
    return {
        "mode": "offline",
        "steps": [
            "check models",
            "create migrations",
            "apply migrations",
            "validate database",
        ],
    }
