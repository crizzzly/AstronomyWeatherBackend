from datetime import datetime
import logging

logger = logging.getLogger("exceptionhandler")
logger.setLevel(logging.DEBUG)

fh = logging.FileHandler("exceptionhandler.log")
fh.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

logger.addHandler(fh)
logger.addHandler(ch)


def handle_exception(tag: str, exception: Exception):
    dt = datetime.now()
    logger.exception(f"{dt} - {tag}: {exception}")


def print_debugging_function_header(filename: str, function_name: str, message: str = None):
    line_line = "----------------------------------------------------------------"
    msg = f"{datetime.now()} - {filename} - {function_name}"
    logger.info(f"{line_line}\n{msg}\n{line_line}")


def print_debugging_message(tag: str, msg: str = None):
    logger.debug(f"{datetime.now()} - {tag}: {msg}")


def print_error_message(tag: str, msg: str = None):
    logger.exception(f"{datetime.now()} - {tag}: {msg}")
