def test_approval_flow():
    class Gateway:
        def request(self, action):
            return action

    from autonomous_core.approval_flow import ApprovalFlow
    assert ApprovalFlow(Gateway()).check('run') == 'run'
