import os

from pandas.core.groupby import DataFrameGroupBy, GroupBy

from dataplotter.plotter import plot_df_dict
from exceptionhandler.exception_handler import print_debugging_function_header, print_debugging_message, \
    handle_exception, print_error_message
from utils.file_utils import save_pd_as_json  # , load_json_from_file, read_mixed_df_from_file
from utils.dataframe_utils import reformat_df_values, explore_group_via_terminal, \
    extract_weatherdata_from_grouped_df, print_groups_from_grouped_df
from utils.constants import FORECAST_FROM_FILE, DEBUG_DATA_HANDLER
from utils.dataframe_utils import clean_dataset
from weatherdata.dwd_data_fetcher import DwdDataFetcher

import pandas as pd
from pandas import DataFrame

_filename = os.path.basename(__file__)


# TODO: replace DEBUG_ and print with exceptionhandler/logging

# TODO: Reshape in functions "get/load_data", "prepare/sort_data" and "plot_data
#  and use public function "load_new_dataset" as public function


class DataHandler:
    def __init__(self):
        self.fetcher = DwdDataFetcher()
        self.df_mosmix = DataFrame()
        self.df_icon = DataFrame()
        self.df_icon_eu = DataFrame()
        self.city = ""
        self.grouped_df = DataFrameGroupBy(DataFrame())

    def get_weather_data(self) -> None:  # -> dict[dict[str^, DataFrame]]:
        """
        function set to handle dataflow
        """
        print_debugging_function_header(_filename, "get_weather_data") if DEBUG_DATA_HANDLER else None

        self._fetch_new_data()
        print_debugging_message("NEW data", self.df_mosmix.to_string(max_rows=5))
        self._clean_data()
        print_debugging_message("CLEANED data", self.df_mosmix.to_string(max_rows=5))
        self._sort_data()
        # self._create_dataplots()
        # print_debugging_message("SORTED data", str(self.grouped_df))  # .to_string(max_rows=5))

    def _fetch_new_data(self) -> None:
        """
        Fetches new forecast data from different datamodels and assigns the results to different
        attributes (df_mosmix, df_icon, df_icon_eu) of the class instance.
        :return: None
        """
        print_debugging_function_header(_filename, "_fetch_new_data") if DEBUG_DATA_HANDLER else None

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
            print("df_mosmix")
            print(self.df_mosmix)
            # print(f"df_icon: {self.df_icon}")
            # print(f"df_icon_eu: {self.df_icon_eu}")

    def _clean_data(self) -> None:
        if DEBUG_DATA_HANDLER:
            print_debugging_function_header(_filename, "_clean_data")
            print("df_mosmix")
            print(self.df_mosmix)

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
        if DEBUG_DATA_HANDLER:
            print_debugging_function_header(_filename, "_sort_data")
            print()
            print("______________________data before grouping/sorting ______________________")  #
            explore_group_via_terminal(self.df_mosmix)
            print(self.df_mosmix['parameter'].unique())

        combined = pd.concat([self.df_mosmix.set_index(['parameter', 'date']),
                              self.df_icon.set_index(['parameter', 'date']),
                              self.df_icon_eu.set_index(['parameter', 'date'])],
                             axis=1)
        combined.columns = ['Mosmix', 'Icon', 'Icon EU']

        if DEBUG_DATA_HANDLER:
            print("================= CONCAT =================")
            print(combined.columns)
            print(combined.index)

        try:
            self.grouped_df = combined.groupby(
                level='parameter',  # Group by 'parameter' index
                axis=0,  # Specify grouping along rows
                dropna=True
            )
            print(f"type(self.grouped_df): {type(self.grouped_df)}")
        except Exception as e:
            print_error_message("Error in _sort_data", "Creating a group did not do well")
            handle_exception(_filename, e)


        if DEBUG_DATA_HANDLER:
            print("____________________________ self.grouped_df ____________________________ ")
            print(f"type in data_handler: {type(self.grouped_df)}")
            print_groups_from_grouped_df(self.grouped_df)
            explore_group_via_terminal(self.grouped_df)

        # TODO: Prove once more - saw no differences between previous versions of combined_df
        # Rename the columns to differentiate them
        if DEBUG_DATA_HANDLER:
            print("____________________________ renaming columns ____________________________")
            print_groups_from_grouped_df(self.grouped_df)
        self.grouped_df.columns = ['Mosmix', 'Icon', 'Icon EU']
        if DEBUG_DATA_HANDLER:
            print("____________________________ renamed columns ____________________________")
            print_groups_from_grouped_df(self.grouped_df)
            # explore_group_via_terminal(self.grouped_df)

        # Reorder the columns if needed
        # self.grouped_df = self.grouped_df[['parameter', 'date', 'Mosmix', 'Icon', 'Icon EU']]

        print("____________________________ reordered columns ____________________________")
        explore_group_via_terminal(self.grouped_df)
        # Now self.df_mosmix contains groups named by parameter,
        # each containing one date column and three columns with values

        # self.grouped_df = self.df_mosmix

    def _create_dataplots(self):
        print_debugging_function_header(_filename, "_create_dataplots") if DEBUG_DATA_HANDLER else None
        df_dict = extract_weatherdata_from_grouped_df(self.grouped_df)
        plot_df_dict(df_dict, self.city)


if __name__ == '__main__':
    dh = DataHandler()
    dh.get_weather_data()
