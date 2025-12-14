import sys
import os
import pytest
import allure
import requests
import random
import string

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from urls import Endpoints

class ApiClient:
    def __init__(self, base_url):
        self.base_url = base_url
    
    @allure.step("POST запрос на {endpoint}")
    def post(self, endpoint, json=None, headers=None):
        return requests.post(endpoint, json=json, headers=headers)
    
    @allure.step("GET запрос на {endpoint}")
    def get(self, endpoint, headers=None):
        return requests.get(endpoint, headers=headers)
    
    @allure.step("DELETE запрос на {endpoint}")
    def delete(self, endpoint, headers=None):
        return requests.delete(endpoint, headers=headers)

def generate_random_email():
    random_str = ''.join(random.choices(string.ascii_lowercase, k=10))
    return f"test_{random_str}_{random.randint(1000, 9999)}@example.com"

def generate_random_password(length=8):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for i in range(length))

@pytest.fixture
def api_client():
    return ApiClient(Endpoints.BASE_URL)

@pytest.fixture
def user_data():
    return {
        "email": generate_random_email(),
        "password": generate_random_password(),
        "name": "Test User"
    }

@pytest.fixture
def existing_user_data():
    return {
        "email": "naduwka20@mail.ru",
        "password": "12345",
        "name": "Надежда"
    }

@pytest.fixture
def registered_user(api_client, user_data):
    """Фикстура для создания и удаления пользователя"""
    
    response = api_client.post(Endpoints.CREATE_USER, json=user_data)
    assert response.status_code == 200, f"Ошибка при создании пользователя: {response.text}"
    token = response.json()["accessToken"]
    
    yield user_data, token    

    headers = {"Authorization": token}
    try:
        api_client.delete(Endpoints.USER, headers=headers)
    except Exception as e:
        print(f"Ошибка при удалении пользователя: {e}")

@pytest.fixture
def authorized_user(api_client, user_data):
    """Фикстура для создания пользователя и получения токена"""
   
    response = api_client.post(Endpoints.CREATE_USER, json=user_data)
    assert response.status_code == 200, f"Ошибка при создании пользователя: {response.text}"
    token = response.json()["accessToken"]
    
    yield user_data, token    
   
    headers = {"Authorization": token}
    try:
        api_client.delete(Endpoints.USER, headers=headers)
    except Exception as e:
        print(f"Ошибка при удалении пользователя: {e}")

@pytest.fixture
def created_order(api_client, authorized_user):
    """Фикстура для создания заказа"""
    user_data, token = authorized_user
    headers = {"Authorization": token}    

    ingredients_response = api_client.get(Endpoints.INGREDIENTS)
    assert ingredients_response.status_code == 200
    
    ingredients_data = ingredients_response.json()
    if ingredients_data["success"] and len(ingredients_data["data"]) > 0:        
        ingredient_ids = [ingredient["_id"] for ingredient in ingredients_data["data"][:3]]
        order_data = {"ingredients": ingredient_ids}
        
        response = api_client.post(Endpoints.ORDERS, headers=headers, json=order_data)
        return response
    else:
        pytest.skip("Нет доступных ингредиентов для создания заказа")