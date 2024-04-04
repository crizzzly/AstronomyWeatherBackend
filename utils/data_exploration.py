import os

from pandas import DataFrame
from pandas.core.groupby import DataFrameGroupBy

from exceptionhandler.exception_handler import print_function_info, print_debugging_message

_filename = os.path.basename(__file__)


def debug_dataset(action_str: str, group_df: DataFrame | DataFrameGroupBy):
    print_function_info(_filename, action_str)
    msg = ""
    print(f"================================ {action_str} ================================")
    if type(group_df) is DataFrameGroupBy:
        msg += f"columns in group: {group_df.get_group('cloud_cover_total').columns}\n"
    elif type(group_df) is DataFrame:
        msg += f"columns: {group_df.columns}\n"
    print_debugging_message(msg)


def explore_dataframe(df: DataFrame):
    """
    A function for exploring the data in the given DataFrame.
    Takes a DataFrame as input and does not return anything.
    """

    print_function_info(_filename, "explore_dataframe")
    msg = f"shape: {df.shape}\n"
    msg += f"\ndtypes: {df.dtypes}\n"
    # msg += f"\nindex: {df.index}\n"
    msg += f"\ncolumns: {df.columns}\n\n"
    msg += f"head: \n{df.head(10)}\n\n"
    msg += f"describe: \n{df.describe()}"
    print_debugging_message(msg)


def print_groups(grouped_df: DataFrameGroupBy):  #
    print_function_info(_filename, "print_groups")
    msg = f"type: {grouped_df.type}\n"
    msg += f"\ngroups: {grouped_df.groups}\n\n"


def explore_group(df: DataFrame | DataFrameGroupBy) -> None:
    """
    A function for exploring the data in the given DataFrame.
    Takes a DataFrame as input and does not return anything.
    """
    print_function_info(_filename, "explore_group")

    msg = f"head: \n{df.head(10)}\n"
    msg += f"description: \n{df.description}\n"

    if type(df) is DataFrame:
        msg += f"shape: {df.shape}\n"
        msg += f"columns: {df.columns}\n"

    elif type(df) is DataFrameGroupBy:
        msg += f"columns: {df.get_group('cloud_cover_total').columns}\n"
        msg += f"count: \n{df.get_group('cloud_cover_')}\n"

    print_debugging_message(msg)

