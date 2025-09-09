import logging
import sys

def setup_logger(name="SkanerP2P", log_file=None, level=logging.INFO):
    """Налаштовує логгер з кольорами і можливістю писати у файл"""
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(message)s",
        datefmt="%H:%M:%S"
    )

    # головний логер
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # консольний хендлер
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # файл (опціонально)
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger

# створюємо глобальний логер
log = setup_logger()
