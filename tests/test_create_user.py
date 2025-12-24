import allure
import pytest
from urls import Endpoints

@allure.feature("Создание пользователя")
class TestCreateUser:
    
    @allure.title("Создание уникального пользователя")
    def test_create_unique_user_success(self, api_client, user_data):
        with allure.step("Отправка запроса на создание пользователя"):
            response = api_client.post(Endpoints.CREATE_USER, json=user_data)
        
        with allure.step("Проверка статус кода"):
            assert response.status_code == 200, f"Ожидался код 200, получен {response.status_code}"
        
        with allure.step("Проверка тела ответа"):
            response_data = response.json()
            assert response_data["success"] == True, "Поле success должно быть True"
            assert "accessToken" in response_data, "В ответе должен быть accessToken"
            assert response_data["user"]["email"] == user_data["email"], f"Email должен быть {user_data['email']}"
            assert response_data["user"]["name"] == user_data["name"], f"Имя должно быть {user_data['name']}"
    
    @allure.title("Создание пользователя, который уже зарегистрирован")
    def test_create_duplicate_user_fails(self, api_client):
        duplicate_user_data = {
            "email": "naduwka@mail.ru",
            "password": "12345@",
            "name": "Надежда"
        }
        
        with allure.step("Попытка создания дубликата пользователя"):
            response = api_client.post(Endpoints.CREATE_USER, json=duplicate_user_data)
        
        with allure.step("Проверка статус кода 403"):
            assert response.status_code == 403, f"Ожидался код 403, получен {response.status_code}"
        
        with allure.step("Проверка тела ответа при ошибке"):
            response_data = response.json()
            assert response_data["success"] == False, "Поле success должно быть False"
            assert "message" in response_data, "В ответе должно быть поле message"
    
    @allure.title("Создание пользователя без email")
    def test_create_user_without_email(self, api_client):
        data = {
            "password": "12345@",
            "name": "Test"
        }
        
        with allure.step("Отправка запроса без email"):
            response = api_client.post(Endpoints.CREATE_USER, json=data)
        
        with allure.step("Проверка ошибки валидации"):
            assert response.status_code == 403, f"Ожидался код 403, получен {response.status_code}"
            response_data = response.json()
            assert response_data["success"] == False, "Поле success должно быть False"
    
    @allure.title("Создание пользователя без пароля")
    def test_create_user_without_password(self, api_client):
        data = {
            "email": "test@test.com",
            "name": "Test"
        }
        
        with allure.step("Отправка запроса без пароля"):
            response = api_client.post(Endpoints.CREATE_USER, json=data)
        
        with allure.step("Проверка ошибки валидации"):
            assert response.status_code == 403, f"Ожидался код 403, получен {response.status_code}"
            response_data = response.json()
            assert response_data["success"] == False, "Поле success должно быть False"
    
    @allure.title("Создание пользователя без имени")
    def test_create_user_without_name(self, api_client):
        data = {
            "email": "test@test.com",
            "password": "12345@"
        }
        
        with allure.step("Отправка запроса без имени"):
            response = api_client.post(Endpoints.CREATE_USER, json=data)
        
        with allure.step("Проверка ошибки валидации"):
            assert response.status_code == 403, f"Ожидался код 403, получен {response.status_code}"
            response_data = response.json()
            assert response_data["success"] == False, "Поле success должно быть False"