import asyncio
from aiogram import Bot, Dispatcher
from config import TELEGRAM_TOKEN
from db import init_db, save_warehouse_data
from wildberries_api import get_warehouses, get_coefficients
from handlers import router


# Основная логика запуска
async def main():
    # Инициализация базы данных
    await init_db()

    # Получение данных с API Wildberries
    warehouses = get_warehouses()  # Список складов
    coefficients = get_coefficients()  # Коэффициенты

    # Формирование данных для записи в базу
    data = []
    for coef in coefficients:
        data.append({
            "warehouseID": coef["warehouseID"],
            "warehouseName": coef["warehouseName"],
            "coefficient": coef["coefficient"],
            "boxTypeName": coef["boxTypeName"],
            "date": coef["date"]
        })
    await save_warehouse_data(data)

    # Инициализация Telegram-бота
    bot = Bot(token=TELEGRAM_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)  # Добавление хендлеров

    await dp.start_polling(bot)  # Запуск бота
    await redis_client.close()

if __name__ == "__main__":
    try:
        print('бот включен')
        asyncio.run(main())
    except KeyboardInterrupt:
        print('бот отключен')
