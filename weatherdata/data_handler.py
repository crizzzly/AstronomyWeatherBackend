import os

from dataplotter.plotter import plot_with_px
from exceptionhandler.exception_handler import print_debugging_function_header, print_debugging_message
from utils.file_utils import save_pd_as_json  # , load_json_from_file, read_mixed_df_from_file
from utils.dataframe_utils import reformat_df_values, data_exploration  # ,data_exploration
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
        self.combined_df = DataFrame()
        self.city = ""


    def get_weather_data(self) -> None:  # -> dict[dict[str^, DataFrame]]:
        """
        function set to handle dataflow
        """
        print_debugging_function_header(_filename, "get_weather_data") if DEBUG_DATA_HANDLER else None

        # reset the combined_df
        self.combined_df = DataFrame()
        self._fetch_new_data()
        print_debugging_message("NEW data", self.df_mosmix.to_string(max_rows=5))
        self._clean_data()
        print_debugging_message("CLEANED data", self.df_mosmix.to_string(max_rows=5))
        self._sort_data()
        # self._create_dataplots()
        print_debugging_message("SORTED data", str(self.combined_df)) #  .to_string(max_rows=5))


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

        for df in [self.df_mosmix, self.df_icon, self.df_icon_eu]:
            df = clean_dataset(df)
            df = reformat_df_values(df)



    def _sort_data(self):
        """
        groups dfs of different models by parameters
        Combines all 3 datamodels to one dataframe and saves it in self.combined_df
        """
        if DEBUG_DATA_HANDLER:
            print_debugging_function_header(_filename, "_sort_data")
            print()
            print("data before grouping/sorting")  #
            data_exploration(self.df_mosmix)

        self.combined_df = pd.concat([self.df_mosmix.set_index(['parameter', 'date']),
                                      self.df_icon.set_index(['parameter', 'date']),
                                      self.df_icon_eu.set_index(['parameter', 'date'])],
                                     axis=1)
        self.combined_df.columns = ['Mosmix', 'Icon', 'Icon EU']
        self.combined_df.reset_index(inplace=True)
        print(self.combined_df.columns)
        print(self.combined_df.index)

        self.combined_df = self.combined_df.groupby(
            self.combined_df['parameter'],
            dropna=True,
            as_index=True
        )

        if DEBUG_DATA_HANDLER:
            print("Combined datasets")
            data_exploration(self.combined_df)

        # TODO: Prove once more - saw no differences between previous versions of combined_df
        # Rename the columns to differentiate them
        self.combined_df.columns = ['Mosmix', 'Icon', 'Icon EU']
        if DEBUG_DATA_HANDLER:
            print("renamed columns")
            data_exploration(self.combined_df)

        # Reorder the columns if needed
        self.combined_df = self.combined_df[['parameter', 'date', 'Mosmix', 'Icon', 'Icon EU']]

        print("reordered columns")
        data_exploration(self.combined_df)
        # Now self.df_mosmix contains groups named by parameter,
        # each containing one date column and three columns with values

        # self.combined_df = self.df_mosmix


    def _create_dataplots(self):
        print_debugging_function_header(_filename, "_create_dataplots")  if DEBUG_DATA_HANDLER else None

        cloud_data = self.combined_df.loc["cloud_cover_total"]
        wind_speed_direction = self.combined_df.loc[("wind_speed", "wind_direction")]
        temperature_data = self.combined_df.loc[("temperature_air_mean_200", "temperature_dew_point_mean_200")]
        visibility_data = self.combined_df.loc["visibility_range"]

        for df, name in zip([cloud_data, wind_speed_direction, temperature_data, visibility_data],
                            ["Clouds", "Wind Speed And Direction", "Temperature and Dew Point", "Visibility"]):
            plot_with_px(df, name, self.city)


if __name__ == '__main__':
    dh = DataHandler()
    dh.get_weather_data()
