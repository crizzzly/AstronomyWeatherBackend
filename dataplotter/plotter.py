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


def plot_dataframes(group: DataFrameGroupBy, city: str):
    print_function_info(_filename, "plot_grouped_df") if DEBUG_PLOTTER else None

    # TODO: move this to dataframe_utils.py

    clouds_df: pd.DataFrame = group.get_group("cloud_cover_total")
    clouds_df = clouds_df.dropna(how='any')
    clouds_df = clouds_df.sort_index(axis=0)  # .sort_index(ascending=True)
    timeseries = clouds_df.index.get_level_values('date')

    wind_df: pd.DataFrame = group.get_group("wind_speed")
    visibility_df: pd.DataFrame = group.get_group("visibility_range")
    temperature_df: pd.DataFrame = group.get_group("temperature_air_mean_200")
    dewpoint_df: pd.DataFrame = group.get_group("temperature_dew_point_mean_200")
    #    humidity_df: pd.DataFrame = group.get_group("relative_humidity")

    if DEBUG_PLOTTER:
        explore_dataframe(clouds_df)
        print_info_message(f"df.columns:", clouds_df.columns)
        print_info_message(f"df.index:", clouds_df.index)
        print_debug_message("df.head()", str(clouds_df.head()))
        print_debug_message("df.tail()", str(clouds_df.tail()))

    fig = make_subplots(
        rows=5,
        cols=1,
        subplot_titles=(
            'Cloud Coverage', 'Wind Speed', 'Temperature And Dew Point',
            'Visibility Range', 'Relative Humidity'),
        shared_xaxes=False
    )

    fig = create_subplot(fig, timeseries, clouds_df, "Cloud Coverage", 1, "%", y_max=110)
    fig = create_subplot(fig, timeseries, wind_df, "Wind Speed", 2, "km/h", y_max=300)
    fig = create_subplot(fig, timeseries, temperature_df, "Temperature", 3, "°C")
    fig = create_subplot(fig, timeseries, dewpoint_df, "Dew Point", 4, "°C", line_style="dash", y_max=300)
    fig = create_subplot(fig, timeseries, visibility_df, "Visibility Range", 5, "m", y_max=100000)
    #fig = create_subplot(fig, timeseries, humidity_df, "Relative Humidity", 5, "m", y_max=100000)
    fig = figure_layout(fig, city)
    fig = figure_axes_config(fig)

    # save figure as html
    # TODO: Doesnt work when working with stored data
    # TODO: Prob is: City is not set in datafetcher
    try:
        fig.write_html(f"templates/{city}.html")
    except IOError as e:
        print_exception(f"{_filename} - _plot_with_px", e)

    # fig.show()
