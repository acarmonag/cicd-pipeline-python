import os
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

BASE_URL = os.environ.get("APP_BASE_URL", "http://localhost:5000")

# Configuración del driver (elige uno: Chrome o Firefox)
@pytest.fixture
def browser():
    # Opción 1: Chrome (headless - sin interfaz gráfica)
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Ejecuta sin interfaz gráfica
    options.add_argument("--no-sandbox")  # Necesario para algunos entornos
    options.add_argument("--disable-dev-shm-usage")  # Necesario para algunos entornos
    driver = webdriver.Chrome(options=options)

    # Opción 2: Firefox (headless)
    # options = webdriver.FirefoxOptions()
    # options.add_argument("--headless")
    # driver = webdriver.Firefox(options=options)

    # Opción 3: Chrome (con interfaz gráfica - para depuración local)
    # driver = webdriver.Chrome()

    # Opción 4: Firefox (con interfaz gráfica)
    # driver = webdriver.Firefox()
    yield driver
    driver.quit()


# Función de ayuda para esperar y obtener el resultado
def get_resultado(browser):
    try:
        # Espera HASTA QUE el <h2> sea visible (máximo 10 segundos)
        # El h2 ahora tiene estilo rojo Lightning McQueen y borde izquierdo rojo
        resultado = WebDriverWait(browser, 10).until(
            EC.visibility_of_element_located((By.TAG_NAME, "h2"))
        )
        return resultado.text
    except TimeoutException:
        return "Error: Tiempo de espera agotado esperando el resultado."


# Funcion auxiliar para encontrar elementos:
def find_elements(browser):
    # Obtiene los elementos del formulario con estilo Lightning McQueen
    num1_input = browser.find_element(By.NAME, "num1")
    num2_input = browser.find_element(By.NAME, "num2")
    operacion_select = Select(browser.find_element(By.NAME, "operacion"))
    # El botón ahora es rojo #e30b0b con texto en mayúsculas
    calcular_button = browser.find_element(By.CSS_SELECTOR, "button[type='submit']")
    return num1_input, num2_input, operacion_select, calcular_button


@pytest.mark.parametrize(
    "num1, num2, operacion, resultado_esperado",
    [
        ("2", "3", "sumar", "Resultado: 5"),
        ("5", "2", "restar", "Resultado: 3"),
        ("4", "6", "multiplicar", "Resultado: 24"),
        ("10", "2", "dividir", "Resultado: 5"),
        ("5", "0", "dividir", "Error: No se puede dividir por cero"),
        ("abc", "def", "sumar", "Error: Introduce números válidos"),
    ],
)
def test_calculadora(browser, num1, num2, operacion, resultado_esperado):
    # Prueba la calculadora con tema de Lightning McQueen
    browser.get(BASE_URL)

    # Encuentra los elementos de la página con el nuevo estilo
    num1_input, num2_input, operacion_select, calcular_button = find_elements(browser)

    # Realiza la operacion:
    num1_input.send_keys(num1)
    num2_input.send_keys(num2)
    operacion_select.select_by_value(operacion)
    calcular_button.click()

    # Verifica con la funcion auxiliar:
    assert resultado_esperado in get_resultado(browser)