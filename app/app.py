"""
Flask application module implementing a web calculator.

Provides a simple web interface for basic and advanced mathematical operations:
addition, subtraction, multiplication, division, power, square root,
absolute value, factorial, and natural logarithm.
"""

from flask import Flask, render_template, request
from .calculadora import (
    sumar,
    restar,
    multiplicar,
    dividir,
    potencia,
    raiz_cuadrada,
    valor_absoluto,
    factorial,
    logaritmo_natural,
)
import os

app = Flask(__name__)


@app.route("/health")
def health():
    """Health check endpoint."""
    return "OK", 200


@app.route("/", methods=["GET", "POST"])
def index():
    """
    Handles GET and POST requests for the calculator's main page.

    GET: Displays the calculator form.
    POST: Processes the selected mathematical operation with the provided numbers.
    """
    resultado = None
    if request.method == "POST":
        try:
            num1 = float(request.form["num1"])
            num2 = float(request.form["num2"])
            operacion = request.form["operacion"]

            if operacion == "sumar":
                resultado = sumar(num1, num2)
            elif operacion == "restar":
                resultado = restar(num1, num2)
            elif operacion == "multiplicar":
                resultado = multiplicar(num1, num2)
            elif operacion == "dividir":
                resultado = dividir(num1, num2)
            elif operacion == "potencia":
                resultado = potencia(num1, num2)
            elif operacion == "raiz_cuadrada":
                resultado = raiz_cuadrada(num1)
            elif operacion == "valor_absoluto":
                resultado = valor_absoluto(num1)
            elif operacion == "factorial":
                try:
                    resultado = factorial(num1)
                except TypeError:
                    resultado = "Error: El factorial solo acepta números enteros"  # noqa: E501
                except ValueError:
                    resultado = "Error: El factorial no acepta números negativos"  # noqa: E501
            elif operacion == "logaritmo_natural":
                resultado = logaritmo_natural(num1)
            else:
                resultado = "Operación no válida"
        except ValueError as e:
            if "factorial" in str(e):
                resultado = "Error: El factorial no acepta números negativos"
            elif "logaritmo natural" in str(e):
                resultado = "Error: El logaritmo natural solo acepta números positivos"  # noqa: E501
            elif "raíz cuadrada" in str(e):
                resultado = (
                    "Error: No se puede calcular la raíz cuadrada de un "
                    "número negativo"
                )
            else:
                resultado = "Error: Introduce números válidos"
        except ZeroDivisionError:
            resultado = "Error: No se puede dividir por cero"

    return render_template("index.html", resultado=resultado)


if __name__ == "__main__":  # pragma: no cover
    app_port = int(os.environ.get("PORT", 5000))
    app_debug = os.environ.get("DEBUG", "False") == "True"
    print(f"Running on port {app_port} with debug={app_debug}")
    app.run(debug=app_debug, port=app_port, host="0.0.0.0")
