import os

# import matplotlib.pyplot as plt
# from matplotlib.figure import Figure
# import matplotlib.dates as mdates
import plotly.express as px
from pandas import DataFrame

from utils.dataframe_utils import explore_dataframe_via_terminal

_filename = os.path.basename(__file__)

plt_style = "classic"  # seaborn-v0_8-darkgrid"

# TODO: replace DEBUG_ and print with exceptionhandler/logging


# TODO: Write only one plot function that plots all relevant data


def plot_df_dict(df_dict: dict[str, DataFrame], city: str):

    df = df_dict["Cloud Coverage"]
    df.reset_index(inplace=True)
    _plot_with_px(df, "Cloud Coverage", city)


def _plot_with_px(df: DataFrame, value_name:str, city: str):
    print("----------------------------- Plotting -----------------------------")
    explore_dataframe_via_terminal(df)
    timeseries = df.index.get_level_values('date')
    fig = px.line(df, x=timeseries, y=[["mosmix_value", "icon_value", "icon_eu_value"]])
    fig.update_layout(title=f"{city} - {value_name}")
    fig.update_traces(textposition="bottom right")
    fig.write_html(f"{value_name}.html")
    fig.show()
