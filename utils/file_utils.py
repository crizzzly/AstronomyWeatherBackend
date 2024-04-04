import os

from utils.constants import DEBUG_UTILS
from exceptionhandler.exception_handler import handle_exception, print_debugging_function_header

import json
from datetime import datetime
import pandas as pd
from io import StringIO


local_tz = datetime.now().astimezone().tzinfo

_filename = os.path.basename(__file__)


def save_pd_as_json(filename: str, weather_data: pd.DataFrame):
    print_debugging_function_header(_filename, "save_pd_as_json")
    print(f"{datetime.now()} - saving weather data") if DEBUG_UTILS else None

    try:
        with open(f"json_data/{filename}.json", "w") as outfile:
            json.dump(weather_data.to_json(), outfile)

    except FileNotFoundError as e:
        handle_exception("utils.py - save_pd_as_json", e)
        print(f"error saving weather data: {e.filename}")


def load_json_from_file(filename):
    try:
        with open(f"../json_data/{filename}.json") as json_file:
            return json.load(json_file)
    except Exception as e:
        handle_exception("utils.py - load_json_from_file", e)
