import os
import unittest

from dotenv import load_dotenv


class TestEnvironmentVariables(unittest.TestCase):
    """
    Тестовый класс для проверки загрузки переменных окружения.
    """

    @classmethod
    def setUpClass(cls):
        """
        Настраивает тестовое окружение, загружая переменные окружения из файла .env.

        Этот метод вызывается один раз перед запуском любых тестов в классе.
        Он использует python-dotenv для загрузки переменных окружения,
        перезаписывая любые существующие.
        """
        load_dotenv(override=True)

    def test_environment_variables(self):
        """
        Проверяет, что все необходимые переменные окружения загружены и не равны None.

        Этот метод проверяет наличие следующих переменных окружения:
        - HOST
        - USERNAME
        - PASSWORD
        - ENABLE_PASSWORD
        - ENCRYPTION_ALGS

        Для каждой переменной утверждается, что значение не равно None,
        что указывает на успешную загрузку переменной из файла .env.

        Вызывает:
            AssertionError: Если любая из требуемых переменных окружения равна None.
        """
        self.assertIsNotNone(os.getenv("HOST"), "HOST переменная окружения не загружена")
        self.assertIsNotNone(os.getenv("USERNAME"), "USERNAME переменная окружения не загружена")
        self.assertIsNotNone(os.getenv("PASSWORD"), "PASSWORD переменная окружения не загружена")
        self.assertIsNotNone(os.getenv("ENABLE_PASSWORD"), "ENABLE_PASSWORD переменная окружения не загружена")
        self.assertIsNotNone(os.getenv("ENCRYPTION_ALGS"), "ENCRYPTION_ALGS переменная окружения не загружена")

