import unittest
from brain_boost import general_knowledge
from brain_boost.progress_tracker import ProgressTracker

class TestGeneralKnowledge(unittest.TestCase):
    def setUp(self):
        self.tracker = ProgressTracker()
    
    def test_general_knowledge_easy(self):
        result = general_knowledge(difficulty="fácil", tracker=self.tracker)
        self.assertIn(result, ["¡Correcto! Sabes mucho.", "Incorrecto. La respuesta correcta era:"])
    
    def test_invalid_difficulty(self):
        with self.assertRaises(ValueError):
            general_knowledge(difficulty="invalid", tracker=self.tracker)
