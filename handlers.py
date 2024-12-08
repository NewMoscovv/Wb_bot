from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from db import get_warehouse_data_by_name
from redis_cache import get_cached_data, cache_warehouse_data

router = Router(name="router")


@router.message(Command("start"))
async def start(message: Message):
    await message.answer("Привет! Отправь мне название склада, чтобы получить его данные.")


@router.message()
# Обработчик для получения информации о складе
async def get_warehouse_info(message: Message):
    """
    Отправляет информацию о складе на основе названия.
    """
    warehouse_name = message.text.strip()
    cached_data = await get_cached_data(warehouse_name)

    if not cached_data:
        await message.answer("Информация о складе не найдена.")
        return

    # Форматируем данные о складе
    formatted_data = format_warehouse_data(cached_data)
    # Разбиваем текст на части
    messages = split_message(formatted_data)

    # Отправляем каждую часть отдельно
    for msg in messages:
        await message.answer(msg)


# Функция для форматирования данных о складе
def format_warehouse_data(data):
    """
    Форматирует данные склада для вывода в сообщение Telegram.
    :param data: Список словарей с информацией о складах.
    :return: Отформатированная строка.
    """
    result = []
    for entry in data:
        result.append(
            f"ID склада: {entry['warehouse_id']}\n"
            f"Тип коробки: {entry['box_type_name']}\n"
            f"Коэффициент: {entry['coefficient']}\n"
            "------------------------"
        )
    return "\n".join(result)


# Функция для разбиения текста на части
def split_message(text, max_length=4096):
    """
    Разбивает текст на части, чтобы каждая часть была не длиннее max_length символов.
    """
    chunks = []
    while len(text) > max_length:
        # Ищем последний перенос строки перед ограничением длины
        split_index = text[:max_length].rfind('\n')
        if split_index == -1:  # Если перенос строки не найден, режем принудительно
            split_index = max_length
        chunks.append(text[:split_index])
        text = text[split_index:].lstrip()  # Удаляем лишние пробелы или переносы строк
    chunks.append(text)  # Добавляем оставшийся текст
    return chunks
