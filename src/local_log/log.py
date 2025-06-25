from pathlib import Path
import logging
from datetime import date


class Log:
    def __init__(self, log_to_console=False):
        self.log_to_console = log_to_console
        self.logger = logging.getLogger("CrewLogger")
        self.logger.setLevel(logging.DEBUG)

        self.log_functions = {
            'info': self.logger.info,
            'warning': self.logger.warning,
            'error': self.logger.error,
            'critical': self.logger.critical,
            'debug': self.logger.debug
        }

        self._initialize_logging()

    def _initialize_logging(self):
        log_dir = Path("src/storage/logs")
        log_dir.mkdir(parents=True, exist_ok=True)

        log_file = log_dir / f"{date.today():%d-%m-%Y}.log"

        file_handler = logging.FileHandler(log_file, mode='a')
        file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        self.logger.addHandler(file_handler)

        if self.log_to_console:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(logging.Formatter('%(levelname)s - %(message)s'))
            self.logger.addHandler(console_handler)


    def log(self, level, msg):
        level = level.lower()
        log_func = self.log_functions.get(level)
        if log_func:
            log_func(msg)
        else:
            self.logger.error(f"Invalid log level '{level}' used: {msg}")


# Initialize logger instance (and make it available globally)
logger = Log(log_to_console=True)
