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
    options.add_argument("--no-sandbox") # Necesario para algunos entornos
    options.add_argument("--disable-dev-shm-usage") # Necesario para algunos entornos
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
        # Espera hasta que el elemento resultado esté presente y sea visible
        wait = WebDriverWait(browser, 10)
        resultado = wait.until(
            EC.visibility_of_element_located((By.CLASS_NAME, "resultado"))
        )
        h2 = resultado.find_element(By.TAG_NAME, "h2")
        return h2.text.strip()
    except TimeoutException:
        pytest.fail("Timeout esperando el resultado")
    except Exception as e:
        pytest.fail(f"Error al obtener resultado: {str(e)}")

def find_elements(browser):
    try:
        wait = WebDriverWait(browser, 10)
        num1_input = wait.until(EC.presence_of_element_located((By.NAME, "num1")))
        num2_input = browser.find_element(By.NAME, "num2")
        operacion_select = Select(browser.find_element(By.NAME, "operacion"))
        calcular_button = browser.find_element(By.CSS_SELECTOR, "button[type='submit']")
        return num1_input, num2_input, operacion_select, calcular_button
    except Exception as e:
        pytest.fail(f"Error al encontrar elementos: {str(e)}")

@pytest.mark.parametrize(
    "num1, num2, operacion, resultado_esperado",
    [
        ("2", "3", "sumar", "Resultado: 5.0"),
        ("5", "2", "restar", "Resultado: 27.0"),
        ("4", "6", "multiplicar", "Resultado: 24.0"),
        ("10", "2", "dividir", "Resultado: 5.0"),
        ("5", "0", "dividir", "Error: No se puede dividir por cero"),
        ("abc", "def", "sumar", "Error: Introduce números válidos"),
        # Nuevos casos de prueba
        ("2", "3", "potencia", "Resultado: 8.0"),
        ("4", "0", "raiz_cuadrada", "Resultado: 2.0"),
        ("-4", "0", "raiz_cuadrada", "Error: No se puede calcular la raíz cuadrada de un número negativo"),
        ("-5", "0", "valor_absoluto", "Resultado: 5.0"),
        ("5", "0", "factorial", "Resultado: 120.0"),
        ("5.5", "0", "factorial", "Error: El factorial solo acepta números enteros"),
        ("-5", "0", "factorial", "Error: El factorial no acepta números negativos"),
        ("2.718281828459045", "0", "logaritmo_natural", "Resultado: 1.0"),
        ("0", "0", "logaritmo_natural", "Error: El logaritmo natural solo acepta números positivos"),
    ],
)
def test_calculadora(browser, num1, num2, operacion, resultado_esperado):
    try:
        browser.get(BASE_URL)
        num1_input, num2_input, operacion_select, calcular_button = find_elements(browser)
        
        num1_input.clear()
        num1_input.send_keys(num1)
        num2_input.clear()
        num2_input.send_keys(num2)
        operacion_select.select_by_value(operacion)
        calcular_button.click()
        
        resultado_actual = get_resultado(browser)
        assert resultado_actual == resultado_esperado
    except Exception as e:
        pytest.fail(f"Test falló: {str(e)}")