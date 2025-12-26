import allure

from helpers.api_client import ApiClient
from urls import Endpoints


@allure.feature("Логин пользователя")
class TestLoginUser:
    @allure.title("Вход под существующим пользователем")
    def test_login_existing_user_success(self, created_user):
        client = ApiClient(Endpoints.BASE_URL)
        user_data = created_user["payload"]

        login_payload = {"email": user_data["email"], "password": user_data["password"]}
        response = client.post(Endpoints.LOGIN_USER, json=login_payload)

        with allure.step("Проверка успешной авторизации"):
            assert response.status_code == 200, f"Ожидался код 200, получен {response.status_code}. body={response.text}"
            response_data = response.json()
            assert response_data["success"] is True, "Поле success должно быть True"
            assert response_data.get("accessToken"), "В ответе должен быть accessToken"
            assert response_data.get("refreshToken"), "В ответе должен быть refreshToken"
            assert response_data["user"]["email"] == user_data["email"]
            assert response_data["user"]["name"] == user_data["name"]

    @allure.title("Вход с неверным логином и паролем")
    def test_login_with_wrong_credentials(self):
        client = ApiClient(Endpoints.BASE_URL)

        response = client.post(
            Endpoints.LOGIN_USER,
            json={"email": "wrong@email.com", "password": "wrongpassword"},
        )

        with allure.step("Проверка ошибки авторизации"):
            assert response.status_code == 401, f"Ожидался код 401, получен {response.status_code}. body={response.text}"
            response_data = response.json()
            assert response_data["success"] is False, "Поле success должно быть False"
            assert response_data.get("message") == "email or password are incorrect",                 f"Некорректное message: {response_data.get('message')}"
