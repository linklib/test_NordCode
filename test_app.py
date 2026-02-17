import pytest
import requests
import random
import string
import allure
from urllib.parse import urlencode

# Конфигурация
BASE_URL = "http://localhost:8080"
MOCK_URL = "http://localhost:8888"
API_KEY = "qazWSXedc"

# Вспомогательные функции
def generate_token():
    """Генерирует валидный токен (32 символа A-Z0-9)"""
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choices(chars, k=32))

def send_request(token, action):
    """Отправляет запрос к тестируемому приложению"""
    url = f"{BASE_URL}/endpoint"
    headers = {
        "X-Api-Key": API_KEY,
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json"
    }
    data = urlencode({"token": token, "action": action})
    return requests.post(url, data=data, headers=headers)

def setup_mock(endpoint, status=200):
    """Настраивает мок для внешнего сервиса"""
    mock_data = {
        "request": {"method": "POST", "url": endpoint},
        "response": {"status": status}
    }
    requests.post(f"{MOCK_URL}/__admin/mappings", json=mock_data)


def reset_mocks():
    """Сбрасывает все моки"""
    requests.post(f"{MOCK_URL}/__admin/mappings/reset")

# TODO: вывести вспомогательные функции в отдельный файл 

# Тесты
@allure.epic("Тестирование веб-сервиса")
class TestApp:    
    
    def setup_method(self):
        """Подготовка перед каждым тестом"""
        reset_mocks()
        self.valid_token = generate_token()
        
    
    @allure.story("LOGIN")
    @allure.title("Успешная аутентификация")
    def test_successful_login(self):

        allure.dynamic.description(f"Тест использует токен: {self.valid_token}")


        # Настраиваем мок
        with allure.step("Настройка мока для /auth"):
            setup_mock("/auth", 200)
        
        # Отправляем запрос
        with allure.step("Отправка запроса LOGIN"):
            response = send_request(self.valid_token, "LOGIN")
            print(response.text)            

        # Проверяем
        with allure.step("Проверка ответа"):           
            assert response.status_code == 200, f"Ожидался 200, получен {response.status_code}"
            

    @allure.story("LOGIN")
    @allure.title("Ошибка при аутентификации")
    def test_login_failed(self):
        
        setup_mock("/auth", 500)
        response = send_request(self.valid_token, "LOGIN")
        print(response.text)
        assert response.status_code == 400        
    
    def test_full_flow(self):
                
        # Настраиваем моки
        with allure.step("Настройка моков"):
            setup_mock("/auth", 200)
            setup_mock("/doAction", 200)
            
        # LOGIN
        with allure.step("Шаг 1: LOGIN"):
            response = send_request(self.valid_token, "LOGIN")
            print(response.text)
            assert response.status_code == 200, f"Ожидался 200, получен {response.status_code}"         
        
        # ACTION
        with allure.step("Шаг 2: ACTION"):
            response = send_request(self.valid_token, "ACTION")
            print(response.text)
            assert response.status_code == 200, f"Ожидался 200, получен {response.status_code}"             

        # LOGOUT
        with allure.step("Шаг 3: LOGOUT"):
            response = send_request(self.valid_token, "LOGOUT")
            print(response.text)
            assert response.status_code == 200, f"Ожидался 200, получен {response.status_code}"             

    @allure.story("ACTION")
    @allure.title("ACTION без предварительного LOGIN")
    def test_action_without_login(self):
        
        setup_mock("/doAction", 200)
        response = send_request(self.valid_token, "ACTION")
        print(response.text)
        with allure.step("Проверка ошибки"):
            assert response.status_code == 400, f"Ожидался 400, получен {response.status_code}"             
    
    @allure.story("Валидация")
    @allure.title("Невалидные токены")
    def test_invalid_token(self):

# TODO: Вынести генерацию невалидного токена во вспомогательную функцию         
        invalid_tokens = [
            "short",
            "A" * 40,
            "abc123"            
        ]
        
        for token in invalid_tokens:
            with allure.step(f"Проверка токена: {token}"):
                response = send_request(token, "LOGIN")
                print(response.text)
                assert response.status_code == 400, f"Ожидался 400, получен {response.status_code}"                 

   

# TODO: вывести настройки и подключение к эндпоинтам в фикстуры        