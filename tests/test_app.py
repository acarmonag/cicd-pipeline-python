# tests/test_app.py
import pytest
from app.app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index_get(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'<!DOCTYPE html>' in response.data  # Assuming the HTML template starts with <!DOCTYPE html>

def test_index_post_sumar(client):
    response = client.post('/', data={'num1': '2', 'num2': '3', 'operacion': 'sumar'})
    assert response.status_code == 200
    assert b'5.0' in response.data

def test_index_post_restar(client):
    response = client.post('/', data={'num1': '5', 'num2': '3', 'operacion': 'restar'})
    assert response.status_code == 200
    assert b'2.0' in response.data

def test_index_post_multiplicar(client):
    response = client.post('/', data={'num1': '2', 'num2': '3', 'operacion': 'multiplicar'})
    assert response.status_code == 200
    assert b'6.0' in response.data

def test_index_post_dividir(client):
    response = client.post('/', data={'num1': '6', 'num2': '3', 'operacion': 'dividir'})
    assert response.status_code == 200
    assert b'2.0' in response.data

def test_index_post_dividir_by_zero(client):
    response = client.post('/', data={'num1': '6', 'num2': '0', 'operacion': 'dividir'})
    assert response.status_code == 200
    assert b'Error: No se puede dividir por cero' in response.data

def test_index_post_invalid_operation(client):
    response = client.post('/', data={'num1': '6', 'num2': '3', 'operacion': 'invalid'})
    assert response.status_code == 200
    assert b'Operaci\xc3\xb3n no v\xc3\xa1lida' in response.data

def test_index_post_invalid_numbers(client):
    response = client.post('/', data={'num1': 'a', 'num2': 'b', 'operacion': 'sumar'})
    assert response.status_code == 200
    assert b'Error: Introduce n\xc3\xbameros v\xc3\xa1lidos' in response.data
    
def test_health_check(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert response.data == b'OK'

def test_index_post_potencia(client):
    response = client.post('/', data={'num1': '2', 'num2': '3', 'operacion': 'potencia'})
    assert response.status_code == 200
    assert b'8.0' in response.data

def test_index_post_raiz_cuadrada(client):
    response = client.post('/', data={'num1': '4', 'num2': '0', 'operacion': 'raiz_cuadrada'})
    assert response.status_code == 200
    assert b'2.0' in response.data

def test_index_post_raiz_cuadrada_negativa(client):
    response = client.post('/', data={'num1': '-4', 'num2': '0', 'operacion': 'raiz_cuadrada'})
    assert response.status_code == 200
    assert b'Error: No se puede calcular la ra\xc3\xadz cuadrada de un n\xc3\xbamero negativo' in response.data

def test_index_post_valor_absoluto(client):
    response = client.post('/', data={'num1': '-5', 'num2': '0', 'operacion': 'valor_absoluto'})
    assert response.status_code == 200
    assert b'5.0' in response.data

def test_index_post_factorial(client):
    response = client.post('/', data={'num1': '5', 'num2': '0', 'operacion': 'factorial'})
    assert response.status_code == 200
    assert b'120' in response.data

def test_index_post_factorial_decimal(client):
    response = client.post('/', data={'num1': '5.5', 'num2': '0', 'operacion': 'factorial'})
    assert response.status_code == 200
    assert b'Error: El factorial solo acepta n\xc3\xbameros enteros' in response.data

def test_index_post_factorial_negativo(client):
    response = client.post('/', data={'num1': '-5', 'num2': '0', 'operacion': 'factorial'})
    assert response.status_code == 200
    assert b'Error: El factorial no acepta n\xc3\xbameros negativos' in response.data

def test_index_post_logaritmo_natural(client):
    response = client.post('/', data={'num1': '2.718281828459045', 'num2': '0', 'operacion': 'logaritmo_natural'})
    assert response.status_code == 200
    assert b'1.0' in response.data

def test_index_post_logaritmo_natural_negativo(client):
    response = client.post('/', data={'num1': '-1', 'num2': '0', 'operacion': 'logaritmo_natural'})
    assert response.status_code == 200
    assert b'Error: El logaritmo natural solo acepta n\xc3\xbameros positivos' in response.data

def test_index_post_logaritmo_natural_cero(client):
    response = client.post('/', data={'num1': '0', 'num2': '0', 'operacion': 'logaritmo_natural'})
    assert response.status_code == 200
    assert b'Error: El logaritmo natural solo acepta n\xc3\xbameros positivos' in response.data
    