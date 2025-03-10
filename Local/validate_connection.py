import asyncio
import sys
import asyncssh

from config import HOST, PASSWORD, USERNAME, ENCRYPTION_ALGS


async def validate_connection_settings() -> None:
    """
    Проверяет настройки подключения к SSH-серверу.

    Эта асинхронная функция выполняет следующие действия:
    1. Проверяет наличие необходимых учетных данных (HOST, USERNAME, PASSWORD).
    2. Устанавливает соединение с SSH-сервером, используя указанные учетные данные и алгоритмы шифрования.
    3. Получает и выводит дополнительную информацию о соединении, такую как хост, порт и имя пользователя.
    4. Обрабатывает возможные ошибки подключения и открытия канала.

    Исключения:
        - asyncssh.Error: Общее исключение для ошибок, связанных с SSH.
        - OSError: Ошибка ввода-вывода, возникающая при попытке подключения.
        - asyncssh.misc.PermissionDenied: Ошибка, возникающая, если у пользователя нет прав для подключения к серверу.
        - asyncssh.ChannelOpenError: Ошибка, возникающая при попытке открыть канал.

    Возвращает:
        None: Функция не возвращает значения, но выводит информацию о подключении и возможных ошибках.
    """
    try:
        print('Проверка подключения к серверу...')

        # Проверяем, что все необходимые переменные окружения установлены
        if not HOST or not PASSWORD or not USERNAME:
            print(f"Ошибка: учетные данные не заданы")
            sys.exit(1)

        await asyncio.sleep(0.1)

        async with asyncssh.connect(
                host=HOST,
                username=USERNAME,
                password=PASSWORD,
                encryption_algs=ENCRYPTION_ALGS,
                connect_timeout=3
        ) as conn:
            print(f"Успешное подключение к серверу")

            # Получаем дополнительную информацию о соединении
            host_info = conn.get_extra_info('host')
            port_info = conn.get_extra_info('port')
            username_info = conn.get_extra_info('username')

            # Выводим информацию
            print(f'Учетные данные:')
            print(f"Host: {host_info}")
            print(f"Port: {port_info}")
            print(f"Username: {username_info}")

    except (asyncssh.Error, OSError) as e:
        print(f'Ошибка подключения/выполнения команды: {e}')

    except asyncssh.misc.PermissionDenied:
        print("Нет прав для подключения к серверу")
        sys.exit(1)

    except asyncssh.ChannelOpenError as e:
        print(f"Ошибка открытия канала: {e}")