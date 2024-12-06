# brain_boost/mental_math.py

import random

def mental_math():
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    operation = random.choice(['+', '-', '*'])
    question = f"{num1} {operation} {num2}"
    correct_answer = eval(question)
    user_answer = int(input(f"¿Cuál es el resultado de {question}? "))
    if user_answer == correct_answer:
        return "¡Correcto! Buen cálculo mental."
    else:
        return f"Incorrecto. La respuesta correcta era: {correct_answer}"
