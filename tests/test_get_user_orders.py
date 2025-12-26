import allure

from helpers.api_client import ApiClient
from urls import Endpoints


@allure.feature("Получение заказов пользователя")
class TestGetUserOrders:
    @allure.title("Получение заказов авторизованного пользователя")
    def test_get_orders_with_auth(self, created_user, created_order):
        client = ApiClient(Endpoints.BASE_URL)

        with allure.step("Получить список заказов пользователя"):
            response = client.get(Endpoints.ORDERS, headers=created_user["headers"])

        with allure.step("Проверка успешного ответа"):
            assert response.status_code == 200, f"Ожидался код 200, получен {response.status_code}. body={response.text}"
            response_data = response.json()
            assert response_data["success"] is True
            assert "orders" in response_data
            assert "total" in response_data
            assert "totalToday" in response_data

    @allure.title("Получение заказов неавторизованного пользователя")
    def test_get_orders_without_auth(self):
        client = ApiClient(Endpoints.BASE_URL)

        response = client.get(Endpoints.ORDERS)

        with allure.step("Проверка ошибки авторизации"):
            assert response.status_code == 401, f"Ожидался код 401, получен {response.status_code}. body={response.text}"
            response_data = response.json()
            assert response_data["success"] is False
            assert response_data.get("message") == "You should be authorised", (
                f"Некорректное message: {response_data.get('message')}"
            )
