import asyncio
import sys

import asyncssh
from config import HOST, USERNAME, PASSWORD, ENCRYPTION_ALGS
from Server.create_folder_server import create_folder_on_server
from copy_file import get_file_transfer_paths


async def connect_to_server(remote_path: str) -> None:
    """
    Устанавливает SSH-подключение к удаленному серверу и создает папку.

    Эта корутина пытается подключиться к удаленному серверу, используя
    учетные данные и настройки, указанные в глобальных переменных. Если подключение
    успешно, она вызывает функцию create_folder_on_server для создания
    папки на удаленном сервере. В случае временных сбоев, выполняет повторные
    попытки подключения с экспоненциальной задержкой.

    Параметры:
    - path_folder (str | None): Путь к папке, которую нужно создать на сервере.

    Используемые глобальные переменные:
    - HOST: имя хоста или IP-адрес удаленного сервера.
    - USERNAME: имя пользователя для аутентификации SSH.
    - PASSWORD: пароль для аутентификации SSH.
    - ENCRYPTION_ALGS: алгоритмы шифрования, используемые для подключения SSH.

    Исключения:
    - asyncssh.misc.PermissionDenied: если предоставленные учетные данные недействительны или недостаточны.
    - asyncssh.Error, OSError: если возникла ошибка, связанная c ошибкой подключения/выполнения команды.

    Возвращает: None
    """

    max_retries = 5  # Максимальное количество попыток
    delay = 2  # Начальная задержка в секундах

    # Повторяем попытки подключения с экспоненциальной задержкой
    while max_retries > 0:
        print(f"\nПодключение к {HOST}")

        try:
            # Устанавливаем SSH-подключение через контекстный менеджер к удаленному серверу
            async with asyncssh.connect(
                    host=HOST,
                    username=USERNAME,
                    password=PASSWORD,
                    encryption_algs=ENCRYPTION_ALGS
            ) as ssh:
                print(f"Успешное подключение к {HOST}")

                # 4. Создаем папку для копирования файлов
                result = await create_folder_on_server(ssh, remote_path)
                if not result:
                    return False

                # 5.
                await get_file_transfer_paths(ssh, remote_path)  # передаем ssh, удаленный путь


        except asyncssh.misc.PermissionDenied:
            print("Нет прав для подключения к серверу")
            sys.exit(1)  # сразу завершаем программу

        except asyncssh.ConnectionLost:
            print("Соединение было потеряно")

        except asyncssh.ChannelOpenError as e:
            print(f"Ошибка открытия канала: {e}")

        except (asyncssh.Error, OSError) as e:
            print(f'Ошибка подключения/выполнения команды: {e}')
            max_retries -= 1
            if max_retries > 0:
                print(f'Повторная попытка через {delay} секунд')
                await asyncio.sleep(delay)
                delay *= 2  # Экспоненциальная задержка
            else:
                print("Максимальное количество попыток исчерпано.")
                # logging.error(f'Ошибка подключения/выполнения команды: {e}')


    # попытки исчерпаны и подключение не удалось
    sys.exit(1)