from datetime import datetime


def print_function_header(filename: str, function_name: str):
    print("----------------------------------------------------------------")
    print(f"{datetime.now()} - {filename} - {function_name}")
    print("----------------------------------------------------------------")