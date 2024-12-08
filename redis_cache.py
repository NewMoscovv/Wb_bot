import redis.asyncio as redis
import json
from config import REDIS_HOST, REDIS_PORT

# Инициализация клиента Redis
redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)


# Сохранение данных о складе в кэш Redis
async def cache_warehouse_data(name, data):
    """
    Сохраняет данные о складе в Redis.
    :param name: Название склада (ключ).
    :param data: Данные склада (значение).
    """
    await redis_client.set(name, json.dumps(data))


# Получение данных из кэша Redis
async def get_cached_data(name):
    """
    Получает данные о складе из Redis.
    :param name: Название склада (ключ).
    :return: Расшифрованные данные (или None, если данные не найдены).
    """
    data = await redis_client.get(name)
    if data:
        return json.loads(data)  # Декодирование JSON
    return None
