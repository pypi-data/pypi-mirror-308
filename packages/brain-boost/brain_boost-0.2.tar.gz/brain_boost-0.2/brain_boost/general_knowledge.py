import random

questions = {
    "fácil": {
        "¿Cuál es la capital de Francia?": "París",
        "¿Cuántos planetas tiene el sistema solar?": "8"
    },
    "intermedio": {
        "¿Quién escribió 'Cien años de soledad'?": "Gabriel García Márquez",
        "¿Qué es el teorema de Pitágoras?": "a^2 + b^2 = c^2"
    },
    "difícil": {
        "¿En qué año comenzó la Segunda Guerra Mundial?": "1939",
        "¿Cuál es la fórmula química del agua?": "H2O"
    }
}

def general_knowledge(difficulty="fácil"):
    question, answer = random.choice(list(questions[difficulty].items()))
    user_answer = input(question + " ")
    if user_answer.lower() == answer.lower():
        return "¡Correcto! Sabes mucho."
    else:
        return f"Incorrecto. La respuesta correcta era: {answer}"
