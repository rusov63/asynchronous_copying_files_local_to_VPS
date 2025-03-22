import asyncio
import asyncssh
from config import HOST, PASSWORD, USERNAME, ENCRYPTION_ALGS, CANCELLED_MESSAGE, ERROR_MESSAGE, \
    EXCEPTION_MESSAGE, TIMEOUTERROR_MESSAGE, PERMISSION_MESSAGE, CHANNEL_MESSAGE
from logs.logger_config import setup_logger

logger = setup_logger(__name__)

async def validate_connection_settings(limit: int = 3, delay: int = 5) -> bool:
    """
    Проверяет настройки подключения к SSH-серверу.

    Эта асинхронная функция выполняет следующие действия:
    1. Проверяет наличие необходимых учетных данных (HOST, USERNAME, PASSWORD).
    2. Устанавливает соединение с SSH-сервером, используя указанные учетные данные и алгоритмы шифрования.
    3. Обрабатывает возможные ошибки подключения и открытого канала.
    4. Если соединение не удается, функция будет повторять попытки в течение заданного количества раз с
    указанной задержкой.

    :arg
        limit (int): Максимальное количество попыток подключения (по умолчанию 3).
        delay (int): Задержка между попытками подключения в секундах (по умолчанию 5).

    :return
        Bool: True, если подключение успешно, иначе False.
        Выводит информацию о подключении и возможных ошибках.

    :except
        Вызывает различные исключения в случае ошибок подключения, аутентификации или других проблем.
    """
    attempts = 0
    while limit > attempts:
        try:
            print('Проверка подключения к серверу...')

            # Проверяем, что все необходимые переменные окружения установлены
            if not HOST or not PASSWORD or not USERNAME:
                logger.info(f"Ошибка: учетные данные не заданы", exc_info=True)
                print(f"\nОшибка: учетные данные не заданы.")
                return False

            await asyncio.sleep(.1)

            async with asyncssh.connect(
                    host=HOST,
                    username=USERNAME,
                    password=PASSWORD,
                    encryption_algs=ENCRYPTION_ALGS,
                    connect_timeout=3
            ) as conn:
                print(f"Успешное подключение к серверу\n")

                # Получаем дополнительную информацию о соединении
                print(f'Учетные данные:')
                print(f"Host: {conn.get_extra_info('host')}")
                print(f"Port: {conn.get_extra_info('port')}")
                print(f"Username: {conn.get_extra_info('username')}")

                return True

        except asyncio.TimeoutError:
            logger.error(f"Сервер не отвечает на запросы", exc_info=True)
            print(TIMEOUTERROR_MESSAGE)

        except asyncio.CancelledError:
            logger.warning(f"Операция была отменена пользователем", exc_info=True)
            print(CANCELLED_MESSAGE)
            return False

        except (asyncssh.Error, OSError, AttributeError) as e:
            logger.error(f"Ошибка выполнения команды: {str(e)}", exc_info=True)
            print(ERROR_MESSAGE.format(e=e))

        except asyncssh.misc.PermissionDenied:
            logger.error(f"Нет прав для подключения к серверу", exc_info=True)
            print(PERMISSION_MESSAGE)

        except asyncssh.ChannelOpenError:
            logger.error(f"Ошибка открытия канала", exc_info=True)
            print(CHANNEL_MESSAGE)

        except Exception as e:
            logger.error(f"Неожиданная ошибка: {str(e)}", exc_info=True)
            print(EXCEPTION_MESSAGE.format(e=e))


        if limit > attempts:
            attempts += 1
            print(f'Повторная попытка подключения через {delay} секунд.\n')
            await asyncio.sleep(delay)

    if limit == attempts:
        print("\nПревышено максимальное количество попыток подключения.")
        return False

