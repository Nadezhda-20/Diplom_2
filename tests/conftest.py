import logging
import pytest
from helpers.api_client import ApiClient
from helpers.generators import build_user_payload
from helpers.ingredients import get_ingredient_ids
from urls import Endpoints

logger = logging.getLogger(__name__)


@pytest.fixture
def created_user():
    """Создаёт пользователя и удаляет его после теста (по accessToken)."""
    client = ApiClient(Endpoints.BASE_URL)
    payload = build_user_payload()

    response = client.post(Endpoints.CREATE_USER, json=payload)
    if response.status_code != 200:
        pytest.fail(f"Не удалось создать пользователя: {response.status_code} {response.text}")

    response_data = response.json()
    token = response_data.get("accessToken")
    if not token:
        pytest.fail(f"Не удалось получить accessToken: {response_data}")

    user = {
        "payload": payload,
        "token": token,
        "headers": {"Authorization": token},
    }

    yield user

    # teardown: удаляем пользователя по токену, который получили при регистрации
    try:
        delete_resp = client.delete(Endpoints.USER, headers=user["headers"])

        # В API Stellar Burgers удаление может возвращать 200 или 202 — оба считаем успехом
        if delete_resp.status_code not in (200, 202):
            logger.warning(
                "Не удалось удалить пользователя. status=%s body=%s",
                delete_resp.status_code,
                delete_resp.text,
            )
        else:
            logger.info(
                "Пользователь удалён. status=%s body=%s",
                delete_resp.status_code,
                delete_resp.text,
            )
    except Exception:
        logger.exception("Исключение при удалении пользователя")


@pytest.fixture
def created_order(created_user):
    """Создаёт заказ для авторизованного пользователя (предусловие для тестов получения заказов)."""
    client = ApiClient(Endpoints.BASE_URL)

    ingredient_ids = get_ingredient_ids(client, count=3)
    response = client.post(
        Endpoints.ORDERS,
        headers=created_user["headers"],
        json={"ingredients": ingredient_ids},
    )

    if response.status_code != 200:
        pytest.fail(f"Не удалось создать заказ: {response.status_code} {response.text}")

    return response.json()
