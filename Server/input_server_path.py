import asyncio
import logging
import sys
import re

import aioconsole
import asyncssh


# Настройка логирования
logging.basicConfig(
    filename='app_info.log',  # Имя файла для записи логов
    filemode='a',              # Режим записи: 'a' для добавления
    level=logging.INFO,        # Уровень логирования
    format='%(asctime)s - %(levelname)s - %(message)s - %(name)s - %(filename)s:%(lineno)d'
)

FOLDER_PATH = '/my_folder'  # Путь по умолчанию
EXIT_COMMAND = "exit"


FIRST_MESSAGE = (
    f'\nДля копирования укажите путь к папке на сервере (по умолчанию путь {FOLDER_PATH}),\n'
    f'начиная с символа "/" (например, /home/my_papka/).'
)

SECOND_MESSAGE = (
    "Для отмены копирования наберите - \"exit\".\n"
)


async def get_server_path_user() -> str:
    """
    Асинхронная функция для получения и проверки пути к папке на сервере от пользователя.

    Функция запрашивает у пользователя путь к папке, проверяет его корректность.
    Если пользователь вводит пустую строку, ему предлагается
    выбрать путь по умолчанию. Пользователь может отменить ввод, введя 'exit'.

    Returns:
        str: Корректный путь к папке, введенный пользователем, или путь по умолчанию.

    Exit:
        sys.exit(): При вводе 'exit' происходит завершения программы.

    Raises:
        KeyboardInterrupt: При прерывании программы пользователем (Ctrl+C).
        OSError: При ошибках, связанных с доступом к файловой системе.
        CancelledError: При прерывании операции внешними факторами или системой.

    Usage:
        path = await get_server_path_user()
    """

    print(FIRST_MESSAGE)
    print(SECOND_MESSAGE)

    while True:

        try:
            user_input = await aioconsole.ainput("Введите путь к папке: ")
            user_input = user_input.strip().lower()

            # Завершение программы
            if user_input == EXIT_COMMAND:
                logging.info("Прерывание пользователем.")
                print("Завершение программы.")
                sys.exit()

            # Проверяем путь на пустую строку
            elif not user_input:
                print("\nПуть не может быть пустым")
                user = await aioconsole.ainput("Выбрать путь по умолчанию? (да, нет): ")
                user = user.lower()
                if user in ['да', '']:
                    print(f'Используется путь: {FOLDER_PATH}')
                    return FOLDER_PATH
                else:
                    continue

            # Проверяем начало пути с '/' или длину ввода не меньше или равно 3
            elif '/' not in user_input[0] or len(user_input) <= 2:
                print(f"Неверный формат пути. Пример: {FOLDER_PATH}")
                continue

            elif is_valid_path(user_input):
                print(f'Путь корректен, введенный путь: {user_input}')
                return user_input
            else:
                print("Путь содержит недопустимые символы. "
                      "Используйте только английские буквы, подчеркивания и дефисы.")
                continue

        except KeyboardInterrupt:
            print("\nПрерывание пользователем.")
            sys.exit(1)

        except (asyncssh.Error, OSError) as e:
            print("\nОшибка при работе с папкой")
            continue

        except asyncio.CancelledError:
            print("\nОперация была отменена.")
            sys.exit(1)

        except Exception as e:
            print(f"\nПроизошла ошибка: {e}")
            continue



def is_valid_path(path: str) -> bool:
    """
    Проверяет, является ли указанный путь допустимым.

    Функция использует регулярное выражение для проверки того,
    что путь состоит только из разрешённых символов: английских букв,
    подчеркиваний, дефисов, цифр, а также флеш.

    Args:
        path (str): Путь, который необходимо проверить.

    Returns:
        bool: True, если путь корректен, иначе False.

    Example:
        is_valid_path("/home/user/documents")  # Вернёт True
        is_valid_path("home/user/documents")    # Вернёт False
    """
    pattern = r'^[a-zA-Z0-9/_-]+$'
    return bool(re.match(pattern, path))