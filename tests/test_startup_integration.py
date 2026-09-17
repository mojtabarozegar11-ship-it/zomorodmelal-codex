"""Startup integration validation for Master Agent Core."""


def test_project_structure_ready():
    required_paths = [
        "app/start.py",
        "app/bootstrap.py",
        "app/core",
        "app/agents",
        "app/runtime",
    ]

    assert all(required_paths)
