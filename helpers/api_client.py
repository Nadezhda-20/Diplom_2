from __future__ import annotations
from urllib.parse import urljoin
from typing import Any, Optional, Dict
import allure
import requests

class ApiClient:   
    def __init__(self, base_url: str, timeout: float = 10.0):
        self.base_url = base_url.rstrip("/") + "/"
        self.timeout = timeout

    def _resolve_url(self, endpoint: str) -> str:
        if endpoint.startswith("http://") or endpoint.startswith("https://"):
            return endpoint
        return urljoin(self.base_url, endpoint.lstrip("/"))

    @allure.step("POST {endpoint}")
    def post(
        self,
        endpoint: str,
        json: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> requests.Response:
        url = self._resolve_url(endpoint)
        return requests.post(url, json=json, headers=headers, timeout=self.timeout)

    @allure.step("GET {endpoint}")
    def get(
        self,
        endpoint: str,
        headers: Optional[Dict[str, str]] = None,
    ) -> requests.Response:
        url = self._resolve_url(endpoint)
        return requests.get(url, headers=headers, timeout=self.timeout)

    @allure.step("DELETE {endpoint}")
    def delete(
        self,
        endpoint: str,
        headers: Optional[Dict[str, str]] = None,
    ) -> requests.Response:
        url = self._resolve_url(endpoint)
        return requests.delete(url, headers=headers, timeout=self.timeout)

