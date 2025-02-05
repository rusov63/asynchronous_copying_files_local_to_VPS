import os
from Local.globals import counter, local_user_paths
from Local.file_utils import count_files_in_directory


# globals import counter, local_user_paths СЧЕТЧИКИ И хранение путей!

async def check_path_file_folder(path_local: str) -> bool:
    """
    Проверяет существование пути и добавляет его в список отслеживаемых путей.

    Функция проверяет существование указанного пути и определяет, является ли он файлом или директорией.
    В зависимости от типа пути выполняются следующие действия:
    - Для файла: добавляет путь в список и увеличивает счетчик файлов
    - Для директории: добавляет путь в список, увеличивает счетчик директорий и подсчитывает количество файлов внутри

    Параметры: path_local (str): Путь к файлу или директории для проверки

    Возвращает: None

    Примечания:
        - Для директорий автоматически добавляется завершающий слеш, если его нет
        - Дублирующиеся пути не добавляются повторно
        - Функция выводит информационные сообщения о результатах проверки
    """

    # Проверяем существует ли путь


async def check_path_file_folder(path_local: str) -> bool:
    try:
        if not os.path.exists(path_local):
            print(f'Путь {path_local} не существует.')
            return False

        # Проверяем доступ к директории
        elif not os.access(path_local, os.R_OK):
            print(f"Нет прав доступа к директории: {path_local}")
            return False

        # Проверяем является ли путь ФАЙЛОМ
        elif os.path.isfile(path_local):
            if path_local not in local_user_paths.paths:
                local_user_paths.append(path_local)
                counter.local_file += 1
                print(f'Файл: {path_local.split('/')[-1]} успешно добавлен.')
            else:
                print(f"Файл с указанным путем уже был добавлен ранее.")
                return False

        # Проверяем является ли путь ДИРЕКТОРИЕЙ
        elif '/' != path_local[-1]:  # Если путь не заканчивается слешем
            path_local = path_local + '/'  # Добавляем слеш в конец

            if path_local not in local_user_paths.paths:  # Проверяем существует ли путь в списке global class PATH

                local_user_paths.append(path_local)  # добавляем путь в global class PATH
                counter.local_dir += 1  # Прибавляем счетчик global class Counter

                # подсчитывает количество файлов в указанной директории.
                await count_files_in_directory(path_local)

            elif path_local in local_user_paths.paths:
                print(f"Папка с указанным путем уже была добавлена ранее.")
                return False

        elif '/' == path_local[-1]:  # Если путь заканчивается слешем

            if path_local not in local_user_paths.paths:  # Проверяем существует ли путь в списке PATH

                local_user_paths.append(path_local)  # добавляем путь в global class PATH
                counter.local_dir += 1  # Прибавляем счетчик global class Counter

                # подсчитывает количество файлов в указанной директории.
                await count_files_in_directory(path_local)
            else:
                print(f"Папка с указанным путем уже была добавлена ранее.")
                return False
        else:
            print(f"Путь '{path_local}' существует, но не является файлом или папкой.")
            return False

    except Exception as e:
        print(f"Непредвиденная ошибка: {e}")
        return False