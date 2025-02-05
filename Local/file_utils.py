import os


async def count_files_in_directory(directory: str) -> None:
    """
    Асинхронно подсчитывает количество файлов в указанной директории.

    Args:
        directory (str): Путь к директории, в которой нужно подсчитать файлы.
    Returns:
        None: Функция выводит количество файлов в директории и сообщение о добавлении папки.
    Example:
        await count_files_in_directory("/path/to/directory")
        Папка "directory" успешно добавлена.
        В папке 5 файлов, 5 папки/папок
    """
    try:
        if not os.access(directory, os.R_OK):
            raise PermissionError(f"Нет прав доступа к директории: {directory}")

        items = os.listdir(directory)
        files = [item for item in items if os.path.isfile(os.path.join(directory, item))]
        folder = [item for item in items if os.path.isdir(os.path.join(directory, item))]

        print(f'Папка "{directory.split("/")[-2]}" успешно добавлена.')
        files_output = f'В папке {len(files)} файл' if len(files) == 1 else f'В папке {len(files)} файла/ов'
        folder_output = f'{len(folder)} папкa' if len(folder) == 1 else f'{len(folder)} папки/папок'

        print(f'{files_output}, {folder_output}')

    except Exception as e:
        print(f"Ошибка при подсчете файлов: {e}")