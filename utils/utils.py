from utils.constants import DEBUG_UTILS
from exceptionhandler.exception_handler import handle_standard_exception

import json
from datetime import datetime
import pandas as pd


def save_to_file(filename: str, weather_data: pd.DataFrame):
    print(f"{datetime.now()} - saving weather data") if DEBUG_UTILS else None

    try:
        with open(f"json_data/{filename}.json", "w") as outfile:
            json.dump(weather_data.to_json(), outfile)

    except FileNotFoundError as e:
        handle_standard_exception("utils.py - save_to_file", e)
        print(f"error saving weather data: {e.filename}")


def load_from_file(filename):
    try:
        with open(f"../json_data/{filename}.json") as json_file:
            return json.load(json_file)
    except Exception as e:
        handle_standard_exception("utils.py - load_from_file", e)


