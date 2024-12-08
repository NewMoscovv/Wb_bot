import asyncpg
from config import POSTGRES_DSN
from redis_cache import cache_warehouse_data
from datetime import datetime


# Инициализация базы данных
async def init_db():
    conn = await asyncpg.connect(POSTGRES_DSN)
    await conn.execute("""
        CREATE TABLE IF NOT EXISTS warehouses (
            id SERIAL PRIMARY KEY,
            warehouse_id BIGINT NOT NULL,
            name VARCHAR(255) NOT NULL,
            coefficient FLOAT NOT NULL,
            box_type_name VARCHAR(255) NOT NULL,
            date VARCHAR(255) NOT NULL
        );
    """)
    await conn.close()


# Сохранение данных о складах в базу данных с кэшированием
async def save_warehouse_data(data):
    """
    Сохраняет данные в базу данных и кэширует их в Redis.
    :param data: Список данных о складах.
    """
    conn = await asyncpg.connect(POSTGRES_DSN)
    async with conn.transaction():
        # Получаем текущую дату в нужном формате
        current_date = datetime.now().strftime('%Y-%m-%dT00:00:00Z')
        # Удаляем старые данные для текущего дня
        await conn.execute("""
            DELETE FROM warehouses WHERE date = $1
        """, current_date)

        for entry in data:
            if entry['date'] == current_date:
                # Сохранение данных в базу данных
                await conn.execute("""
                    INSERT INTO warehouses (warehouse_id, name, coefficient, box_type_name, date)
                    VALUES ($1, $2, $3, $4, $5)
                """, entry['warehouseID'], entry['warehouseName'], entry['coefficient'], entry['boxTypeName'], entry['date'])

                # Подготовка данных для кэширования
                warehouse_records = await conn.fetch("""
                    SELECT warehouse_id, box_type_name, coefficient
                    FROM warehouses
                    WHERE name = $1
                """, entry['warehouseName'])

                # Преобразование asyncpg.Record в список словарей
                warehouse_data = [dict(record) for record in warehouse_records]

                # Кэширование данных по названию склада
                await cache_warehouse_data(entry['warehouseName'], warehouse_data)
    await conn.close()


# Получение данных о складе по названию
async def get_warehouse_data_by_name(name):
    conn = await asyncpg.connect(POSTGRES_DSN)
    records = await conn.fetch("""
        SELECT warehouse_id, box_type_name, coefficient FROM warehouses
        WHERE name = $1
    """, name)
    await conn.close()
    return [dict(record) for record in records]
