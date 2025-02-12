import sys

from Local.check_path import check_path_file_folder
from Local.file_folder_counter import get_counts_folders_and_files


FIRST_MESSAGE = ("""Для копирования укажите абсолютный путь к директории (например, /home/my_papka/) 
или файлу (/home/my_file.txt) локально, начиная с символа \"/\".\n""")

SECOND_MESSAGE = ("""После окончания добавления файлов, укажите - "0".
Для отмены копирования наберите - "exit".\n""")


async def get_local_path_user() -> None:
    """
    Асинхронная функция для получения и обработки путей к локальным файлам и директориям от пользователя.

    Функция запрашивает у пользователя абсолютные пути к файлам и директориям,
    проверяет их корректность и существование. Пользователь может добавлять multiple пути
    до тех пор, пока не введет '0' для завершения ввода или 'exit' для выхода из программы.

    Returns: None

    Raises:
        KeyboardInterrupt: При прерывании программы пользователем (Ctrl+C)
        Exception: При возникновении других ошибок во время выполнения

    Usage:
        await get_local_path_user()

    Notes:
        - Пути должны начинаться с символа '/'
        - Ввод '0' завершает процесс добавления путей
        - Ввод 'exit' завершает программу
        - После завершения ввода выводится статистика добавленных файлов и папок
    """
    print(FIRST_MESSAGE)
    print(SECOND_MESSAGE)

    # Обрабатываем путь до тех пор, пока пользователь не введет "exit" или '0'
    while True:
        try:
            user_input = input("Укажите путь: ").strip()

            if user_input.lower() == "exit":
                print("Завершение программы.")
                sys.exit()

            elif not user_input.strip():
                print("Путь не может быть пустым")
                continue

            elif user_input == '0':
                break  # Возвращаем результат сохраненный в глобальной переменной class Path: local_user_paths

            elif '/' != user_input[0]:
                # Работает быстрее, выполняет только одну операцию
                print("Неверный формат пути. Пример: /home/to/folder/")
                continue

            else:
                # Проверяем результат выполнения check_path_file_folder
                path_exists = await check_path_file_folder(user_input)
                if not path_exists:
                    continue  # Если путь не существует, продолжаем цикл

            # Проверяет существование пути и добавляет его в список отслеживаемых путей.
            await check_path_file_folder(user_input)

        except KeyboardInterrupt:
            print("\nПрерывание пользователем.")
            sys.exit(1)

        except Exception as e:
            print(f"Произошла ошибка: {e}")
            continue

    # выводит количество добавленных файлов и папок, заключительная функция
    await get_counts_folders_and_files()






# /home/rusov/PycharmProjects/asyncio_copying_files_server/
# /home/rusov/PycharmProjects/asyncio_copying_files_server/readme.md
# /home/rusov/PycharmProjects/