import os

from utils.constants import DEBUG_UTILS
from exceptionhandler.exception_handler import print_exception, print_function_info

import json
from datetime import datetime
import pandas as pd

local_tz = datetime.now().astimezone().tzinfo

_filename = os.path.basename(__file__)


def save_json_to_file(filename: str, weather_data: pd.DataFrame):
    print_function_info(_filename, "save_pd_as_json") if DEBUG_UTILS else None
    print(f"{datetime.now()} - saving weather data") if DEBUG_UTILS else None

    try:
        with open(f"json_data/{filename}.json", "w") as outfile:
            json.dump(weather_data.to_json(), outfile)

    except FileNotFoundError as e:
        print_exception("utils.py - save_pd_as_json", e)
        print(f"error saving weather data: {e.filename}")


def load_json_from_file(filename) -> str:
    try:
        with open(f"json_data/{filename}.json") as json_file:
            return json.load(json_file)
    except Exception as e:
        print_exception("utils.py - load_json_from_file", e)
