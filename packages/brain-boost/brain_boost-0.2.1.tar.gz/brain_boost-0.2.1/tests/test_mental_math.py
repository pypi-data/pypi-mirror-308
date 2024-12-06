import unittest
from brain_boost import mental_math
from brain_boost.progress_tracker import ProgressTracker

class TestMentalMath(unittest.TestCase):
    def setUp(self):
        self.tracker = ProgressTracker()
    
    def test_mental_math_easy(self):
        result = mental_math(difficulty="fácil", tracker=self.tracker)
        self.assertIn(result, ["¡Correcto! Buen cálculo mental.", "Incorrecto. La respuesta correcta era:"])
    
    def test_invalid_difficulty(self):
        with self.assertRaises(ValueError):
            mental_math(difficulty="invalid", tracker=self.tracker)
