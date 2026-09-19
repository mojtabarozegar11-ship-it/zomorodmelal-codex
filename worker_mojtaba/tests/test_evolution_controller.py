from worker_mojtaba.evolution.engine import EvolutionEngine
from worker_mojtaba.evolution.controller import UpgradeController


def test_upgrade_controller_approves_candidate_without_auto_deploy():
    controller = UpgradeController(EvolutionEngine())
    result = controller.run(
        "1.0.0",
        ["improve-planner"],
        lambda: True,
    )

    assert result.candidate.status == "approved"
    assert result.action == "awaiting_owner_approval"
    assert result.state["version"] == "1.0.0-candidate"


def test_upgrade_controller_rolls_back_rejected_candidate():
    controller = UpgradeController(EvolutionEngine())
    result = controller.run(
        "1.0.0",
        ["unsafe-change"],
        lambda: False,
    )

    assert result.candidate.status == "rejected"
    assert result.action == "rollback_available"
    assert result.state["version"] == "1.0.0"
