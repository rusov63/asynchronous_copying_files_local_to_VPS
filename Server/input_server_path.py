import asyncio
import logging
import re
from typing import Union

import aioconsole
import asyncssh
from config import CANCELLED_MESSAGE, ERROR_MESSAGE, EXCEPTION_MESSAGE
from logs.logger_config import setup_logger

logger = setup_logger(__name__)


FOLDER_PATH: str = '/my_folder'  # Путь по умолчанию
EXIT_COMMAND: str = "exit"


FIRST_MESSAGE: str = (
    f'\nДля копирования укажите путь к папке на сервере (по умолчанию путь {FOLDER_PATH}),\n'
    f'начиная с символа "/" (например, /home/my_papka/).'
)

SECOND_MESSAGE: str = "Для отмены наберите - \"exit\".\n"

INVALID_PATH_MESSAGE: str = (
    "Путь содержит недопустимые символы. "
    "Используйте только английские буквы, подчеркивания и дефисы."
)




async def get_server_path_user() -> Union[str, bool]:
    """
    Асинхронная функция для получения и проверки пути к папке на сервере от пользователя.

    Функция запрашивает у пользователя путь к папке, проверяет его корректность.
    Если пользователь вводит пустую строку, ему предлагается
    выбрать путь по умолчанию. Пользователь может отменить ввод, введя 'exit'.

    Returns:
        str: Корректный путь к папке, введенный пользователем, или путь по умолчанию.
        Bool: В случае ошибки или отмены операции

    Errors:
        asyncssh. Error: При ошибках SSH соединения
        OSError: При системных ошибках
        asyncio. CancelledError: При отмене операции
    """

    print(FIRST_MESSAGE)
    print(SECOND_MESSAGE)

    while True:

        try:
            user_input = await aioconsole.ainput("Введите путь к папке: ")
            user_input = user_input.strip().lower()

            # Завершение программы
            if user_input == EXIT_COMMAND:
                logger.info("Прерывание пользователем.")
                print("Завершение программы.")
                return False

            # Проверяет являеться ли указанный путь допустимым.
            elif not user_input:
                print("\nПуть не может быть пустым")
                user = await aioconsole.ainput("Выбрать путь по умолчанию? (да, нет): ")
                user = user.lower()

                if user in ['да', '']:
                    print(f'Используется путь: {FOLDER_PATH}')
                    return FOLDER_PATH
                else:
                    logger.info('Пользователь не выбрал путь по умолчанию')
                    continue

            # Проверяет через регулярное выражение
            elif is_valid_path(user_input):
                print(f'Путь корректен, введенный путь: {user_input}')
                return user_input
            else:
                print(INVALID_PATH_MESSAGE)
                continue


        except (asyncssh.Error, OSError, AttributeError) as e:
            logger.error(f"Ошибка при работе с папкой: {str(e)}", exc_info=True)
            print(ERROR_MESSAGE.format(e=e))
            return False

        except asyncio.CancelledError:
            logger.warning(f"Операция была отменена пользователем", exc_info=True)
            print(CANCELLED_MESSAGE)
            return False

        except Exception as e:
            logger.error(f"Неожиданная ошибка: {str(e)}", exc_info=True)
            print(EXCEPTION_MESSAGE.format(e=e))
            return False


def is_valid_path(path: str) -> bool:
    """
    Проверяет, является ли указанный путь допустимым.

    Путь считается допустимым, если он соответствует определенному шаблону,
    начинается с '/' и содержит только разрешенные символы. Также проверяется,
    что длина пути находится в пределах от 3 до 30 символов.

    :arg
        path (str): Путь, который необходимо проверить.

    :return
        bool: True, если путь корректен, иначе False.

    :exception
        Если путь недопустим, выводится сообщение об ошибке с указанием причины.
        Is_valid_path("/home/user/documents")  # Вернёт True
        is_valid_path("home/user/documentы")  # Вернёт False
    """
    pattern = r'^/[a-zA-Z0-9_-]+(?:/[a-zA-Z0-9_-]+)*/?$'

    if '/' not in path[0]:
        print(f"Неверный формат пути. Пример: {FOLDER_PATH}")
        return False

    if 30 <= len(path) <= 2:
        print(f"Путь слишком короткий. Пример: {FOLDER_PATH}")
        return False

    if not re.match(pattern, path):
        print("Путь содержит недопустимые символы")
        return False

    return True

