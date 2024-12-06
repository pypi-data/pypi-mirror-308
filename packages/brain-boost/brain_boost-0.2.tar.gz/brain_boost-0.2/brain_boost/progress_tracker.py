import json
import os

class ProgressTracker:
    def __init__(self, file_path="progress.json"):
        self.file_path = file_path
        self.load_progress()

    def load_progress(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as file:
                self.data = json.load(file)
        else:
            self.data = {}

    def save_progress(self):
        with open(self.file_path, "w") as file:
            json.dump(self.data, file)

    def update_progress(self, exercise, score):
        if exercise not in self.data:
            self.data[exercise] = []
        self.data[exercise].append(score)
        self.save_progress()

    def get_progress(self, exercise):
        return self.data.get(exercise, [])
