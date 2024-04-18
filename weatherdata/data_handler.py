import os

import pandas as pd
from pandas import DataFrame
from pandas.core.groupby import DataFrameGroupBy

from exceptionhandler.exception_handler import print_function_info, print_debug_message, print_info_message
from dataplotter.plotter import plot_grouped_df
from utils.constants import FORECAST_FROM_FILE, DEBUG_DATA_HANDLER
from utils.dataframe_utils import reformat_df_values, clean_dataset
from utils.data_exploration import debug_dataset
from utils.file_utils import save_pd_as_json
from weatherdata.dwd_data_fetcher import DwdDataFetcher


_filename = os.path.basename(__file__)


class DataHandler:
    def __init__(self):
        self.fetcher = DwdDataFetcher()
        self.df_mosmix = DataFrame()
        self.df_icon = DataFrame()
        self.df_icon_eu = DataFrame()
        # TODO: Check why city name isn't saved
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
        self._sort_data()
        self._create_dataplots()

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
                save_pd_as_json(name, df)

        else:
            self.df_mosmix = self.fetcher.get_mosmix_forecast()
            self.df_icon = self.fetcher.get_icon_forecast()
            self.df_icon_eu = self.fetcher.get_icon_eu_forecast()

        if DEBUG_DATA_HANDLER:
            print_debug_message(f"{_filename} - _fetch_new_data\n"
                                f"df_mosmix: {self.df_mosmix}")


    def _clean_data(self) -> None:
        if DEBUG_DATA_HANDLER:
            print_function_info(_filename, "_clean_data")
            print_debug_message(f"{_filename} - _clean_data\n"
                                f"df_mosmix: {self.df_mosmix}")

        # self.df_mosmix = self.df_mosmix.dropna()
        # self.df_icon = self.df_icon.dropna()
        # self.df_icon_eu = self.df_icon_eu.dropna()

        self.city = self.fetcher.city

        self.df_mosmix = clean_dataset(self.df_mosmix)
        self.df_icon = clean_dataset(self.df_icon)
        self.df_icon_eu = clean_dataset(self.df_icon_eu)

        self.df_mosmix = reformat_df_values(self.df_mosmix)
        self.df_icon = reformat_df_values(self.df_icon)
        self.df_icon_eu = reformat_df_values(self.df_icon_eu)

    def _sort_data(self):
        """
        groups dfs of different models by parameters
        Combines all 3 datamodels to one dataframe and saves it in self.grouped_df
        """
        print_function_info(_filename, "_sort_data") if DEBUG_DATA_HANDLER else None
        if DEBUG_DATA_HANDLER:
            print_info_message("_________________ data before grouping/sorting _________________", "")
            print_debug_message("params", self.df_mosmix['parameter'].unique())

        combined = pd.concat([self.df_mosmix.set_index(['parameter', 'date']),
                              self.df_icon.set_index(['parameter', 'date']),
                              self.df_icon_eu.set_index(['parameter', 'date'])],
                             axis=1)
        combined.columns = ['Mosmix', 'Icon', 'Icon EU']

        action = "\n================= CONCAT =================\n"
        debug_dataset(action, combined) if DEBUG_DATA_HANDLER else None

        self.grouped_df = combined.groupby(
            level='parameter',  # Group by 'parameter' index
            # axis=0,  # Specify grouping along rows
            dropna=True,
            # sort=False,
        )


        action = "\n=========================== self.grouped_df =========================== \n"
        debug_dataset(action, self.grouped_df) if DEBUG_DATA_HANDLER else None

        # Rename the columns to differentiate them
        self.grouped_df.columns = ['df_mosmix', 'df_icon', 'df_icon_eu']

        action = "\n=========================== rename columns =========================== \n"
        debug_dataset(action, self.grouped_df) if DEBUG_DATA_HANDLER else None
        # Reset index to make 'parameter' and 'date' regular columns
        # self.grouped_df.reset_index(inplace=True)

        # explore_group(self.grouped_df)
        # Now self.df_mosmix contains groups named by parameter,
        # each containing one date column and three columns with values

        # self.grouped_df = self.df_mosmix

    def _create_dataplots(self):
        print_function_info(_filename, "_create_dataplots") if DEBUG_DATA_HANDLER else None
        plot_grouped_df(self.grouped_df, self.city)


if __name__ == '__main__':
    dh = DataHandler()
    dh.get_weather_data()
