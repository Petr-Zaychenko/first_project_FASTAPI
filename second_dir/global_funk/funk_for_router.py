import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def del_file(path_file):
    try:
        os.remove(path_file)
        logger.info(f"Файл {path_file} успешно удален")
        return True

    except OSError as e:
        logger.error(f"Ошибка при удалении файла {path_file}")
        return False
