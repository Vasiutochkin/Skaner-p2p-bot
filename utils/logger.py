import logging
from logging.handlers import RotatingFileHandler
import sys

# ANSI-коди для кольорів
COLORS = {
    "DEBUG": "\033[90m",    # сірий
    "INFO": "\033[92m",     # зелений
    "WARNING": "\033[93m",  # жовтий
    "ERROR": "\033[91m",    # червоний
    "RESET": "\033[0m"
}

class ColorFormatter(logging.Formatter):
    def format(self, record):
        log_color = COLORS.get(record.levelname, COLORS["RESET"])
        message = super().format(record)
        return f"{log_color}{message}{COLORS['RESET']}"

def setup_logger(name="SkanerP2P", log_file="bot.log", level=logging.INFO):
    """Налаштовує логгер з кольорами, ротацією і можливістю писати у файл"""
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(message)s",
        datefmt="%H:%M:%S"
    )
    color_formatter = ColorFormatter(
        "%(asctime)s | %(levelname)-8s | %(message)s",
        datefmt="%H:%M:%S"
    )

    logger = logging.getLogger(name)
    logger.setLevel(level)

    # щоб не дублювати хендлери при повторному виклику
    if not logger.handlers:
        # консольний хендлер з кольорами
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(color_formatter)
        logger.addHandler(console_handler)

        # файл з ротацією (макс 5MB, до 3 файлів)
        if log_file:
            file_handler = RotatingFileHandler(log_file, maxBytes=5*1024*1024, backupCount=3)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

    return logger

# глобальний логер
log = setup_logger()
