from io import StringIO

from dataplotter.plotter import plot_forecast_datasets
from utils.utils import load_from_file
from utils.constants import FORECAST_FROM_FILE
from utils.constants_weatherdata import PARAMS_MOSMIX, PARAMS_OBSERVATION
from exceptionhandler.exception_handler import handle_standard_exception


import tzlocal
import pandas as pd
from pandas import DataFrame

from weatherdata.dwd_data_fetcher import DwdDataFetcher
from weatherdata.sort_data import get_nights_only_as_list, sort_df_per_param, group_df_per_parameter


local_tz = tzlocal.get_localzone()


# TODO: Reshape in functions "get/load_data", "prepare/sort_data" and "plot_data
#  and use public function "load_new_dataset" as public function

def read_mixed_df_from_file(filename):
    try:
        df = pd.read_json(StringIO(load_from_file(filename)))
    except Exception as e:
        handle_standard_exception("Data_handler.py read_mixed_df_from_file")
    finally:
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

        self.observation: dict[str, dict[str, DataFrame]] = {}

        self.mosmix = DataFrame()
        self.icon = DataFrame()
        self.icon_eu = DataFrame()


    def load_new_dataset(self):
        self.get_weather_data()
        plot_forecast_datasets(self.sorted_forecast_dict)


    def get_weather_data(self):  # -> dict[dict[str, DataFrame]]:
        if FORECAST_FROM_FILE:
            for day in ["tonight", "tomorrow", "tomorrow2"]:
                for param in PARAMS_MOSMIX:
                    dict_df = read_mixed_df_from_file(f"{day}/{param}")
                    self.sorted_forecast_dict[param] = dict_df
            self.forecast_tonight = self.sorted_forecast_dict["tonight"]
            self.forecast_tomorrow = self.sorted_forecast_dict["tomorrow"]
            self.forecast_tomorrow2 = self.sorted_forecast_dict["tomorrow2"]
        else:
            self.fetch_new_forecast_data()
            self.sort_forecasts()
            # self.fetch_and_sort_observations()


    def fetch_new_forecast_data(self) -> None:
        """
        It calls three different methods from Fetcher class to fetch forecast data from different datamodels
        and assigns the results to different attributes (mosmix, icon, icon_eu) of the class instance.
        :return: None
        """

        # dataframe with columns ['station_id', 'dataset', 'parameter', 'date', 'value', 'quality']
        self.mosmix = self.fetcher.get_mosmix_forecast()
        self.icon = self.fetcher.get_icon_forecast()
        self.icon_eu = self.fetcher.get_icon_eu_forecast()


    def sort_forecasts(self) -> dict[str, dict[str, DataFrame]]:
        self.fetch_and_sort_forecasts()


    def fetch_and_sort_forecasts(self) -> dict[str, dict[str, DataFrame]]:
        # TODO: KEEP SEQUENCE Mosmix - Icon - Icon EU
        # Fetch the forecast
        # mosmix = self.fetcher.get_mosmix_forecast()
        # icon = self.fetcher.get_icon_forecast()
        # icon_eu = self.fetcher.get_icon_eu_forecast()

        # Process forecasts
        mosmix_forecasts = get_nights_only_as_list(self.mosmix)
        icon_forecasts = get_nights_only_as_list(self.icon)
        icon_eu_forecasts = get_nights_only_as_list(self.icon_eu)

        # Group forecasts by parameter
        mosmix_dfs = [group_df_per_parameter(forecast, PARAMS_MOSMIX) for forecast in mosmix_forecasts]
        icon_dfs = [group_df_per_parameter(forecast, PARAMS_MOSMIX) for forecast in icon_forecasts]
        icon_eu_dfs = [group_df_per_parameter(forecast, PARAMS_MOSMIX) for forecast in icon_eu_forecasts]


        # Sort forecasts by night
        self.forecast_tomorrow = sort_df_per_param(PARAMS_MOSMIX, *mosmix_dfs,  name="tomorrow")
        self.forecast_tomorrow2 = sort_df_per_param(PARAMS_MOSMIX, *icon_dfs, name="tomorrow2")
        self.forecast_tonight = sort_df_per_param(PARAMS_MOSMIX, *icon_eu_dfs, name="tonight")




        self.sorted_forecast_dict = {
            "tonight": self.forecast_tonight,
            "tomorrow": self.forecast_tomorrow,
            "tomorrow2": self.forecast_tomorrow2
        }
        return self.sorted_forecast_dict

    def fetch_and_sort_observations(self):
        observation = self.fetcher.get_observation()

        # process (get_nights_only)
        observation_forecasts = get_nights_only_as_list(observation)
        observation_dfs = [group_df_per_parameter(forecast, PARAMS_OBSERVATION) for forecast in observation_forecasts]
        self.observation = sort_df_per_param(PARAMS_OBSERVATION, *observation_dfs, name="observation")


if __name__ == '__main__':
    dh = DataHandler()
    dh.get_weather_data()
