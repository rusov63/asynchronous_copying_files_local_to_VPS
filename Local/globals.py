
class Counter:
    """
    Класс для подсчета количества добавленных файлов и папок.

    Attributes:
    local_file (int): Счетчик количества добавленных файлов
    local_dir (int): Счетчик количества добавленных папок
    """

    def __init__(self) -> None:
        self.local_file: int = 0  # Счетчик кол-во добавленных файлов
        self.local_dir: int = 0   # Счетчик кол-во добавленных папок


counter = Counter()


class Path:
    """
    Класс для хранения и управления списком путей, добавленных пользователем.

    Attributes:
    paths (List[str]): Список путей, добавленных пользователем

    Methods:
    append(path: str): Добавляет новый путь в список
     __contains__(path: str): Проверяет наличие пути в списке
    """

    def __init__(self) -> None:
        self.paths = []  # Список добавленных путей от пользователя

    def append(self, path: str) -> None:
        """
        Добавляет новый путь в список paths.
        Args: path (str): Путь к файлу или директории для добавления
        """
        self.paths.append(path)

    def __contains__(self, path: str) -> bool:
        """
        Проверяет наличие пути в списке paths.
        Args: path (str): Путь для проверки
        Returns: bool: True если путь найден в списке, False в противном случае
        """
        return path in self.paths


local_user_paths = Path()  # Создаем экземпляр класса
