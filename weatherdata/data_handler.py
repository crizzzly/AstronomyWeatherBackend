import os

from dataplotter.plotter import plot_with_px
from utils.debugging_outputs import print_function_header
from utils.file_utils import save_pd_as_json  # , load_json_from_file, read_mixed_df_from_file
from utils.dataframe_utils import reformat_df_values  # ,data_exploration
from utils.constants import FORECAST_FROM_FILE, DEBUG_DATA_HANDLER
from utils.dataframe_utils import clean_dataset
from weatherdata.dwd_data_fetcher import DwdDataFetcher
# from exceptionhandler.exception_handler import handle_standard_exception

import pandas as pd
from pandas import DataFrame


_filename = os.path.basename(__file__)

# TODO: Reshape in functions "get/load_data", "prepare/sort_data" and "plot_data
#  and use public function "load_new_dataset" as public function


class DataHandler:
    def __init__(self):
        self.fetcher = DwdDataFetcher()
        self.df_mosmix = DataFrame()
        self.df_icon = DataFrame()
        self.df_icon_eu = DataFrame()
        self.combined_df = DataFrame()


    def get_weather_data(self) -> None:  # -> dict[dict[str^, DataFrame]]:
        """
        function set to handle dataflow
        """
        print_function_header(_filename, "get_weather_data") if DEBUG_DATA_HANDLER else None

        # reset the combined_df
        self.combined_df = DataFrame()
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
        print_function_header(_filename, "_fetch_new_data")

        if not FORECAST_FROM_FILE:
            for (df, name) in zip([self.df_mosmix, self.df_icon, self.df_icon_eu],
                                  ["mosmix", "icon", "icon_eu"]):
                df = self.fetcher.get_mosmix_forecast()
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
            print_function_header(_filename, "_clean_data")
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
            print_function_header(_filename, "_sort_data")
            print()
            print("data before grouping/sorting")  #
            print(self.df_mosmix)


        for df in [self.df_mosmix, self.df_icon, self.df_icon_eu]:
            df = df.groupby(df['parameter'], dropna=True)  #.apply(lambda x: x)
            print(df) if DEBUG_DATA_HANDLER else None

        if DEBUG_DATA_HANDLER:
            print("Data after grouping")
            print(self.df_mosmix)

        self.combined_df = pd.concat([self.df_mosmix.set_index(['parameter', 'date']),
                                      self.df_icon.set_index(['parameter', 'date']),
                                      self.df_icon_eu.set_index(['parameter', 'date'])],
                                     axis=1)

        # Concatenate the dataframes along the columns axis
        concatenated_df = pd.concat([self.df_mosmix,  #.set_index(['parameter', 'date']),
                                     self.df_icon,  #.set_index(['parameter', 'date']),
                                     self.df_icon_eu], axis=1)  #.set_index(['parameter', 'date'])],

        if DEBUG_DATA_HANDLER:
            print("combined dataframes")
            print(concatenated_df)
            print("columns")
            print(concatenated_df.columns)


        # Rename the columns to differentiate them
        concatenated_df.columns = ['df_mosmix', 'df_icon', 'df_icon_eu']

        # Reset index to make 'parameter' and 'date' regular columns
        # concatenated_df.reset_index(inplace=True)

        if DEBUG_DATA_HANDLER:
            print("renamed columns and resetted index")
            print(concatenated_df)
            print("columns")
            print(concatenated_df.columns)

        # Reorder the columns if needed
        # concatenated_df = concatenated_df[['parameter', 'date', 'df_mosmix', 'df_icon', 'df_icon_eu']]

        # Now concatenated_df contains groups named by parameter,
        # each containing one date column and three columns with values

        self.combined_df = concatenated_df


    def _create_dataplots(self):
        print_function_header(_filename, "_create_dataplots")

        cloud_data = self.combined_df.loc["cloud_cover_total"]
        wind_speed_direction = self.combined_df.loc[("wind_speed", "wind_direction")]
        temperature_data = self.combined_df.loc[("temperature_air_mean_200", "temperature_dew_point_mean_200")]
        visibility_data = self.combined_df.loc["visibility_range"]

        for df, name in zip([cloud_data, wind_speed_direction, temperature_data, visibility_data],
                            ["Clouds", "Wind Speed And Direction", "Temperature and Dew Point", "Visibility"]):
            plot_with_px(df, name)


if __name__ == '__main__':
    dh = DataHandler()
    dh.get_weather_data()
