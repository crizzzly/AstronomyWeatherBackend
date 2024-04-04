import os

# import matplotlib.pyplot as plt
# from matplotlib.figure import Figure
# import matplotlib.dates as mdates
import plotly.express as px
from pandas import DataFrame

from exceptionhandler.exception_handler import print_function_info, print_info_message
from utils.constants import DEBUG_PLOTTER
from utils.data_exploration import explore_dataframe

_filename = os.path.basename(__file__)

plt_style = "classic"  # seaborn-v0_8-darkgrid"

# TODO: replace DEBUG_ and print with exceptionhandler/logging


# TODO: Write only one plot function that plots all relevant data


def plot_df_dict(df_dict: dict[str, DataFrame], city: str):
    df = df_dict["Cloud Coverage"]
    _plot_with_px(df, "Cloud Coverage", city)


def _plot_with_px(df: DataFrame, value_name:str, city: str):
    print_function_info(_filename, "_plot_with_px")  if DEBUG_PLOTTER else None

    explore_dataframe(df) if DEBUG_PLOTTER else None

    if DEBUG_PLOTTER:
        print_info_message(f"df.columns:\n {df.columns}")
        print_info_message((f"df.index:\n {df.index}"))

    try:
        timeseries = df.loc["date"]  # .index.get_level_values('date')
    except Exception as e:
        print(e)
        # try:
            # timeseries = df.inde
    fig = px.line(df, x=timeseries, y=[["mosmix_value", "icon_value", "icon_eu_value"]])
    fig.update_layout(title=f"{city} - {value_name}")
    fig.update_traces(textposition="bottom right")
    fig.write_html(f"{value_name}.html")
    fig.show()
