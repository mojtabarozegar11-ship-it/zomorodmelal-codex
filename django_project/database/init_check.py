"""Database initialization check for offline phase."""


def check_database_ready():
    return {
        "database": "pending migration",
        "ai_api": False,
        "status": "phase1"
    }
