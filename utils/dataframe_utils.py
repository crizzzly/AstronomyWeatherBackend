import os

import numpy as np
import pandas as pd
from pandas import DataFrame
from datetime import datetime

from pandas.core.groupby import DataFrameGroupBy

from exceptionhandler.exception_handler import print_function_info, print_debug_message, print_info_message
from utils.astronomical import add_timedelta_to_current_time
from utils.constants import FORECAST_DURATION_HRS, DEBUG_DF_UTILS
from utils.data_exploration import debug_dataset

_filename = os.path.basename(__file__)
local_tz = datetime.now().astimezone().tzinfo


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
    print_function_info(_filename, "clean_dataset") if DEBUG_DF_UTILS else None

    if DEBUG_DF_UTILS:
        print_debug_message(f"dataset")
        print_debug_message(df.to_string(max_rows=5, show_dimensions=True, min_rows=df.columns.size))

    df.drop(['quality', 'dataset', 'station_id'], axis=1, inplace=True)  # , 'station_id'
    df.dropna(inplace=True)

    date_max = np.datetime64(add_timedelta_to_current_time(hours=FORECAST_DURATION_HRS))
    date_max = pd.to_datetime(date_max, utc=True)
    df['date'] = pd.to_datetime(df['date'], utc=True)

    df = df.query('@df["date"] < @date_max')
    df = df.dropna(axis=0)

    if DEBUG_DF_UTILS:
        print_debug_message("dataset after cleaning", "")
        print_debug_message(str(df.head(7)), "")

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
        print_debug_message("", "")
        print_debug_message("index", str(df.index))
        print_debug_message("columns", df.columns)

    # TODO: Calculate relative humidity with temperature dew point in C° 
    #  RH = 100 × (exp(17.625 × Dp/(243.04 + Dp)]/exp(17.625 × T/(243.04 + T)))
    df['date'] = pd.to_datetime(df['date'], utc=True)
    df.loc[df['parameter'] == 'temperature_air_mean_200', "value"] -= 273.15
    df.loc[df['parameter'] == 'temperature_dew_point_mean_200', "value"] -= 273.15
    df.loc[df['parameter'] == 'wind_speed', "value"] *= 3.6

    # TODO: Maybe convert right before displaying data - else may cause probs with calculations
    df['date'] = df['date'].dt.tz_convert("Europe/Berlin")

    # sort ascending
    df = df.sort_values(by='date', ascending=True)
    return df


def group_dataframes(df_mosmix: DataFrame, df_icon: DataFrame, df_icon_eu: DataFrame) -> DataFrameGroupBy:
    """
    Groups dataframes of different weather models by parameters.
    Combines all three datamodels into one dataframe and saves it in grouped_df.

    Parameters:
    df_mosmix (DataFrame): The dataframe containing Mosmix model data.
    df_icon (DataFrame): The dataframe containing Icon model data.
    df_icon_eu (DataFrame): The dataframe containing Icon EU model data.

    Returns:
    DataFrame.GroupedDataFrame: The grouped dataframe containing data from all three models.

    Note:
    - The dataframes are grouped by the 'parameter' index.
    - The columns of the combined dataframe are renamed to differentiate them.
    - Debugging information is printed if DEBUG_DF_UTILS is True.
    """
    print_function_info(_filename, "group_dataframes") if DEBUG_DF_UTILS else None
    if DEBUG_DF_UTILS:
        print_info_message("_________________ data before grouping/sorting _________________", "")
        print_debug_message("params", df_mosmix['parameter'].unique())

    combined = pd.concat([df_mosmix.set_index(['parameter', 'date']),
                          df_icon.set_index(['parameter', 'date']),
                          df_icon_eu.set_index(['parameter', 'date'])],
                         axis=1)
    combined.columns = ['Mosmix', 'Icon', 'Icon EU']
    print("combined data before")
    print(combined.head(10))
    action = "CONCAT"
    debug_dataset(action, combined) if DEBUG_DF_UTILS else None

    grouped_df = combined.groupby(
        level='parameter',  # Group by 'parameter' index
        # axis=0,  # Specify grouping along rows
        dropna=True,
        as_index=True
        # sort=False,
    )
    print("grouped_df after")
    print(grouped_df.get_group('temperature_air_mean_200').head(10))

    action = "grouped_df"
    debug_dataset(action, grouped_df) if DEBUG_DF_UTILS else None


    for df in grouped_df.groups:
        print(f"df: {df}")

    action = "rename columns"
    debug_dataset(action, grouped_df) if DEBUG_DF_UTILS else None

    return grouped_df


def create_relative_humidity_group(weather_groups: DataFrameGroupBy) -> DataFrameGroupBy:
    """
        Calculates the relative humidity for a given group of weather data.

        Parameters:
        group (DataFrameGroupBy): A group of weather data containing temperature and dew point.
            The group should have the following parameters:
            - 'temperature_air_mean_200': Mean air temperature in Kelvin.
            - 'temperature_dew_point_mean_200': Mean dew point temperature in Kelvin.

        Returns:
        DataFrameGroupBy: A group of weather data containing the calculated relative humidity.

        Note:
        - The relative humidity is calculated using the formula:
          RH = 100 * (e_td / e_t)
          where e_t is the saturation vapor pressure for temperature and e_td is the saturation vapor pressure
          for dew point.
        """

    print_function_info(_filename, "create_relative_humidity_group") if DEBUG_DF_UTILS else None
    print(f"weather_groups:\n {weather_groups.groups}")
    print(f"weather_groups columns:\n {weather_groups.get_group('temperature_air_mean_200').columns}")

    temp_df: DataFrame = weather_groups.get_group('temperature_air_mean_200')
    dew_point_df: DataFrame = weather_groups.get_group('temperature_dew_point_mean_200')
    timeseries = temp_df.index.get_level_values('date')
    param = temp_df.index.get_level_values('parameter')

    relative_humidity_df = temp_df
    relative_humidity_df["df_mosmix"] = _calculate_relative_humidity(temp_df['Mosmix'], dew_point_df['Mosmix'])
    relative_humidity_df["df_icon"] = _calculate_relative_humidity(temp_df['Icon'], dew_point_df['Icon'])
    relative_humidity_df["df_icon_eu"] = _calculate_relative_humidity(temp_df['Icon EU'], dew_point_df['Icon EU'])

    # TODO: Add a MultiIndex to match the group structure
    # relative_humidity_df.set_index(['parameter', 'date'])  # ["relative_humidity", timeseries], level=

    return weather_groups


def _calculate_relative_humidity(temp_ser, dew_point_ser):
    print_function_info(_filename, "_calculate_relative_humidity") if DEBUG_DF_UTILS else None

    # Calculate saturation vapor pressure for temperature
    e_t = 6.112 * temp_ser.apply(lambda x: 10 ** (7.5 * x / (237.7 + x)))
    # Calculate saturation vapor pressure for dew point
    e_td = 6.112 * dew_point_ser.apply(lambda x: 10 ** (7.5 * x / (237.7 + x)))
    # Calculate relative humidity
    relative_humidity = 100 * (e_td / e_t)
    return relative_humidity
