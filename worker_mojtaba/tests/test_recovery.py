from worker_mojtaba.security.recovery import RecoveryManager


def test_checkpoint_and_restore_round_trip():
    manager = RecoveryManager()
    manager.checkpoint("before-change", {"version": "1", "enabled": True})
    manager.checkpoint("after-change", {"version": "2", "enabled": False})

    assert manager.latest().checkpoint_id == "after-change"
    assert manager.restore("before-change") == {"version": "1", "enabled": True}
    assert [c.checkpoint_id for c in manager.list_checkpoints()] == [
        "before-change",
        "after-change",
    ]
