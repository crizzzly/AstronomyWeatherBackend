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
        print(f"{Fore.BLUE}{_filename} - ColoredFormatter {Fore.RESET}")
        print(f"record.name: {Fore.CYAN}{record.name}{Fore.RESET}")
        print(f"record.levelname: {record.levelname}")
        print(f"record.getMessage(): {record.getMessage()}")
        print(f"record.message: {record.message}")
        levelname_color = record.levelname
        return f"{levelname_color} - {message}{Fore.RESET}"  # Reset color after the message

        # message_color = f"{Fore.RESET}{message}{Fore.RESET}"  # Reset color after message
        # return f"{levelname_color} - {message_color}"

logger = logging.getLogger("exceptionhandler")
logger.setLevel(logging.DEBUG)

# File handler
fh = logging.FileHandler("exceptionhandler.log")
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
# print("===================== LOGGER TEST =====================")
# logger.debug(f'{colors["DEBUG"]}This is a debug message{Fore.RESET}')
# logger.info(f'{colors["INFO"]}This is an info message{Fore.RESET}')
# logger.warning('This is a warning message')
# logger.error('This is an error message')
# logger.critical('This is a critical message')
# print("===================== TEST END =====================")


def print_exception(tag: str, exception: Exception):
    dt = datetime.now()
    msg = f"{colors['CRITICAL']}{dt} - {tag}: {exception}{Fore.RESET}"
    logger.exception(msg=msg)


def print_function_info(filename: str, function_name: str, message: str = None):
    line_line = "----------------------------------------------------------------"
    msg = f"{colors['INFO']}{line_line}\n{datetime.now()} - {filename} - {function_name}\n{line_line}{Fore.RESET}\n"
    logger.info(msg=msg)


def print_debugging_message(tag: str, msg: str = None) -> object:
    msg = f"{colors['DEBUG']}{datetime.now()} - {tag}: {msg}{Fore.RESET}"
    logger.debug(msg=msg)


def print_info_message(tag: str, msg: str = None):
    msg = f"{colors['INFO']}{datetime.now()} - {tag}: {msg}{Fore.RESET}"
    logger.info(msg=msg)


def print_warning_message(tag: str, msg: str = None):
    msg = f"{colors['WARNING']}{datetime.now()} - {tag}: {msg}{Fore.RESET}"
    logger.warning(msg=msg)


def print_error_message(tag: str, msg: str = None):
    msg = f"{colors['ERROR']}{datetime.now()} - {tag}: {msg}{Fore.RESET}"
    logger.error(msg=msg)


def print_error_message(tag: str, msg: str = None):
    logger.exception(msg=f"{datetime.now()} - {tag}: {msg}")
