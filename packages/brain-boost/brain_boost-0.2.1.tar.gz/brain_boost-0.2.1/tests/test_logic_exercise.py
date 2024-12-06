import unittest
from brain_boost import logic_exercise
from brain_boost.progress_tracker import ProgressTracker

class TestLogicExercise(unittest.TestCase):
    def setUp(self):
        self.tracker = ProgressTracker()
    
    def test_logic_exercise_easy(self):
        result = logic_exercise(difficulty="fácil", tracker=self.tracker)
        self.assertIn(result, ["¡Correcto! Buen razonamiento lógico.", "Incorrecto. La respuesta correcta era:"])
    
    def test_invalid_difficulty(self):
        with self.assertRaises(ValueError):
            logic_exercise(difficulty="invalid", tracker=self.tracker)
