import logging

class CustomFormatter(logging.Formatter):

    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "%(asctime)s %(levelname)s %(message)s"

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: grey + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

class LogFactory:
    logger = None

    @staticmethod
    def Initialize(filePath):
        # Уровни логирования:
        # Debug - логируется только тогда, когда нажимаешь на жучка
        # Info - обычная информация
        # Warning - предупруждение
        # Error - ошибка (в основном в try/except)
        # Critical - критическая ошибка

        # logging.basicConfig(level=logging.INFO, filename="bot.log",filemode="w",
        #                    format="%(asctime)s %(levelname)s %(message)s")

        # Создаем объект логгера
        LogFactory.logger = logging.getLogger()

        # Устанавливаем уровень логирования
        LogFactory.logger.setLevel(logging.INFO)

        # Создаем обработчик для записи в файл
        file_handler = logging.FileHandler(filePath)
        file_handler.setLevel(logging.INFO)

        # Создаем обработчик для вывода в консоль
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        # Создаем форматтер для сообщений логгера
        formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

        # Добавляем форматтер к обоим обработчикам
        file_handler.setFormatter(formatter)

        consoleFormater = CustomFormatter()
        consoleFormater.datefmt = "%Y-%m-%d %H:%M:%S"
        console_handler.setFormatter(consoleFormater)

        # Добавляем оба обработчика к логгеру
        LogFactory.logger.addHandler(file_handler)
        LogFactory.logger.addHandler(console_handler)


