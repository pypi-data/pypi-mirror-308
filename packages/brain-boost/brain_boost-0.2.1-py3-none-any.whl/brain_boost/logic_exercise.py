import random

def logic_exercise(difficulty="fácil", tracker=None):
    """
    Presenta una secuencia lógica y pide al usuario que identifique el siguiente número.

    Parameters:
    - difficulty (str): Nivel de dificultad ("fácil", "intermedio", "difícil").
    - tracker (ProgressTracker, optional): Objeto para guardar el progreso.

    Returns:
    - result (str): Mensaje de resultado (correcto/incorrecto).
    """
    patterns = {
        "fácil": [2, 4, 6, 8, 10],
        "intermedio": [3, 6, 9, 12, 15],
        "difícil": [1, 4, 9, 16, 25]
    }
    
    try:
        sequence = patterns[difficulty]
    except KeyError:
        raise ValueError(f"Dificultad '{difficulty}' no válida. Usa 'fácil', 'intermedio' o 'difícil'.")
    
    print("Encuentra el patrón y da el siguiente número de la secuencia:")
    print(sequence)
    
    correct_answer = sequence[-1] + (sequence[-1] - sequence[-2])
    user_answer = int(input("¿Cuál es el siguiente número? "))
    
    if user_answer == correct_answer:
        result = "¡Correcto! Buen razonamiento lógico."
        score = 5
    else:
        result = f"Incorrecto. La respuesta correcta era: {correct_answer}"
        score = 2
    
    print(result)
    
    if tracker is not None:
        tracker.update_progress("logic_exercise", score)
    
    return result


# import random

# def logic_exercise(difficulty="fácil", tracker=None):
#     patterns = {
#         "fácil": [2, 4, 6, 8, 10],
#         "intermedio": [3, 6, 9, 12, 15],
#         "difícil": [1, 4, 9, 16, 25]
#     }
#     sequence = patterns[difficulty]
#     print("Encuentra el patrón y da el siguiente número de la secuencia:")
#     print(sequence)
    
#     correct_answer = sequence[-1] + (sequence[-1] - sequence[-2])
#     user_answer = int(input("¿Cuál es el siguiente número? "))
    
#     if user_answer == correct_answer:
#         result = "¡Correcto! Buen razonamiento lógico."
#         score = 5
#     else:
#         result = f"Incorrecto. La respuesta correcta era: {correct_answer}"
#         score = 2
    
#     print(result)
    
#     # Actualiza el progreso si el tracker está presente
#     if tracker is not None:
#         tracker.update_progress("logic_exercise", score)
    
#     return result
