import logging
from logging import FileHandler


class LOGS:
    def __init__(self, file_scripts, log_message, log_level):
        self.logger = logging.getLogger(file_scripts)  # Создание лога как объект класса Logger
        self.message = log_message  # Сообщение лога
        self.format_message = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(name)s - %(message)s')  # Задается формат записи лога

        if log_level == 'WARNING':
            self.fh = logging.FileHandler('log_file.log', encoding="Windows-1251")
            self.fh.setLevel(logging.WARNING)
            self.fh.setFormatter(self.format_message)
            self.logger.warning(self.message)
            self.logger.addHandler(self.fh)

        if log_level == 'INFO':
            self.fh = logging.FileHandler('log_file.log', encoding="Windows-1251")
            self.logger.setLevel(logging.INFO)
            self.fh.setFormatter(self.format_message)
            self.logger.addHandler(self.fh)
            self.logger.info(self.message)
        if log_level == 'ERROR':
            self.fh = logging.FileHandler('log_file.log', encoding="Windows-1251")
            self.logger.setLevel(logging.INFO)
            self.fh.setFormatter(self.format_message)
            self.logger.addHandler(self.fh)
            self.logger.error(self.message)

    def print_message(self):
        print(self.logger.info(self.message))