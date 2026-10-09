"""CAPA DE LÓGICA DE NEGOCIO.

Aquí no hay nada de HTTP ni de HTML: solo las reglas de la lotería.
"""
import random

NUM_COUNT = 6   # cuántos números tiene un boleto
MAX_NUM = 49    # los números van de 1 a MAX_NUM

PRIZES = {
    6: "Premio mayor",
    5: "Segundo premio",
    4: "Tercer premio",
    3: "Reintegro",
}


def validate_ticket(numbers):
    """Devuelve (True, "") si el boleto es válido, o (False, motivo)."""
    if not isinstance(numbers, list) or len(numbers) != NUM_COUNT:
        return False, f"Debes elegir exactamente {NUM_COUNT} números."
    if not all(isinstance(n, int) and not isinstance(n, bool) for n in numbers):
        return False, "Todos los valores deben ser números enteros."
    if len(set(numbers)) != NUM_COUNT:
        return False, "No puedes repetir números."
    if any(n < 1 or n > MAX_NUM for n in numbers):
        return False, f"Los números deben estar entre 1 y {MAX_NUM}."
    return True, ""


def random_ticket():
    """Boleto aleatorio ("quick pick")."""
    return sorted(random.sample(range(1, MAX_NUM + 1), NUM_COUNT))


def draw():
    """Sortea la combinación ganadora."""
    return sorted(random.sample(range(1, MAX_NUM + 1), NUM_COUNT))


def evaluate(ticket, winning):
    """Compara el boleto con la combinación ganadora."""
    matches = sorted(set(ticket) & set(winning))
    prize = PRIZES.get(len(matches))
    return {
        "matches": matches,
        "match_count": len(matches),
        "prize": prize,
        "won": prize is not None,
    }
