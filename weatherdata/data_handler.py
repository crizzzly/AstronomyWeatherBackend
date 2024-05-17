import os

import pandas as pd
from pandas import DataFrame
from pandas.core.groupby import DataFrameGroupBy

from exceptionhandler.exception_handler import print_function_info, print_debug_message
from dataplotter.plotter import plot_dataframes
from utils.constants import FORECAST_FROM_FILE, DEBUG_DATA_HANDLER
from utils.dataframe_utils import reformat_df_values, clean_dataset, group_dataframes, create_relative_humidity_group
from utils.file_utils import save_json_to_file, load_json_from_file
from weatherdata.dwd_data_fetcher import DwdDataFetcher


_filename = os.path.basename(__file__)


# TODO: calculate relative humidity

class DataHandler:
    def __init__(self):
        self.fetcher = DwdDataFetcher()
        self.df_mosmix = DataFrame()
        self.df_icon = DataFrame()
        self.df_icon_eu = DataFrame()
        # TODO: Check why city name isn't saved when loading from file
        self.city = ""
        self.grouped_df = DataFrameGroupBy(DataFrame())

        # that's why:
        # https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy
        pd.options.mode.copy_on_write = True


    def get_weather_data(self) -> None:
        """
        function set to handle dataflow
        """
        print_function_info(_filename, "get_weather_data") if DEBUG_DATA_HANDLER else None

        self._fetch_new_data()
        self._clean_data()
        self._prepare_data()
        plot_dataframes(self.grouped_df, self.city)

    def _fetch_new_data(self) -> None:
        """
        Fetches new forecast data from different datamodels and assigns the results to different
        attributes (df_mosmix, df_icon, df_icon_eu) of the class instance.
        :return: None
        """
        print_function_info(_filename, "_fetch_new_data") if DEBUG_DATA_HANDLER else None

        if not FORECAST_FROM_FILE:
            self.df_mosmix = self.fetcher.get_mosmix_forecast()
            self.df_icon = self.fetcher.get_icon_forecast()
            self.df_icon_eu = self.fetcher.get_icon_eu_forecast()

            # save as json
            for (df, name) in zip([self.df_mosmix, self.df_icon, self.df_icon_eu],
                                  ["mosmix", "icon", "icon_eu"]):
                save_json_to_file(name, df)

        else:
            # TODO: FutureWarning: Passing literal json to 'read_json' is deprecated.
            #  To read from a literal string, wrap it in a 'StringIO' object
            self.df_mosmix = pd.read_json(load_json_from_file("mosmix"))
            self.df_icon = pd.read_json(load_json_from_file("icon"))
            self.df_icon_eu = pd.read_json(load_json_from_file("icon_eu"))

        if DEBUG_DATA_HANDLER:
            print_debug_message(f"{_filename} - _fetch_new_data\n"
                                f"df_mosmix: {self.df_mosmix}")


    def _clean_data(self) -> None:
        if DEBUG_DATA_HANDLER:
            print_function_info(_filename, "_clean_data")
            print_debug_message(f"{_filename} - _clean_data\n"
                                f"df_mosmix: {self.df_mosmix}")


        self.city = self.fetcher.city

        self.df_mosmix = clean_dataset(self.df_mosmix)
        self.df_icon = clean_dataset(self.df_icon)
        self.df_icon_eu = clean_dataset(self.df_icon_eu)

        self.df_mosmix = reformat_df_values(self.df_mosmix)
        self.df_icon = reformat_df_values(self.df_icon)
        self.df_icon_eu = reformat_df_values(self.df_icon_eu)


    def _prepare_data(self):
        self.grouped_df = group_dataframes(self.df_mosmix, self.df_icon, self.df_icon_eu)
        self.grouped_df = create_relative_humidity_group(self.grouped_df)




if __name__ == '__main__':
    dh = DataHandler()
    dh.get_weather_data()
