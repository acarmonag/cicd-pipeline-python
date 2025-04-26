# tests/test_calculadora.py
import pytest
from app.calculadora import (
    sumar, restar, multiplicar, dividir,
    potencia, raiz_cuadrada, valor_absoluto,
    factorial, logaritmo_natural
)

def test_sumar():
    assert sumar(2, 3) == 5
    assert sumar(-1, 1) == 0
    assert sumar(0, 0) == 0

def test_restar():
    assert restar(5, 2) == 3
    assert restar(1, -1) == 2
    assert restar(0, 0) == 0

def test_multiplicar():
    assert multiplicar(2, 3) == 6
    assert multiplicar(-1, 5) == -5
    assert multiplicar(0, 10) == 0

def test_dividir():
    assert dividir(10, 2) == 5.0
    assert dividir(5, -1) == -5.0
    with pytest.raises(ZeroDivisionError):
        dividir(1, 0)

def test_potencia():
    assert potencia(2, 3) == 8
    assert potencia(5, 0) == 1
    assert potencia(2, -1) == 0.5
    assert potencia(0, 5) == 0

def test_raiz_cuadrada():
    assert raiz_cuadrada(4) == 2.0
    assert raiz_cuadrada(0) == 0.0
    assert raiz_cuadrada(2) == pytest.approx(1.4142135623730951)
    with pytest.raises(ValueError):
        raiz_cuadrada(-1)

def test_valor_absoluto():
    assert valor_absoluto(5) == 5
    assert valor_absoluto(-5) == 5
    assert valor_absoluto(0) == 0
    assert valor_absoluto(-3.14) == 3.14

def test_factorial():
    assert factorial(0) == 1
    assert factorial(1) == 1
    assert factorial(5) == 120
    with pytest.raises(ValueError):
        factorial(-1)
    with pytest.raises(TypeError):
        factorial(3.14)

def test_logaritmo_natural():
    assert logaritmo_natural(1) == 0.0
    assert logaritmo_natural(2.718281828459045) == pytest.approx(1.0)
    with pytest.raises(ValueError):
        logaritmo_natural(0)
    with pytest.raises(ValueError):
        logaritmo_natural(-1)