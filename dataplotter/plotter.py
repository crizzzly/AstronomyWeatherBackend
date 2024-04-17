import os

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import plotly.express as px
from pandas import DataFrame
from pandas.core.groupby import DataFrameGroupBy

from dataplotter.plotly_gradient_bg import gradient_plot
from exceptionhandler.exception_handler import print_function_info, print_info_message, print_debug_message, \
    print_exception
from utils.constants import DEBUG_PLOTTER
from utils.data_exploration import explore_dataframe

_filename = os.path.basename(__file__)

plt_style = "classic"  # seaborn-v0_8-darkgrid"


# TODO: replace DEBUG_ and print with exceptionhandler/logging


def plot_grouped_df(group: DataFrameGroupBy, city: str):
    print_function_info(_filename, "plot_grouped_df") if DEBUG_PLOTTER else None
    clouds_df = group.get_group("cloud_cover_total")
    if DEBUG_PLOTTER:
        explore_dataframe(clouds_df)

    # gradient_plot()
    _plot_with_px(clouds_df, "Cloud Coverage", city) if clouds_df is not None else None


def _plot_with_px(df: DataFrame, value_name: str, city: str):
    print_function_info(_filename, "_plot_with_px") if DEBUG_PLOTTER else None
    if DEBUG_PLOTTER:
        print_info_message(f"df.columns:", df.columns)
        print_info_message(f"df.index:", df.index)

    timeseries = df.index.get_level_values('date')
    if DEBUG_PLOTTER:
        print_debug_message(
            f"{_filename} - _plot_with_px - timeseries", timeseries) \
            if DEBUG_PLOTTER else None
        print_info_message("Mosmix Values", df["Mosmix"])
        print_debug_message("Mosmix df size:", df["Mosmix"].size)
        print_debug_message("Icon Values", df["Icon"])
        print_debug_message("Icon df size:", df["Icon"].size)
        print_debug_message("Icon EU Values", df["Icon EU"])
        print_debug_message("Icon EU df size:", df["Icon EU"].size)

    df = df.sort_index(ascending=True)  # , inplace=True
    df = df.fillna(999.9)
    print_debug_message(f"{_filename} - _plot_with_px - df.isna?", df.isna().any())

    fig = px.line(df, x=timeseries, y=["Mosmix", "Icon", "Icon EU"])
    fig.update_layout(title=f"{city} - {value_name}")
    fig.update_traces(textposition="bottom right")

    # save figure as html
    try:
        fig.write_html(f"figures/{city}-{value_name}.html")
        # fig.write_html("/")
    except IOError as e:
        print_exception(f"{_filename} - _plot_with_px", e)

    fig.show()
