import os

async def print_count_files_and_directories(directory: str) -> None:
    """
    Асинхронно подсчитывает количество файлов в указанной директории.
    Параметры:
        directory (str): Путь к директории, в которой нужно подсчитать количество файлов или папок.
    Returns:
        None: Функция выводит количество файлов в директории и сообщение о добавлении папки.
    Пример:
        await print_count_files_and_directories("/path/to/directory")
        Папка "directory" успешно добавлена.
        В папке 5 файлов, 5 папки/папок
    """
    try:
        if directory[-1] == '/':
            print(f'Папка "{directory.split("/")[-2]}" успешно добавлена.')
        else:
            print(f'Папка "{directory.split("/")[-1]}" успешно добавлена.')

        # Получаем список всех элементов в директории
        items = os.listdir(directory)
        files = [item for item in items if os.path.isfile(os.path.join(directory, item))]
        files_output = f'В папке {len(files)} файл' if len(files) == 1 else f'В папке {len(files)} файла/ов'

        # Получаем список директорий
        folder = [item for item in items if os.path.isdir(os.path.join(directory, item))]
        folder_output = f'{len(folder)} папкa' if len(folder) == 1 else f'{len(folder)} папки/папок'

        print(f'{files_output}, {folder_output}')
        print('*' * 40)

    except Exception as e:
        print(f"Ошибка при подсчете файлов: {e}")