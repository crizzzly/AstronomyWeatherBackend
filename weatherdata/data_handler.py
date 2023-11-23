from io import StringIO

import tzlocal

import pandas as pd
from pandas import DataFrame

from dataplotter import plot_forecast_datasets
from utils import load_from_file, PARAMS_MOSMIX, FORECAST_FROM_FILE
from weatherdata.dwd_data_fetcher import DwdDataFetcher
from weatherdata.sort_data import get_nights_only_as_list, sort_df_per_param, group_df_per_parameter

local_tz = tzlocal.get_localzone()


def get_mixed_df_from_file(filename):
    df = pd.read_json(StringIO(load_from_file(filename)))
    df["date"] = pd.to_datetime(df["date"], unit="s")
    df["date"] = df["date"].dt.tz_localize("UTC").dt.tz_convert(local_tz)
    return df



class DataHandler:

    def __init__(self):
        self.fetcher = DwdDataFetcher()
        self.sorted_forecast_dict = {}  # : dict[str, DataFrame] = {}
        self.forecast_tonight = DataFrame()
        self.forecast_tomorrow: dict[str, dict[str, DataFrame]] = {}
        self.forecast_tomorrow2: dict[str, dict[str, DataFrame]] = {}


    def get_weather_data(self):  # -> dict[dict[str, DataFrame]]:
        if FORECAST_FROM_FILE:
            for day in ["tonight", "tomorrow", "tomorrow2"]:
                for param in PARAMS_MOSMIX:
                    dict_df = get_mixed_df_from_file(f"{day}/{param}")
                    self.sorted_forecast_dict[param] = dict_df
            self.forecast_tonight = self.sorted_forecast_dict["tonight"]
            self.forecast_tomorrow = self.sorted_forecast_dict["tomorrow"]
            self.forecast_tomorrow2 = self.sorted_forecast_dict["tomorrow2"]

            # self.sorted_forecast_dict
            # return self.sorted_forecast_dict
        else:
            self.fetch_and_sort_forecasts()
            # return self.fetch_and_sort_forecasts()



    def fetch_and_sort_forecasts(self) -> dict[str, dict[str, DataFrame]]:
        # Fetch the forecast
        mosmix = self.fetcher.get_mosmix_forecast()
        icon = self.fetcher.get_icon_forecast()
        icon_eu = self.fetcher.get_icon_eu_forecast()

        # Process forecasts
        mosmix_forecasts = get_nights_only_as_list(mosmix)
        icon_forecasts = get_nights_only_as_list(icon)
        icon_eu_forecasts = get_nights_only_as_list(icon_eu)

        # Group forecasts by parameter
        mosmix_dfs = [group_df_per_parameter(forecast, PARAMS_MOSMIX) for forecast in mosmix_forecasts]
        icon_dfs = [group_df_per_parameter(forecast, PARAMS_MOSMIX) for forecast in icon_forecasts]
        icon_eu_dfs = [group_df_per_parameter(forecast, PARAMS_MOSMIX) for forecast in icon_eu_forecasts]


        # Sort forecasts by night
        self.forecast_tomorrow = sort_df_per_param(PARAMS_MOSMIX, *mosmix_dfs,  name="tomorrow")
        self.forecast_tomorrow2 = sort_df_per_param(PARAMS_MOSMIX, *icon_dfs, name="tomorrow2")
        self.forecast_tonight = sort_df_per_param(PARAMS_MOSMIX, *icon_eu_dfs, name="tonight")

        plot_forecast_datasets(self.forecast_tonight)

        self.sorted_forecast_dict = {
            "tonight": self.forecast_tonight,
            "tomorrow": self.forecast_tomorrow,
            "tomorrow2": self.forecast_tomorrow2
        }
        return self.sorted_forecast_dict
