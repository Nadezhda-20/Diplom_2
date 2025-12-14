import requests
import allure

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