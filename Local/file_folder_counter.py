import sys
from Local.globals import counter, local_user_paths


async def get_counts_folders_and_files() -> None:
    """
    Асинхронно выводит количество добавленных файлов и папок.

    Функция проверяет счетчики добавленных файлов и папок и выводит соответствующую информацию.
    В случае отсутствия добавленных элементов или ошибки, программа завершается.

    Returns:
        None: Функция только выводит информацию на экран.

    Raises:
        SystemExit: Если не было добавлено ни одного элемента или произошла ошибка.

    Examples:
        async def example():
        ...     counter.local_file = 5
        ...     counter.local_dir = 2
        ...     await get_counts_folders_and_files()
        Добавлено файлов: 5, папок: 2

        async def example_empty():
        ...     counter.local_file = 0
        ...     counter.local_dir = 0
        ...     await get_counts_folders_and_files()
        В результате операции не было добавлено ни одной папки или файла.
        Операция завершена.
    """

    if counter.local_file > 0 or counter.local_dir > 0:
        print(f'Добавлено файлов: {counter.local_file}, папок: {counter.local_dir}')
        print(local_user_paths.paths)
    elif counter.local_file == 0 and counter.local_dir == 0:
        print("""В результате операции не было добавлено ни одной папки или файла.
                 Операция завершена.""")
        print(local_user_paths.paths)
        sys.exit()
    else:
        print("Не указано количество добавленных папок и файлов.")
        sys.exit()

