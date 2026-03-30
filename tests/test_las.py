import unittest
from datetime import datetime
from lasm import LASMEvaluator

class TestLASEvaluator(unittest.TestCase):
    def test_las_computation(self):
        evaluator = LASMEvaluator()
        system = evaluator.load_system("tests/fixtures/sample_systems.json")
        res = evaluator.compute_las(system, datetime.now(), "B_mid")
        self.assertIsNotNone(res)
        self.assertGreaterEqual(res.LAS_norm, 0)
        self.assertLessEqual(res.LAS_norm, 100)

if __name__ == '__main__':
    unittest.main()
