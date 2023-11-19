import json
from datetime import datetime

import pandas as pd


def save_to_file(filename: str, weather_data: pd.DataFrame):
    print(f"{datetime.now()} - saving weather data") #if DEBUG_DWD_FETCHER else None

    with open(f"json_data/{filename}.json", "w") as outfile:
        json.dump(weather_data.to_json(), outfile)


def load_from_file(filename):
    with open(f"json_data/{filename}.json") as json_file:
        return json.load(json_file)



