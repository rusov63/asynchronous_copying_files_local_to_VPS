from dotenv import load_dotenv
import os


load_dotenv(override=True)


# Получаем данные из переменных окружения
HOST: str = os.getenv("HOST")
USERNAME: str = os.getenv("USERNAME")
PASSWORD: str = os.getenv("PASSWORD")
ENCRYPTION_ALGS: str = os.getenv("ENCRYPTION_ALGS")


class ConfigServer():
    HOST = str(os.getenv("HOST"))
    USERNAME = str(os.getenv("USERNAME"))
    PASSWORD =  str(os.getenv("PASSWORD"))
    ENCRYPTION_ALGS = os.getenv("ENCRYPTION_ALGS")


TIMEOUTERROR_MESSAGE: str = "\nСервер не отвечает на запросы."

CANCELLED_MESSAGE: str = "\nОперация была отменена пользователем."

ERROR_MESSAGE: str = "\nОшибка выполнения команды: {e}."

EXCEPTION_MESSAGE: str = "\nПроизошла ошибка: {e}."

PERMISSION_MESSAGE: str = "\nНет прав для подключения к серверу."

CHANNEL_MESSAGE: str = "\nОшибка открытия канала."
