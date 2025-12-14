import allure
import pytest
from urls import Endpoints

@allure.feature("Получение заказов пользователя")
class TestGetUserOrders:
    
    @allure.title("Получение заказов авторизованного пользователя")
    def test_get_orders_with_auth(self, api_client, authorized_user):
        user_data, token = authorized_user
        headers = {"Authorization": token}        

        with allure.step("Создание тестового заказа"):
            ingredients_response = api_client.get(Endpoints.INGREDIENTS)
            if ingredients_response.status_code == 200:
                ingredients_data = ingredients_response.json()
                if ingredients_data["success"] and len(ingredients_data["data"]) > 0:
                    ingredient_ids = [ingredient["_id"] for ingredient in ingredients_data["data"][:3]]
                    order_data = {"ingredients": ingredient_ids}
                    
                    create_response = api_client.post(Endpoints.ORDERS, headers=headers, json=order_data)
                    assert create_response.status_code == 200, "Не удалось создать заказ для теста"
        
        with allure.step("Получение заказов пользователя"):
            response = api_client.get(Endpoints.ORDERS, headers=headers)
        
        with allure.step("Проверка успешного получения заказов"):
            assert response.status_code == 200, f"Ожидался код 200, получен {response.status_code}"
            response_data = response.json()
            assert response_data["success"] == True, "Поле success должно быть True"
            assert "orders" in response_data, "В ответе должен быть список orders"
            assert "total" in response_data, "В ответе должно быть общее количество заказов"
            assert "totalToday" in response_data, "В ответе должно быть количество заказов за сегодня"
    
    @allure.title("Получение заказов неавторизованного пользователя")
    def test_get_orders_without_auth(self, api_client):
        with allure.step("Попытка получения заказов без авторизации"):
            response = api_client.get(Endpoints.ORDERS)
        
        with allure.step("Проверка ошибки авторизации"):
            assert response.status_code == 401, f"Ожидался код 401, получен {response.status_code}"
            response_data = response.json()
            assert response_data["success"] == False, "Поле success должно быть False"
            assert response_data["message"] == "You should be authorised", \
                f"Сообщение должно быть 'You should be authorised', получено: {response_data.get('message')}"