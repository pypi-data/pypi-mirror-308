import unittest
from brain_boost import analyze_overall_performance

class TestPerformanceAnalysis(unittest.TestCase):
    def test_analyze_overall_performance(self):
        try:
            analyze_overall_performance()
            success = True
        except Exception:
            success = False
        self.assertTrue(success)
