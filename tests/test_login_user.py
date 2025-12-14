import allure
import pytest
from urls import Endpoints

@allure.feature("Логин пользователя")
class TestLoginUser:
    
    @allure.title("Вход под существующим пользователем")
    def test_login_existing_user_success(self, api_client):
        login_data = {
            "email": "naduwka@mail.ru",
            "password": "12345@"
        }
        
        with allure.step("Отправка запроса на авторизацию"):
            response = api_client.post(Endpoints.LOGIN_USER, json=login_data)
        
        with allure.step("Проверка успешной авторизации"):
            assert response.status_code == 200, f"Ожидался код 200, получен {response.status_code}"
            response_data = response.json()
            assert response_data["success"] == True, "Поле success должно быть True"
            assert "accessToken" in response_data, "В ответе должен быть accessToken"
            assert response_data["user"]["email"] == login_data["email"], f"Email должен быть {login_data['email']}"
            assert response_data["user"]["name"] == "Надежда", "Имя должно быть 'Надежда'"
    
    @allure.title("Вход с неверным логином и паролем")
    def test_login_with_wrong_credentials(self, api_client):
        login_data = {
            "email": "wrong@email.com",
            "password": "wrongpassword"
        }
        
        with allure.step("Отправка запроса с неверными данными"):
            response = api_client.post(Endpoints.LOGIN_USER, json=login_data)
        
        with allure.step("Проверка ошибки авторизации"):
            assert response.status_code == 401, f"Ожидался код 401, получен {response.status_code}"
            response_data = response.json()
            assert response_data["success"] == False, "Поле success должно быть False"
            assert response_data["message"] == "email or password are incorrect", \
                f"Сообщение должно быть 'email or password are incorrect', получено: {response_data.get('message')}"
    
    @allure.title("Вход с неверным паролем")
    def test_login_with_wrong_password(self, api_client):
        login_data = {
            "email": "naduwka@mail.ru",
            "password": "wrongpassword"
        }
        
        with allure.step("Отправка запроса с неверным паролем"):
            response = api_client.post(Endpoints.LOGIN_USER, json=login_data)
        
        with allure.step("Проверка ошибки авторизации"):
            assert response.status_code == 401, f"Ожидался код 401, получен {response.status_code}"
            response_data = response.json()
            assert response_data["success"] == False, "Поле success должно быть False"