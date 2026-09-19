from worker_mojtaba.security.policy import Policy


def test_allow_list_denies_undeclared_capabilities():
    policy = Policy({"calendar_event"})
    assert policy.check_capability("calendar_event")
    assert not policy.check_capability("wallet")


def test_disabled_policy_denies_everything():
    policy = Policy({"calendar_event"})
    policy.disable()
    assert not policy.check_capability("calendar_event")
