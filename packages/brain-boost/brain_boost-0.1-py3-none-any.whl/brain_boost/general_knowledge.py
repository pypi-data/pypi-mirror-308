# brain_boost/general_knowledge.py

import random

questions = {
    "¿Cuál es la capital de Francia?": "París",
    "¿Cuántos planetas tiene el sistema solar?": "8",
    "¿Quién escribió 'Cien años de soledad'?": "Gabriel García Márquez"
}

def general_knowledge():
    question, answer = random.choice(list(questions.items()))
    user_answer = input(question + " ")
    if user_answer.lower() == answer.lower():
        return "¡Correcto! Sabes mucho."
    else:
        return f"Incorrecto. La respuesta correcta era: {answer}"
