"""CAPA DE CONTROLADOR / API.

Recibe las peticiones HTTP del navegador, llama a la capa de lógica
(lottery.py) y devuelve JSON. También registra una "traza" para que la UI
muestre qué elementos participaron en cada request.
"""
import time

from flask import Flask, jsonify, render_template, request

import lottery

app = Flask(__name__)


class Trace:
    """Registra cada paso de la petición con su tiempo en milisegundos."""

    def __init__(self):
        self.t0 = time.perf_counter()
        self.steps = []

    def add(self, layer, action):
        ms = round((time.perf_counter() - self.t0) * 1000, 2)
        self.steps.append({"layer": layer, "action": action, "ms": ms})


@app.get("/")
def index():
    # Capa de presentación: se entrega el HTML
    return render_template("index.html", count=lottery.NUM_COUNT, max_num=lottery.MAX_NUM)


@app.get("/api/quickpick")
def quickpick():
    trace = Trace()
    trace.add("API (app.py)", "Recibe GET /api/quickpick")
    ticket = lottery.random_ticket()
    trace.add("Lógica (lottery.py)", f"random_ticket() -> {ticket}")
    trace.add("API (app.py)", "Responde JSON al navegador")
    return jsonify({"ticket": ticket, "trace": trace.steps})


@app.post("/api/jugar")
def jugar():
    trace = Trace()
    trace.add("API (app.py)", "Recibe POST /api/jugar con el boleto")

    data = request.get_json(silent=True) or {}
    ticket = data.get("ticket")

    ok, error = lottery.validate_ticket(ticket)
    trace.add("Lógica (lottery.py)", f"validate_ticket({ticket}) -> {'válido' if ok else error}")
    if not ok:
        trace.add("API (app.py)", "Responde 400 (boleto inválido)")
        return jsonify({"error": error, "trace": trace.steps}), 400

    winning = lottery.draw()
    trace.add("Lógica (lottery.py)", f"draw() -> {winning}")

    result = lottery.evaluate(ticket, winning)
    trace.add("Lógica (lottery.py)", f"evaluate() -> {result['match_count']} aciertos")

    trace.add("API (app.py)", "Responde JSON al navegador")
    return jsonify({"ticket": ticket, "winning": winning, **result, "trace": trace.steps})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
