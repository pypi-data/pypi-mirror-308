import matplotlib.pyplot as plt
from .progress_tracker import ProgressTracker

def analyze_overall_performance():
    """
    Analiza el rendimiento promedio en cada ejercicio y muestra un gráfico de barras.
    """
    tracker = ProgressTracker()
    exercises = ["memory_exercise", "mental_math", "general_knowledge", "logic_exercise"]
    
    average_scores = {}
    for exercise in exercises:
        scores = tracker.get_progress(exercise)
        if scores:
            average_scores[exercise] = sum(scores) / len(scores)
        else:
            average_scores[exercise] = 0
    
    exercises = list(average_scores.keys())
    averages = list(average_scores.values())
    
    plt.bar(exercises, averages, color='skyblue')
    plt.title("Puntuación promedio en todos los ejercicios")
    plt.xlabel("Ejercicio")
    plt.ylabel("Puntuación Promedio")
    plt.ylim(0, 5)
    plt.show()


# import matplotlib.pyplot as plt
# from .progress_tracker import ProgressTracker

# def analyze_overall_performance():
#     tracker = ProgressTracker()
#     exercises = ["memory_exercise", "mental_math", "general_knowledge", "logic_exercise"]
    
#     # Calcula la puntuación promedio para cada ejercicio
#     average_scores = {}
#     for exercise in exercises:
#         scores = tracker.get_progress(exercise)
#         if scores:
#             average_scores[exercise] = sum(scores) / len(scores)
#         else:
#             average_scores[exercise] = 0  # Asigna 0 si no hay datos
    
#     # Crear el gráfico de puntuación promedio para cada ejercicio
#     exercises = list(average_scores.keys())
#     averages = list(average_scores.values())
    
#     plt.bar(exercises, averages, color='skyblue')
#     plt.title("Puntuación promedio en todos los ejercicios")
#     plt.xlabel("Ejercicio")
#     plt.ylabel("Puntuación Promedio")
#     plt.ylim(0, 5)  # Ajusta el límite en función de la escala de puntuación
#     plt.show()
