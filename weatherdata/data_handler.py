from io import StringIO
from typing import Dict

import pandas as pd
from pandas import DataFrame

from utils import load_from_file, save_to_file, DF_LENGTH, PARAMS_MOSMIX
from weatherdata import DwdDataFetcher

# DF_LENGTH = 78
FROM_FILE = True



def get_mixed_df_per_param(col_name, mosmix_forecast, icon_forecast, icon_eu_forecast):
    df = pd.DataFrame()
    if FROM_FILE:
        df = pd.read_json(StringIO(load_from_file(col_name)))
    else:
        date_col = mosmix_forecast[col_name]['date'].head(DF_LENGTH)
        vals_col = mosmix_forecast[col_name]['value'].head(DF_LENGTH)
        icon_eu_col = icon_eu_forecast[col_name]['value'].head(DF_LENGTH)
        icon_col = icon_forecast[col_name]['value'].head(DF_LENGTH)
        df['date'] = date_col
        df['mosmix_value'] = vals_col
        df['icon_value'] = icon_col
        df['icon_eu_value'] = icon_eu_col
        save_to_file(col_name, df)

    df.set_index("date")
    return df


class DataHandler:
    fetcher = DwdDataFetcher()

    def __init__(self):
        self.cloud_cover_total = pd.DataFrame()
        self.cloud_cover_below_500_ft = pd.DataFrame()
        self.cloud_cover_below_1000_ft = pd.DataFrame()
        self.cloud_cover_above_7_km = pd.DataFrame()

        self.forecast_dict = {}

    def get_latest_weather_datasets(self) -> dict[str, pd.DataFrame]:
        mosmix = self.fetcher.get_mosmix_forecast()
        icon = self.fetcher.get_icon_forecast()
        icon_eu = self.fetcher.get_icon_eu_forecast()
        for param in PARAMS_MOSMIX:
            df = get_mixed_df_per_param(param, mosmix, icon, icon_eu)
            self.forecast_dict[param] = df
        # self.cloud_cover_total = get_mixed_df_per_param("cloud_cover_total", mosmix, icon, icon_eu)
        # self.cloud_cover_below_500_ft = get_mixed_df_per_param("cloud_cover_below_500_ft", mosmix, icon, icon_eu)
        # self.cloud_cover_below_1000_ft = get_mixed_df_per_param("cloud_cover_below_1000_ft", mosmix, icon, icon_eu)
        # self.cloud_cover_above_7_km = get_mixed_df_per_param("cloud_cover_above_7_km", mosmix, icon, icon_eu)
        #
        # # df_dict: dict[str, pd.DataFrame] = dict
        # df_dict: dict[str, DataFrame] = {"cloud_cover_total": self.cloud_cover_total,
        #            "cloud_cover_below_500_ft": self.cloud_cover_below_500_ft,
        #            "cloud_cover_below_1000_ft": self.cloud_cover_below_1000_ft,
        #            "cloud_cover_above_7_km": self.cloud_cover_above_7_km}  # dict()

        return self.forecast_dict

