import sys
from Local.globals import counter, stored_user_paths


async def get_counts_folders_and_files() -> None:
    """
    Асинхронно выводит количество добавленных файлов и папок из глобальной переменной,
    а также список добавленных путей. Функция проверяет счетчики добавленных файлов и папок.
    Если есть добавленные элементы, выводит их количество и отсортированный список путей.
    Если добавленных элементов нет, завершает выполнение программы с соответствующим сообщением.

    Возвращает:
        None: Функция только выводит информацию на экран.
    Исключения:
        SystemExit: Если не было добавлено ни одного элемента или произошла ошибка.
    Примеры:
        async def example():
            counter.local_file = 5
            counter.local_dir = 2
            stored_user_paths.paths = ['/path/to/file1', '/path/to/dir1']
            await get_counts_folders_and_files()
        Вывод:
        Добавлено файлов: 5, папок: 2
        1: /path/to/dir1
        2: /path/to/file1

        async def example_empty():
            counter.local_file = 0
            counter.local_dir = 0
            stored_user_paths.paths = []
            await get_counts_folders_and_files()
        Вывод:
        В результате операции не было добавлено ни одной папки или файла.
        Операция завершена.
    """
    if counter.local_file > 0 or counter.local_dir > 0:
        print(f'Добавлено файлов: {counter.local_file}, папок: {counter.local_dir}')

        # Выводим отсортированный список добавленных папок и файлов
        stored_user_paths.paths.sort()
        print(*[f'{i + 1}: {stored_user_paths.paths[i]}' for i in range(len(stored_user_paths.paths))], sep='\n')

    elif counter.local_file == 0 and counter.local_dir == 0:
        print("""В результате операции не было добавлено ни одной папки или файла.
                 Операция завершена.""")
        #print(stored_user_paths.paths)
        sys.exit()
    else:
        print("Не указано количество добавленных папок и файлов.")
        sys.exit()