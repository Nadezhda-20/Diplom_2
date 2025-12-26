import allure

from data.order_data import EMPTY_INGREDIENTS, INVALID_INGREDIENTS
from helpers.api_client import ApiClient
from helpers.ingredients import get_ingredient_ids
from urls import Endpoints


@allure.feature("Создание заказа")
class TestCreateOrder:
    @allure.title("Создание заказа с авторизацией")
    def test_create_order_with_auth(self, created_user):
        client = ApiClient(Endpoints.BASE_URL)
        ingredient_ids = get_ingredient_ids(client, count=3)

        response = client.post(
            Endpoints.ORDERS,
            headers=created_user["headers"],
            json={"ingredients": ingredient_ids},
        )

        with allure.step("Проверка успешного создания заказа по документации"):
            assert response.status_code == 200, (
                f"Ожидался код 200, получен {response.status_code}. body={response.text}"
            )
            response_data = response.json()
            assert response_data.get("success") is True
            assert "order" in response_data
            assert "number" in response_data["order"]
          
            assert "name" in response_data
            assert response_data["name"], "Поле name не должно быть пустым"

    @allure.title("Создание заказа без авторизации")
    def test_create_order_without_auth(self):
        client = ApiClient(Endpoints.BASE_URL)
        ingredient_ids = get_ingredient_ids(client, count=3)

        response = client.post(
            Endpoints.ORDERS,
            json={"ingredients": ingredient_ids},
        )

        with allure.step("Проверка успешного создания заказа по документации"):
            assert response.status_code == 200, (
                f"Ожидался код 200, получен {response.status_code}. body={response.text}"
            )
            response_data = response.json()
            assert response_data.get("success") is True
            assert "order" in response_data
            assert "number" in response_data["order"]
            assert "name" in response_data
            assert response_data["name"], "Поле name не должно быть пустым"

    @allure.title("Создание заказа без ингредиентов")
    def test_create_order_without_ingredients_fails(self):
        client = ApiClient(Endpoints.BASE_URL)

        response = client.post(Endpoints.ORDERS, json=EMPTY_INGREDIENTS)

        with allure.step("Проверка ошибки по документации"):
            assert response.status_code == 400, (
                f"Ожидался код 400, получен {response.status_code}. body={response.text}"
            )
            response_data = response.json()
            assert response_data.get("success") is False
            assert response_data.get("message") == "Ingredient ids must be provided", (
                f"Некорректное message: {response_data.get('message')}"
            )

    @allure.title("Создание заказа с неверным хешем ингредиентов")
    def test_create_order_with_invalid_ingredients_fails(self, created_user):
        client = ApiClient(Endpoints.BASE_URL)

        response = client.post(
            Endpoints.ORDERS,
            headers=created_user["headers"],
            json=INVALID_INGREDIENTS,
        )

        with allure.step("Проверка ошибки по документации"):
            assert response.status_code == 500, (
                f"Ожидался код 500, получен {response.status_code}. body={response.text}"
            )
          
            allure.attach(
                response.text,
                name="Response body (500)",
                attachment_type=allure.attachment_type.TEXT,
            )
            assert response.text.strip() != "", "Тело ответа не должно быть пустым"
