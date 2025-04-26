# app/calculadora.py
"""
Calculator module that provides basic mathematical operations.

This module implements the core mathematical operations used by the calculator
web application. All functions accept numeric parameters and return the
result of the operation.

Functions:
    sumar(a, b): Returns the sum of two numbers
    restar(a, b): Returns the difference between two numbers
    multiplicar(a, b): Returns the product of two numbers
    dividir(a, b): Returns the quotient of two numbers
    potencia(base, exponente): Returns base raised to the power of exponente
    raiz_cuadrada(n): Returns the square root of a number
    valor_absoluto(n): Returns the absolute value of a number
    factorial(n): Returns the factorial of a number
    logaritmo_natural(n): Returns the natural logarithm of a number
"""


def sumar(a, b):
    """
    Add two numbers together.

    Args:
        a (float): First number
        b (float): Second number

    Returns:
        float: The sum of a and b
    """
    return a + b


def restar(a, b):
    """
    Subtract the second number from the first.

    Args:
        a (float): Number to subtract from
        b (float): Number to subtract

    Returns:
        float: The difference between a and b
    """
    return a - b


def multiplicar(a, b):
    """
    Multiply two numbers together.

    Args:
        a (float): First number
        b (float): Second number

    Returns:
        float: The product of a and b
    """
    return a * b


def dividir(a, b):
    """
    Divide the first number by the second.

    Args:
        a (float): Numerator
        b (float): Denominator

    Returns:
        float: The quotient of a divided by b

    Raises:
        ZeroDivisionError: If b is zero
    """
    if b == 0:
        raise ZeroDivisionError("No se puede dividir por cero")
    return a / b


def potencia(base, exponente):
    """
    Calculate base raised to the power of exponente.

    Args:
        base (float): The base number
        exponente (float): The exponent

    Returns:
        float: base raised to the power of exponente
    """
    return base**exponente


def raiz_cuadrada(n):
    """
    Calculate the square root of a number.

    Args:
        n (float): The number to calculate square root of

    Returns:
        float: The square root of n

    Raises:
        ValueError: If n is negative
    """
    if n < 0:
        raise ValueError(
            "No se puede calcular la raíz cuadrada de un número negativo"
        )  # noqa: E501, E261
    return n**0.5


def valor_absoluto(n):
    """
    Calculate the absolute value of a number.

    Args:
        n (float): The number to calculate absolute value of

    Returns:
        float: The absolute value of n
    """
    return abs(n)


def factorial(n):
    """
    Calculate the factorial of a number.

    Args:
        n (int): The number to calculate factorial of

    Returns:
        int: The factorial of n

    Raises:
        ValueError: If n is negative
        TypeError: If n is not an integer
    """
    # Verificar si el número es decimal
    if isinstance(n, float) and n != int(n):
        raise TypeError("El factorial solo está definido para números enteros")
    # Convertir a entero si es un float sin parte decimal
    if isinstance(n, float):
        n = int(n)

    if not isinstance(n, int):
        raise TypeError("El factorial solo está definido para números enteros")
    if n < 0:
        raise ValueError(
            "El factorial no está definido para números negativos"
        )  # noqa: E501, E261
    if n == 0:
        return 1
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result


def logaritmo_natural(n):
    """
    Calculate the natural logarithm of a number.

    Args:
        n (float): The number to calculate natural logarithm of

    Returns:
        float: The natural logarithm of n

    Raises:
        ValueError: If n is less than or equal to 0
    """
    if n <= 0:
        raise ValueError(
            "El logaritmo natural no está definido para números menores o "
            "iguales a cero"
        )
    from math import log

    return log(n)