# Загрузка переменных окружения из .env
from dotenv import load_dotenv
import os

load_dotenv()

# Telegram Bot Token
TELEGRAM_TOKEN = os.getenv("BOT_TOKEN")

# Wildberries API Token
WILDBERRIES_TOKEN = os.getenv("WILDBERRIES_TOKEN")

# Строка подключения к PostgreSQL
POSTGRES_DSN = os.getenv("POSTGRES_DSN")

# Настройки подключения к Redis
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
