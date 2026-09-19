from worker_mojtaba.evolution.engine import EvolutionEngine


def test_evolution_candidate_gets_checkpoint_and_rolls_back():
    engine = EvolutionEngine()
    candidate = engine.propose("0.9.0", ["improve-security"])

    assert candidate.checkpoint_id == "0.9.0-pre-upgrade"
    assert candidate.rollback_state["version"] == "0.9.0"

    engine.evaluate(candidate, tests_passed=False)
    assert candidate.status == "rejected"
    assert engine.rollback(candidate)["version"] == "0.9.0"
