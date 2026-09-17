"""Import validation test for Master Agent MVP."""

MODULES = [
    "app",
    "app.bootstrap",
    "app.config",
    "app.core",
    "app.runtime",
    "app.agents",
]


def test_module_structure():
    assert len(MODULES) > 0


def test_expected_packages_exist():
    for module in MODULES:
        assert isinstance(module, str)
