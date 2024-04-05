import os
from datetime import datetime
import logging
from colorama import init, Fore

_filename = os.path.basename(__file__)
# Initialize Colorama
init()


class ColoredFormatter(logging.Formatter):
    LEVEL_COLORS = {
        'DEBUG': Fore.BLUE,
        'INFO': Fore.GREEN,
        'WARNING': Fore.YELLOW,
        'ERROR': Fore.RED,
        'CRITICAL': Fore.LIGHTRED_EX,
    }

    def format(self, record):
        levelname = record.levelname
        if levelname in self.LEVEL_COLORS:
            levelname_color = self.LEVEL_COLORS[levelname] + levelname + Fore.RESET
            record.levelname = levelname_color
        return super().format(record)

    def formatMessage(self, record):
        message = record.getMessage()
        levelname_color = record.levelname
        return f"{levelname_color} - {message}{Fore.RESET}"  # Reset color after the message


logger = logging.getLogger("exceptionhandler")
logger.setLevel(logging.DEBUG)

# File handler
fh = logging.FileHandler("logs/exceptionhandler.log")
fh.setLevel(logging.DEBUG)

# Create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

formatter = ColoredFormatter('%(levelname)s - %(message)s')
ch.setFormatter(formatter)

logger.addHandler(fh)
logger.addHandler(ch)

# get color sceme
colors = ColoredFormatter.LEVEL_COLORS


def print_exception(tag: str, exception: Exception):
    dt = datetime.now()
    msg = f"{colors['CRITICAL']}{dt} - {tag}: {exception}{Fore.RESET}"
    logger.exception(msg=msg)


def print_function_info(filename: str, function_name: str, message: str = None):
    line_line = "----------------------------------------------------------------"
    msg = f"{colors['INFO']}{line_line}\n{datetime.now()} - {filename} - {function_name}\n{line_line}{Fore.RESET}\n"
    logger.info(msg=msg)


def print_debug_message(tag: str, msg: str = None) -> None:
    msg = f"{colors['DEBUG']}{datetime.now()} - {tag}: {msg}{Fore.RESET}"
    logger.debug(msg=msg)


def print_info_message(tag: str, msg: str = None) -> None:
    msg = f"{colors['INFO']}{datetime.now()} - {tag}: {msg}{Fore.RESET}"
    logger.info(msg=msg)


def print_warning_message(tag: str, msg: str = None) -> None:
    msg = f"{colors['WARNING']}{datetime.now()} - {tag}: {msg}{Fore.RESET}"
    logger.warning(msg=msg)


def print_error_message(tag: str, msg: str = None) -> None:
    msg = f"{colors['ERROR']}{datetime.now()} - {tag}: {msg}{Fore.RESET}"
    logger.error(msg=msg)
