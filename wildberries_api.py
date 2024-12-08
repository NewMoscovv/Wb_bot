import requests
from config import WILDBERRIES_TOKEN

BASE_URL = "https://supplies-api.wildberries.ru/api/v1"


# Получение списка складов через API Wildberries
def get_warehouses():
    headers = {"Authorization": WILDBERRIES_TOKEN}
    response = requests.get(f"{BASE_URL}/warehouses", headers=headers)
    response.raise_for_status()  # Проверка на ошибки
    return response.json()


# Получение коэффициентов для складов через API Wildberries
def get_coefficients():
    headers = {"Authorization": WILDBERRIES_TOKEN}
    response = requests.get(f"{BASE_URL}/acceptance/coefficients", headers=headers)
    response.raise_for_status()  # Проверка на ошибки
    return response.json()

