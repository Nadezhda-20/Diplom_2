import allure
import pytest

from helpers.api_client import ApiClient
from helpers.generators import build_user_payload
from urls import Endpoints


@allure.feature("Создание пользователя")
class TestCreateUser:
    @allure.title("Создание уникального пользователя")
    def test_create_unique_user_success(self):
        client = ApiClient(Endpoints.BASE_URL)
        payload = build_user_payload()

        response = client.post(Endpoints.CREATE_USER, json=payload)

        token = None
        try:
            with allure.step("Проверка успешного ответа"):
                assert response.status_code == 200, (
                    f"Ожидался код 200, получен {response.status_code}. body={response.text}"
                )
                response_data = response.json()
                assert response_data["success"] is True
                assert "accessToken" in response_data
                assert "refreshToken" in response_data
                assert response_data["user"]["email"] == payload["email"]
                assert response_data["user"]["name"] == payload["name"]

                token = response_data.get("accessToken")
        finally:
            if token:
                client.delete(Endpoints.USER, headers={"Authorization": token})

    @allure.title("Создание пользователя, который уже зарегистрирован")
    def test_create_duplicate_user_fails(self, created_user):
        client = ApiClient(Endpoints.BASE_URL)
        user_data = created_user["payload"]

        response = client.post(Endpoints.CREATE_USER, json=user_data)

        with allure.step("Проверка ошибки дубликата"):
            assert response.status_code == 403, f"Ожидался код 403, получен {response.status_code}. body={response.text}"
            response_data = response.json()
            assert response_data["success"] is False
            assert response_data.get("message") == "User already exists", (
                f"Некорректное message: {response_data.get('message')}"
            )

    @allure.title("Создание пользователя без обязательного поля")
    @pytest.mark.parametrize("missing_key", ["email", "password", "name"])
    def test_create_user_without_required_field(self, missing_key):
        client = ApiClient(Endpoints.BASE_URL)
        payload = build_user_payload()
        payload.pop(missing_key, None)

        response = client.post(Endpoints.CREATE_USER, json=payload)

        with allure.step("Проверка ошибки валидации"):
            assert response.status_code == 403, f"Ожидался код 403, получен {response.status_code}. body={response.text}"
            response_data = response.json()
            assert response_data["success"] is False
            assert response_data.get("message") == "Email, password and name are required fields", (
                f"Некорректное message: {response_data.get('message')}"
            )
