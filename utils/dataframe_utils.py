import os
from datetime import datetime
from io import StringIO

import pandas as pd
from pandas import DataFrame
from pandas.core.groupby.generic import DataFrameGroupBy

from exceptionhandler.exception_handler import handle_exception, print_debugging_function_header, \
    print_debugging_message
from utils.constants import DEBUG_DF_UTILS, DEBUG_UTILS
from utils.file_utils import load_json_from_file

_filename = os.path.basename(__file__)
local_tz = datetime.now().astimezone().tzinfo


def data_exploration(df: DataFrame|DataFrameGroupBy) -> None:
    """
    A function for exploring the data in the given DataFrame.
    Takes a DataFrame as input and does not return anything.
    """

    print_debugging_function_header(_filename, "data_exploration")
    print("-------------------- head -------------------- ")
    print(df.head(10))
    # print("-------------------- describe -------------------- ")
    # print(df.describe())

    if type(df) is DataFrame:
        print(f"shape: \t\t\t{df.shape}")
        print("-------------------- Columns -------------------- ")
        print(df.columns)
        print("-------------------- indices -------------------- ")
        print(df.index)
    elif type(df) is DataFrameGroupBy:
        pass
        # print("-------------------- groups -------------------- ")
        # print(df.groups)
        # print("-------------------- count -------------------- ")
        # print(df.count())



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
    print_debugging_function_header(_filename, "clean_dataset")

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
        print_debugging_function_header(_filename, "reformat_df_values")
        print_debugging_message("", "")
        print_debugging_message("datatypes", str(df.dtypes))
        print_debugging_message("columns", df.columns)
        print_debugging_message("")


    df['date'] = pd.to_datetime(df['date'], utc=True)
    df['date'] = df['date'].dt.tz_convert("Europe/Berlin")

    return df


def read_mixed_df_from_file(filename):
    if DEBUG_UTILS:
        print_debugging_function_header(_filename, "read_mixed_df_from_file")
    try:
        df = pd.read_json(StringIO(load_json_from_file(filename)))
    except Exception as e:
        print_debugging_function_header(_filename, "read_mixed_df_from_file")
        handle_exception("Data_handler.py read_mixed_df_from_file", e)
        df = DataFrame()
    else:
        df["date"] = pd.to_datetime(df["date"], unit="s")
        df["date"] = df["date"].dt.tz_localize("UTC").dt.tz_convert(local_tz)
    return df
