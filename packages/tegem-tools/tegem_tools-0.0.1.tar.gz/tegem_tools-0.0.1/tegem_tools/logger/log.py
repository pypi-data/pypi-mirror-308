import logging
from logging.handlers import RotatingFileHandler


class BasicLog:
    def __init__(self, log_file_path: str, stream: bool = True) -> None:
        self.log_file_path = log_file_path
        self.stream = stream

    def log_config(
            self, 
            name:str, 
            loglevel= logging.DEBUG
            ) -> logging.Logger:
        """
        Configuration of the logger.

        Args:
            name (str): The name of the logger.
            stream (bool, optional): Whether to log to a stream or a file. Defaults to True.
            loglevel (int, optional): The level of the messages to log. Defaults to logging.DEBUG.

        Returns:
            logging.Logger: The configured logger.
        """
        logger_name = (name)
        logger = logging.getLogger(logger_name)
        logger.setLevel(loglevel)
        formater = logging.Formatter('%(asctime)s - %(filename)s - %(funcName)s - %(levelname)s - %(message)s')
        conf = {
            True: self.stream_conf(formater),
            False: self.file_conf(formater)
        }
        #добавление хендлера
        logger.addHandler(conf[self.stream])
        return logger

    def stream_conf(self, formater):
        #настройки для консоли
        stream = logging.StreamHandler()
        stream.setFormatter(formater)
        return stream
    
    def file_conf(self, formater):
        #настройки для лог-файла
        log_file = RotatingFileHandler(self.log_file_path, maxBytes=100000, backupCount=3)
        log_file.setFormatter(formater)
        return log_file
