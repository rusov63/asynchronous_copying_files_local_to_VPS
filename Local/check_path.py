import asyncio
import os
from Local.globals import counter, stored_user_paths
from Local.file_utils import print_count_files_and_directories


# globals import counter, local_user_paths СЧЕТЧИКИ И хранение путей!

async def check_path_file_folder(path_local: str) -> bool:
    """
    Проверяет существование пути и добавляет его в список отслеживаемых путей.

    Функция проверяет существование указанного пути и определяет, является ли он файлом или директорией.
    В зависимости от типа пути выполняются следующие действия:
    - Для файла: добавляет путь в список и увеличивает счетчик файлов
    - Для директории: добавляет путь в список, увеличивает счетчик директорий и подсчитывает количество
    файлов внутри

    Параметры: path_local (str): Путь к файлу или директории для проверки

    Возвращает: None
    Примечания:
        - Дублирующиеся пути не добавляются повторно
        - Функция выводит информационные сообщения о результатах проверки
    """
    try:
        if not os.path.exists(path_local):
            print(f'Путь {path_local} не существует.')
            return False

        # Проверяем доступ к директории
        elif not os.access(path_local, os.R_OK):
            print(f"Нет прав доступа к директории: {path_local}")
            return False

        # Проверяем является ли путь ФАЙЛОМ
        elif await is_file(path_local):
            if path_local not in stored_user_paths.paths:
                stored_user_paths.append(path_local)
                counter.local_file += 1
                print(f'Файл: "{path_local.split('/')[-1]}" успешно добавлен.')
                print('*' * 40)
            else:
                print(f"Файл с указанным путем уже существует в списке.")
                print('*' * 50)
                return False

        # Проверяем является ли путь ДИРЕКТОРИЕЙ
        elif await is_directory(path_local):
            if path_local[-1] == '/':
                # Проверяем существует ли путь в списке global class PATH
                if path_local not in stored_user_paths.paths and path_local.rstrip('/') not in stored_user_paths.paths:
                    stored_user_paths.append(path_local)  # добавляем путь в global class PATH
                    counter.local_dir += 1  # Прибавляем счетчик global class Counter
                    # подсчитывает количество файлов в указанной директории.
                    await print_count_files_and_directories(path_local)
                else:
                    print(f"Папка с указанным путем уже существует в списке.")
                    print('*' * 50)
                    return False

            elif path_local[-1] != '/':
                # Проверяем существует ли путь в списке global class PATH
                if path_local + '/' not in stored_user_paths.paths and path_local not in stored_user_paths.paths:
                    stored_user_paths.append(path_local)
                    counter.local_dir += 1  # Прибавляем счетчик global class Counter
                    # подсчитывает количество файлов в указанной директории.
                    await print_count_files_and_directories(path_local)
                else:
                    print(f"Папка с указанным путем уже существует в списке.")
                    print('*' * 50)
                    return False

        else:
            print(f"Путь '{path_local}' существует, но не является файлом или папкой.")
            return False

    except Exception as e:
        print(f"Непредвиденная ошибка: {e}")
        return False


async def is_directory(path_local: str) -> bool:
    """
    Проверяет, является ли указанный путь директорией.

    Эта асинхронная функция использует 'os.path.isdir' для проверки,
    является ли путь 'path_local' директорией. 'os.path.isdir'
    вызывается в отдельном потоке с помощью 'asyncio.to_thread',
    что позволяет избежать блокировки основного цикла событий.

    Параметры:
    path_local (str): Путь к проверяемой директории.
    Возвращает:
    bool: True, если путь является директорией, иначе False.
    """
    return await asyncio.to_thread(os.path.isdir, path_local)


async def is_file(path_local: str) -> bool:
    """
    Проверяет, является ли указанный путь файлом.

    Эта асинхронная функция использует 'os.path.isfile' для проверки,
    является ли путь `path_local` файлом. 'os.path.isfile'
    вызывается в отдельном потоке с помощью 'asyncio.to_thread',
    что позволяет избежать блокировки основного цикла событий.

    Параметры:
    path_local (str): Путь к проверяемому файлу.
    Возвращает:
    bool: True, если путь является файлом, иначе False.
    """
    return await asyncio.to_thread(os.path.isfile, path_local)