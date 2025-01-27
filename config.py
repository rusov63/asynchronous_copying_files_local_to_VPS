from dotenv import load_dotenv
import os


load_dotenv(override=True)


# Получаем данные из переменных окружения
HOST = os.getenv("HOST")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
ENABLE_PASSWORD = os.getenv("ENABLE_PASSWORD")
ENCRYPTION_ALGS = os.getenv("ENCRYPTION_ALGS")
