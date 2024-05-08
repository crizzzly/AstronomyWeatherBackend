import os

import pandas as pd

from pandas.core.groupby import DataFrameGroupBy
from plotly.subplots import make_subplots

from dataplotter.plotly_figure_configs import create_subplot, figure_layout, figure_axes_config
from exceptionhandler.exception_handler import print_function_info, print_info_message, print_debug_message, \
    print_exception
from utils.constants import DEBUG_PLOTTER
from utils.data_exploration import explore_dataframe

_filename = os.path.basename(__file__)

plt_style = "classic"  # seaborn-v0_8-darkgrid"


# TODO: replace DEBUG_ and print with exceptionhandler/logging


def plot_dataframes(group: DataFrameGroupBy, city: str):
    print_function_info(_filename, "plot_grouped_df") if DEBUG_PLOTTER else None

    # TODO: move this to dataframe_utils.py

    clouds_df: pd.DataFrame = group.get_group("cloud_cover_total")
    clouds_df = clouds_df.dropna(how='any')
    clouds_df = clouds_df.sort_index(axis=0)  # .sort_index(ascending=True)

    wind_df: pd.DataFrame = group.get_group("wind_speed")

    if DEBUG_PLOTTER:
        explore_dataframe(clouds_df)

    timeseries = clouds_df.index.get_level_values('date')

    if DEBUG_PLOTTER:
        print_info_message(f"df.columns:", clouds_df.columns)
        print_info_message(f"df.index:", clouds_df.index)
        print_debug_message("df.head()", clouds_df.head())
        print_debug_message("df.tail()", clouds_df.tail())



    fig = make_subplots(
        rows=2,
        cols=1,
        subplot_titles=('Cloud Coverage', 'Wind Speed'),
        shared_xaxes=True
    )

    fig = create_subplot(fig, timeseries, clouds_df, "Cloud Coverage", 1, "%")
    fig = create_subplot(fig, timeseries, wind_df, "Wind Speed", 2, "m/s")
    fig = figure_layout(fig, city)
    fig = figure_axes_config(fig)



    # save figure as html
    # TODO: Doesnt work when working with stored data
    # TODO: Prob is: City is not set in datafetcher
    try:
        fig.write_html(f"templates/{city}-{'Cloud Coverage'}.html")
    except IOError as e:
        print_exception(f"{_filename} - _plot_with_px", e)

    # fig.show()
