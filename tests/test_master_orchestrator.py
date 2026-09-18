import unittest
from master_agent import MasterOrchestrator

class MasterOrchestratorTests(unittest.TestCase):
    def test_denies_without_approval(self):
        self.assertEqual(MasterOrchestrator().execute('audit site')['status'], 'approval_required')

    def test_runs_after_approval(self):
        result = MasterOrchestrator().execute('audit site', approved=True, action=lambda plan: {'ok': True}, validate=lambda value: value['ok'])
        self.assertEqual(result['status'], 'completed')

    def test_validation_failure(self):
        result = MasterOrchestrator().execute('audit site', approved=True, action=lambda plan: {'ok': False}, validate=lambda value: value['ok'])
        self.assertEqual(result['status'], 'validation_failed')

if __name__ == '__main__':
    unittest.main()
