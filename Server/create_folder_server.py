import sys

import asyncssh

from config import HOST


async def create_folder_on_server(ssh: asyncssh.SSHClientConnection, path_folder: str) -> None:
    """
    Создает папку на удаленном сервере через SSH-соединение.

    Эта корутина проверяет существование директории на сервере и создает её,
    если она не существует. Если директория уже существует, предлагает пользователю
    удалить её.

    Параметры:
    - ssh (asyncssh.SSHClientConnection): Объект SSH-соединения.
    - path_folder (str): Путь к папке, которую нужно создать на сервере.

    Возвращает: None

    Исключения:
    - KeyboardInterrupt: Если пользователь прерывает выполнение.
    - OSError: Ошибка работы с папкой.
    - Exception: Любая другая непредвиденная ошибка.
    """
    try:
        # Проверяем, существует ли директория на сервере
        command_check = f"if [ -d {path_folder} ]; then echo 'exists'; else echo 'not exists'; fi"
        result = await ssh.run(command_check)

        # Если директория на сервере существует:
        if result.stdout.strip() == 'exists':
            print(f"Директория {path_folder} уже существует.")
            await handle_existing_directory(ssh, path_folder)

        # Если директория на сервере не существует:
        elif result.stdout.strip() == 'not exists':
            print(f'Создаем "{path_folder[1:]}" на сервере {HOST}')
            await create_directory(ssh, path_folder)

        else:
            print(f"Неизвестный результат проверки директории: {result.stdout.strip()}")

    except KeyboardInterrupt:
        print("\nПрерывание пользователем.")
        sys.exit(1)

    except OSError:
        print("Ошибка при работе с папкой")
        sys.exit(1)

    except Exception as e:
        print(f"Произошла ошибка: {e}")
        sys.exit(1)



async def handle_existing_directory(ssh: asyncssh.SSHClientConnection, path_folder: str) -> None:
    """
    Обрабатывает существующую директорию на сервере.

    Предлагает пользователю удалить существующую директорию. Если
    пользователь соглашается, удаляет её и создает новую.

    Параметры:
    - ssh (asyncssh.SSHClientConnection): Объект SSH-соединения.
    - path_folder (str): Путь к существующей папке на сервере.

    Возвращает: None
    """
    # Список файлов в директории
    files = f'find "{path_folder}" -type f | wc -l'

    # Получаем количество файлов из результата
    command_files = await ssh.run(files, check=True)
    files_count = command_files.stdout.strip()
    print(f'В этой директории {files_count} файлов')

    # Запрашиваем у пользователя, хочет ли он удалить директорию
    while True:
        user = input('Удалить директорию? (y/n):').strip().lower()

        if user in ('y', 'yes', 'да', ''):
            command_delete = f"rm -rf {path_folder}"
            result = await ssh.run(command_delete, check=True)

            if result.exit_status == 0:
                print(f"Директория {path_folder} успешно удалена")
                break

            else:
                print(f"Ошибка при удалении директории: {result.stderr.strip()}")
                break

        elif user in ('n', 'no', 'нет'):
            print("Операция отменена")
            return None
        else:
            print("Неизвестный ввод, повторите")
            continue

    # После удаления директории создаем папку
    await create_folder_on_server(ssh, path_folder)



async def create_directory(ssh: asyncssh.SSHClientConnection, path_folder: str) -> None:
    """
    Создает новую папку на удаленном сервере.

    Параметры:
    - ssh (asyncssh.SSHClientConnection): Объект SSH-соединения.
    - path_folder (str): Путь к новой папке, которую нужно создать на сервере.

    Возвращает: None
    """
    command_create = f"mkdir -p {path_folder}"
    result = await ssh.run(command_create)

    if result.exit_status == 0:
        print(f'Папка "{path_folder[1:]}" успешно создана')
    else:
        print(f"Ошибка при создании папки: {result.stderr.strip()}")



# вывод результатов выполнения команды
# print("Результат команды проверки директории:")
# print(f"stdout: {result.stdout.strip()}")
# print(f"stderr: {result.stderr.strip()}")
# print(f"exit_status: {result.exit_status}")
