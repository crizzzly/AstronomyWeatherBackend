from datetime import datetime


def handle_standard_exception(tag: str, exception: Exception):
    dt = datetime.now()
    print(f"{dt} - {tag}: {exception}")