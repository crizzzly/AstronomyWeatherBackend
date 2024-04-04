import os
from datetime import datetime
import pandas as pd
from pandas import DataFrame
from pandas.core.groupby.generic import DataFrameGroupBy

from exceptionhandler.exception_handler import print_function_info, print_debugging_message
from utils.constants import DEBUG_DF_UTILS

_filename = os.path.basename(__file__)
local_tz = datetime.now().astimezone().tzinfo


def extract_dfs_from_group(grouped_df: DataFrameGroupBy) -> dict[str, DataFrame]:
    """
    takes a grouped DataFrame as input and extracts specific weather data from it,
    such as cloud coverage, wind speed, wind direction, temperature, dew point, and visibility range.
    It then returns a dictionary containing the extracted data,
    with the weather data type as the key and the corresponding DataFrame as the value.
    :rtype: object
    :param grouped_df: DataFrameGroupBy
    :return: dictionary containing the extracted weather with the value name as key
    """
    cloud_data = grouped_df.get_group("cloud_cover_total")
    wind_speed = grouped_df.get_group("wind_speed")
    wind_direction = grouped_df.get_group("wind_direction")
    temp = grouped_df.get_group("temperature_air_mean_200")
    dew_point = grouped_df.get_group("temperature_dew_point_mean_200")
    visibility = grouped_df.get_group("visibility_range")

    df_dict = {}

    name_list_beautified = ["Cloud Coverage", "Wind Speed", "Wind Direction", "Temperature", "Dew Point",
                            "Visibility Range"]
    name_list = ["cloud_cover_total", "wind_speed", "wind_direction", "temperature_air_mean_200",
                 "temperature_dew_point_mean_200", "visibility_range"]
    for df, name, name_beauty in zip(
            [cloud_data, wind_speed, wind_direction, temp, dew_point, visibility],
            name_list,
            name_list_beautified):
        df_dict[name_beauty] = df

    return df_dict


def clean_dataset(df: DataFrame) -> DataFrame:
    """
    Cleans the given DataFrame by
    - dropping certain columns,
    - removing rows with missing values,
    - converting values to proper formats
    and returning the cleaned DataFrame.

    Parameters:
    df (DataFrame): The input DataFrame to be cleaned.
    Columns: ['station_id', 'dataset', 'parameter', 'date', 'value', 'quality']

    Returns:
    DataFrame: The cleaned DataFrame with columns 'station_id', 'dataset', 'parameter', 'date'
    """
    print_function_info(_filename, "clean_dataset")

    if DEBUG_DF_UTILS:
        print_debugging_message(f"dataset")
        print_debugging_message(df.to_string(max_rows=5, show_dimensions=True, min_rows=df.columns.size))

    name = df['station_id'][0]
    print(name)

    df.drop(['quality', 'dataset', 'station_id'], axis=1, inplace=True)  # , 'station_id'
    df.dropna(inplace=True)

    if DEBUG_DF_UTILS:
        print_debugging_message("datatypes before cleaning")
        print_debugging_message(str(df.dtypes))

    return df


def reformat_df_values(df: DataFrame) -> DataFrame:
    """
    Reformat the column-values of the given DataFrame to match the expected format.

    Parameters:
    df (DataFrame): The input DataFrame to be reformatted.

    Returns:
    DataFrame: The reformatted DataFrame
    """
    if DEBUG_DF_UTILS:
        print_function_info(_filename, "reformat_df_values")
        print_debugging_message("", "")
        print_debugging_message("datatypes", str(df.dtypes))
        print_debugging_message("columns", df.columns)
        print_debugging_message("")

    df['date'] = pd.to_datetime(df['date'], utc=True)
    df['date'] = df['date'].dt.tz_convert("Europe/Berlin")

    return df
