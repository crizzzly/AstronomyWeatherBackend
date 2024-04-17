import os
import pandas as pd
from pandas import DataFrame
from datetime import datetime

from exceptionhandler.exception_handler import print_function_info, print_debug_message
from utils.astronomical import add_timedelta_to_current_time
from utils.constants import DEBUG_DF_UTILS, FORECAST_DURATION_HRS

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

    date_max = add_timedelta_to_current_time(hours=FORECAST_DURATION_HRS)
    df = df.query('@df["date"] < @date_max')

    if DEBUG_DF_UTILS:
        print_debug_message("datatypes after cleaning")
        print_debug_message(str(df.dtypes))

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
        print_debug_message("datatypes", str(df.dtypes))
        print_debug_message("columns", df.columns)
        print_debug_message("")

    df['date'] = pd.to_datetime(df['date'], utc=True)

    # sort ascending
    df = df.sort_values(by='date', ascending=True)
    # TODO: Maybe convert right before displaying data - else may cause probs with calculations
    df['date'] = df['date'].dt.tz_convert("Europe/Berlin")
    return df
