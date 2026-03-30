import unittest
from datetime import datetime
from lasm import LASMEvaluator

class TestMetrics(unittest.TestCase):
    def setUp(self):
        self.evaluator = LASMEvaluator()
        self.system = self.evaluator.load_system("tests/fixtures/sample_systems.json")

    def test_eas_computation(self):
        res = self.evaluator.compute_eas(self.system, datetime.now(), "B_mid", "criminal", 5000)
        self.assertTrue(0 <= res.deterrence_ratio <= 1.0)
        
    def test_adt_computation(self):
        res = self.evaluator.compute_adt("LlamaGuard", "criminal", self.system, (0.5, 1.5))
        self.assertIsNotNone(res.ADT)

if __name__ == '__main__':
    unittest.main()
