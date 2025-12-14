import allure
import pytest
import json
from urls import Endpoints
from data.order_data import EMPTY_INGREDIENTS, INVALID_INGREDIENTS

@allure.feature("Создание заказа")
class TestCreateOrder:
    
    @allure.title("Создание заказа с авторизацией")
    def test_create_order_with_auth(self, api_client, authorized_user):
        user_data, token = authorized_user
        headers = {"Authorization": token}
        
        with allure.step("Получение доступных ингредиентов"):
            ingredients_response = api_client.get(Endpoints.INGREDIENTS)
            assert ingredients_response.status_code == 200, "API ингредиентов должно быть доступно"
        
        ingredients_data = ingredients_response.json()
        if ingredients_data["success"] and len(ingredients_data["data"]) > 0:
            with allure.step("Создание заказа с валидными ингредиентами"):
                
                ingredient_ids = [ingredient["_id"] for ingredient in ingredients_data["data"][:3]]
                order_data = {"ingredients": ingredient_ids}
                
                response = api_client.post(Endpoints.ORDERS, headers=headers, json=order_data)
            
            with allure.step("Проверка успешного создания заказа"):
                assert response.status_code == 200, f"Ожидался код 200, получен {response.status_code}"
                response_data = response.json()
                assert response_data["success"] == True, "Поле success должно быть True"
                assert "order" in response_data, "В ответе должен быть объект order"
                assert "number" in response_data["order"], "В order должен быть номер заказа"
                assert "name" in response_data["order"], "В order должно быть имя заказа"
        else:
            pytest.skip("Нет доступных ингредиентов для создания заказа")
    
    @allure.title("Создание заказа без авторизации")
    def test_create_order_without_auth(self, api_client):
        with allure.step("Получение доступных ингредиентов"):
            ingredients_response = api_client.get(Endpoints.INGREDIENTS)
            assert ingredients_response.status_code == 200, "API ингредиентов должно быть доступно"
        
        ingredients_data = ingredients_response.json()
        if ingredients_data["success"] and len(ingredients_data["data"]) > 0:
            with allure.step("Создание заказа без авторизации"):
                
                ingredient_ids = [ingredient["_id"] for ingredient in ingredients_data["data"][:3]]
                order_data = {"ingredients": ingredient_ids}
                
                response = api_client.post(Endpoints.ORDERS, json=order_data)
            
            with allure.step("Проверка создания заказа без авторизации"):
                assert response.status_code == 200, f"Ожидался код 200, получен {response.status_code}"
                response_data = response.json()
                assert response_data["success"] == True, "Поле success должно быть True"
        else:
            pytest.skip("Нет доступных ингредиентов для создания заказа")
    
    @allure.title("Создание заказа без ингредиентов")
    def test_create_order_without_ingredients(self, api_client, authorized_user):
        user_data, token = authorized_user
        headers = {"Authorization": token}
        
        with allure.step("Отправка запроса без ингредиентов"):
            response = api_client.post(Endpoints.ORDERS, headers=headers, json=EMPTY_INGREDIENTS)
        
        with allure.step("Проверка ошибки валидации"):
            assert response.status_code == 400, f"Ожидался код 400, получен {response.status_code}"
            response_data = response.json()
            assert response_data["success"] == False, "Поле success должно быть False"
            assert "message" in response_data, "В ответе должно быть сообщение об ошибке"
    
    @allure.title("Создание заказа с неверным хешем ингредиентов")
    def test_create_order_with_invalid_ingredients(self, api_client, authorized_user):
        user_data, token = authorized_user
        headers = {"Authorization": token}
        
        with allure.step("Отправка запроса с неверными ингредиентами"):
            response = api_client.post(Endpoints.ORDERS, headers=headers, json=INVALID_INGREDIENTS)
        
        with allure.step("Проверка ошибки при неверных ингредиентах"):
           
            assert response.status_code >= 400, f"Ожидалась ошибка (4xx или 5xx), получен {response.status_code}"
            
  
            if response.text.strip():
                try:
                    response_data = response.json()
                    if "success" in response_data:
                        assert response_data["success"] == False, "Поле success должно быть False"
                except json.JSONDecodeError:
                    
                    assert len(response.text) > 0, "Ответ не должен быть пустым"