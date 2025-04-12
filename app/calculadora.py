# app/calculadora.py
"""
Módulo de calculadora que proporciona funciones aritméticas básicas.
Implementa operaciones de suma, resta, multiplicación y división.
"""


def sumar(a, b):
    """
    Suma dos números.

    Args:
        a (float): Primer número.
        b (float): Segundo número.

    Returns:
        float: La suma de a y b.
    """
    return a + b


def restar(a, b):
    """
    Resta dos números.

    Args:
        a (float): Número del que se resta.
        b (float): Número a restar.

    Returns:
        float: La diferencia entre a y b (a - b).
    """
    return a - b


def multiplicar(a, b):
    """
    Multiplica dos números.

    Args:
        a (float): Primer factor.
        b (float): Segundo factor.

    Returns:
        float: El producto de a y b.
    """
    return a * b


def dividir(a, b):
    """
    Divide dos números.

    Args:
        a (float): Dividendo.
        b (float): Divisor.

    Returns:
        float: El cociente de a dividido por b.

    Raises:
        ZeroDivisionError: Si b es cero.
    """
    if b == 0:
        raise ZeroDivisionError("No se puede dividir por cero")
    return a / b
