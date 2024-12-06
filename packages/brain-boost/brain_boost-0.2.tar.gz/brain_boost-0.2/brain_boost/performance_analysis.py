import matplotlib.pyplot as plt
from .progress_tracker import ProgressTracker

def analyze_performance(exercise):
    tracker = ProgressTracker()
    scores = tracker.get_progress(exercise)

    if not scores:
        print("No hay datos para este ejercicio.")
        return

    plt.plot(scores, marker="o", linestyle="-")
    plt.title(f"Progreso en {exercise}")
    plt.xlabel("Intento")
    plt.ylabel("Puntuación")
    plt.show()
