from __future__ import annotations
from typing import List
import pytest
from .api_client import ApiClient
from urls import Endpoints

def get_ingredient_ids(client: ApiClient, count: int = 3) -> List[str]:
    """Cписок валидных id ингредиентов (предусловие для тестов заказов)"""
    response = client.get(Endpoints.INGREDIENTS)
    if response.status_code != 200:
        pytest.fail(f"Не удалось получить ингредиенты: {response.status_code} {response.text}")

    payload = response.json()
    data = payload.get("data") or []
    if len(data) < count:
        pytest.fail(f"Ожидалось минимум {count} ингредиента(ов), получено: {len(data)}")

    return [item["_id"] for item in data[:count]]
