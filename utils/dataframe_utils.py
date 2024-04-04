import os
from datetime import datetime
from io import StringIO

import pandas as pd
from pandas import DataFrame

from exceptionhandler.exception_handler import handle_standard_exception
from utils.constants import DEBUG_DF_UTILS, DEBUG_UTILS
from utils.debugging_outputs import print_function_header
from utils.file_utils import load_json_from_file

_filename = os.path.basename(__file__)
local_tz = datetime.now().astimezone().tzinfo


def data_exploration(df: DataFrame) -> None:
    """
    A function for exploring the data in the given DataFrame.
    Takes a DataFrame as input and does not return anything.
    """

    print(f"{datetime.now()} - dataframe_utils - data_exploration") if DEBUG_DF_UTILS else None

    print(f"shape\t\t\t{df.shape}")
    print("Columns")
    print(df.columns)
    print("values")
    print(df.values)


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
    print("----------------------------------------------------------------")
    print(f"{datetime.now()} - dataframe_utils.py - clean_dataset")
    print("----------------------------------------------------------------")

    if DEBUG_DF_UTILS:
        print(f"dataset")
        print(df)

    name = df.loc[['station_id'][0]]


    df.drop(['quality', 'dataset'], axis=1, inplace=True)  # , 'station_id'
    df.dropna(inplace=True)

    if DEBUG_DF_UTILS:
        print("datatypes before cleaning")
        print(df.dtypes)

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
        print("----------------------------------------------------------------")
        print(f"{datetime.now()} - dataframe_utils - reformat_df_values")
        print("----------------------------------------------------------------")
        print("")
        print(f"datatypes: {df.dtypes}")
        print(f"columns: {df.columns}")
        print("")


    df['date'] = pd.to_datetime(df['date'], utc=True)
    df['date'] = df['date'].dt.tz_convert("Europe/Berlin")

    return df


def read_mixed_df_from_file(filename):
    if DEBUG_UTILS:
        print_function_header(_filename, "read_mixed_df_from_file")


    try:
        df = pd.read_json(StringIO(load_json_from_file(filename)))
    except Exception as e:
        print_function_header(_filename, "read_mixed_df_from_file")
        handle_standard_exception("Data_handler.py read_mixed_df_from_file", e)
        df = DataFrame()
    else:
        df["date"] = pd.to_datetime(df["date"], unit="s")
        df["date"] = df["date"].dt.tz_localize("UTC").dt.tz_convert(local_tz)
    return df
