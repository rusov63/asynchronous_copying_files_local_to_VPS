import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

# Создаем директорию для логов если её нет
log_dir = Path('logs')
log_dir.mkdir(exist_ok=True)

# Путь к файлу лога
log_file = log_dir / 'app_info.log'

def setup_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        '\n%(asctime)s - %(levelname)s - %(message)s - %(name)s - %(filename)s:%(lineno)d'
    )

    try:
        # Создаем handler для записи в файл с ротацией
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=1024*1024,
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    except Exception as e:
        print(f"Ошибка при создании файла лога: {e}")

    # Добавляем вывод в консоль
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger
