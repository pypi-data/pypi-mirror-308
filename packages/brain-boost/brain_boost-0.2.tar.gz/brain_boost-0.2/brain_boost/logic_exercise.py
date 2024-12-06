import random

def logic_exercise(difficulty="fácil"):
    patterns = {
        "fácil": [2, 4, 6, 8, 10],
        "intermedio": [3, 6, 9, 12, 15],
        "difícil": [1, 4, 9, 16, 25]
    }
    sequence = patterns[difficulty]
    print("Encuentra el patrón y da el siguiente número de la secuencia:")
    print(sequence)
    
    correct_answer = sequence[-1] + (sequence[-1] - sequence[-2])
    user_answer = int(input("¿Cuál es el siguiente número? "))
    
    if user_answer == correct_answer:
        return "¡Correcto! Buen razonamiento lógico."
    else:
        return f"Incorrecto. La respuesta correcta era: {correct_answer}"
