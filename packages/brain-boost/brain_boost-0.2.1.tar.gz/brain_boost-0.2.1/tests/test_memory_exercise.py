import unittest
from brain_boost import memory_exercise
from brain_boost.progress_tracker import ProgressTracker

class TestMemoryExercise(unittest.TestCase):
    def setUp(self):
        self.tracker = ProgressTracker()
    
    def test_memory_exercise_easy(self):
        result = memory_exercise(difficulty="fácil", tracker=self.tracker)
        self.assertIn(result, ["¡Correcto! Buena memoria.", "Incorrecto. La secuencia correcta era:"])
    
    def test_invalid_difficulty(self):
        with self.assertRaises(KeyError):
            memory_exercise(difficulty="invalid", tracker=self.tracker)
