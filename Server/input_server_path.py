import sys
import re

FOLDER_PATH = '/usr/my_files/'  # Путь по умолчанию

FIRST_MESSAGE = f'\nУкажите путь к папке на сервере (по умолчанию {FOLDER_PATH}), начиная с символа "/".'

SECOND_MESSAGE = f'Для отмены копирования наберите - "exit".\n'


async def get_server_path_user() -> str:
    """
    Асинхронная функция для получения и проверки пути к папке на сервере от пользователя.

    Функция запрашивает у пользователя путь к папке, проверяет его корректность и
    существование. Если пользователь вводит пустую строку, ему предлагается
    выбрать путь по умолчанию. Пользователь может отменить ввод, введя 'exit'.

    Returns:
        str: Корректный путь к папке, введенный пользователем, или путь по умолчанию.

    Exit:
        sys.exit(): При вводе 'exit' происходит завершения программы.

    Raises:
        KeyboardInterrupt: При прерывании программы пользователем (Ctrl+C).
        OSError: При ошибках, связанных с доступом к файловой системе.

    Usage:
        path = await get_server_path_user()
    """

    print(FIRST_MESSAGE)
    print(SECOND_MESSAGE)

    while True:

        try:
            user_input = input("Укажите путь: ").strip()

            # Завершение программы
            if user_input.lower() == "exit":
                print("Завершение программы.")
                sys.exit()

            # Проверяем путь на пустую строку
            elif not user_input.strip():
                print("Путь не может быть пустым\nВыбрать путь по умолчанию? (да, нет)")
                user = input().lower()
                if user == 'да' or user == '':
                    print(f'Используется путь: {FOLDER_PATH}')
                    return FOLDER_PATH
                else:
                    continue

            # Проверяем начало пути с '/' или длину ввода не меньше или равно 3
            elif '/' not in user_input[0] or len(user_input) <= 3:
                print(f"Неверный формат пути. Пример: {FOLDER_PATH}")
                continue

            elif is_valid_path(user_input):
                print(f'Путь корректен, введенный путь: {user_input}')
                return user_input
            else:
                print("Путь содержит недопустимые символы. Используйте только английские буквы, подчеркивания и дефисы.")
                continue

        except KeyboardInterrupt:
            print("\nПрерывание пользователем.")
            sys.exit(1)

        except OSError:
            print("Ошибка при работе с папкой")
            continue

        except Exception as e:
            print(f"Произошла ошибка: {e}")
            continue



def is_valid_path(path: str) -> bool:
    """
    Проверяет, является ли указанный путь допустимым.

    Функция использует регулярное выражение для проверки того,
    что путь состоит только из разрешённых символов: английских букв,
    подчеркиваний и дефисов, а также слешей.

    Args:
        path (str): Путь, который необходимо проверить.

    Returns:
        bool: True, если путь корректен, иначе False.

    Example:
        is_valid_path("/home/user/documents")  # Вернёт True
        is_valid_path("home/user/documents")    # Вернёт False
    """
    pattern = r'^[a-zA-Z/_-]+$'
    return bool(re.match(pattern, path))

