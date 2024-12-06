import random

def mental_math(difficulty="fácil"):
    ranges = {"fácil": (1, 10), "intermedio": (10, 50), "difícil": (50, 100)}
    num1 = random.randint(*ranges[difficulty])
    num2 = random.randint(*ranges[difficulty])
    operation = random.choice(['+', '-', '*'])
    question = f"{num1} {operation} {num2}"
    correct_answer = eval(question)
    
    user_answer = int(input(f"¿Cuál es el resultado de {question}? "))
    if user_answer == correct_answer:
        return "¡Correcto! Buen cálculo mental."
    else:
        return f"Incorrecto. La respuesta correcta era: {correct_answer}"
