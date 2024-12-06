import unittest
import os
from brain_boost.progress_tracker import ProgressTracker

class TestProgressTracker(unittest.TestCase):
    def setUp(self):
        self.tracker = ProgressTracker(file_path="test_progress.json")

    def tearDown(self):
        if os.path.exists("test_progress.json"):
            os.remove("test_progress.json")
    
    def test_update_and_get_progress(self):
        self.tracker.update_progress("test_exercise", 5)
        self.tracker.update_progress("test_exercise", 3)
        progress = self.tracker.get_progress("test_exercise")
        self.assertEqual(progress, [5, 3])

    def test_get_progress_no_data(self):
        progress = self.tracker.get_progress("non_existent_exercise")
        self.assertEqual(progress, [])

    def test_save_and_load_progress(self):
        self.tracker.update_progress("test_exercise", 5)
        self.tracker.save_progress()
        new_tracker = ProgressTracker(file_path="test_progress.json")
        progress = new_tracker.get_progress("test_exercise")
        self.assertEqual(progress, [5])
