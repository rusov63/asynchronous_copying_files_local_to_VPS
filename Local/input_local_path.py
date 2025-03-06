import sys

import aioconsole

from Local.check_path import check_path_file_folder
from Local.file_folder_counter import get_counts_folders_and_files


FIRST_MESSAGE = (
    "Для копирования укажите абсолютный путь к директории (например, /home/my_papka/)\n"
    "или файлу (/home/my_file.txt) локально, начиная с символа \"/\".\n"
)

SECOND_MESSAGE = (
    "После окончания добавления файлов, укажите - \"0\".\n"
    "Для отмены копирования наберите - \"exit\".\n"
)


async def get_user_input_path() -> None:
    """
    Асинхронная функция для получения и обработки путей к локальным файлам и директориям от пользователя.

    Функция запрашивает у пользователя абсолютные пути к файлам и директориям,
    проверяет их корректность и существование. Пользователь может добавлять multiple пути
    до тех пор, пока не введет '0' для завершения ввода или 'exit' для выхода из программы.

    Returns: None

    Ошибки:
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
            user_input = await aioconsole.ainput("Введите путь к файлу/папке: ").strip()

            if user_input.lower() == "exit":
                print("Завершение программы.")
                sys.exit()

            elif not user_input:
                print("Ошибка: Путь не может быть пустым. Пожалуйста, введите корректный путь.")
                continue

            elif user_input == '0':
                break  # Возвращаем результат сохраненный в глобальной переменной class Path: local_user_paths

            elif user_input[0] != '/':
                print("Ошибка: Неверный формат пути. Путь должен начинаться с символа '/'.")
                continue

            else:
                # Проверяет существование пути
                path_exists = await check_path_file_folder(user_input)
                if not path_exists:
                    continue  # Если путь не существует, продолжаем цикл

        except KeyboardInterrupt:
            print("\nПрерывание пользователем.")
            sys.exit(1)

        except Exception as e:
            print(f"Произошла ошибка: {e}")
            continue

    # выводит количество добавленных файлов и папок, заключительная корутина
    await get_counts_folders_and_files()