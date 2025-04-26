"""
Main Flask application module that implements a web calculator.

This module provides a simple web interface for performing basic mathematical
operations such as addition, subtraction, multiplication, division, and
advanced operations like power, square root, absolute value, factorial,
and natural logarithm. It handles common errors like division by zero
and invalid inputs.
comment to re deploy

Functions:
    index(): Handles GET and POST requests for the main page.
"""

# app/app.py
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
    """
    Health check endpoint to ensure the application is running.

    Returns:
        str: "OK" if the application is running.
    """
    return "OK", 200


@app.route("/", methods=["GET", "POST"])
def index():
    """
    Handles GET and POST requests for the calculator's main page.

    GET: Displays the calculator form.
    POST: Processes the selected mathematical operation with the provided
        numbers.

    Returns:
        str: Renders the index.html template with the operation result if it
            exists. In case of error, returns a descriptive error message.
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
                    resultado = "Error: El factorial solo acepta números enteros"  # noqa: E501, E261
                except ValueError:
                    resultado = "Error: El factorial no acepta números negativos"  # noqa: E501, E261
            elif operacion == "logaritmo_natural":
                resultado = logaritmo_natural(num1)
            else:
                resultado = "Operación no válida"
        except ValueError as e:
            if "factorial" in str(e):
                resultado = "Error: El factorial no acepta números negativos"
            elif "logaritmo natural" in str(e):
                resultado = "Error: El logaritmo natural solo acepta números positivos"  # noqa: E501, E261
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
    # Remove debug=True for production
    app_port = int(os.environ.get("PORT", 5000))
    app_debug = os.environ.get("DEBUG", "False") == "True"
    print(f"Running on port {app_port} with debug={app_debug}")
    app.run(debug=app_debug, port=app_port, host="0.0.0.0")