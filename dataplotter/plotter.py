import os

import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import matplotlib.dates as mdates
import plotly.express as px
from pandas import DataFrame

_filename = os.path.basename(__file__)

plt_style = "classic"  # seaborn-v0_8-darkgrid"

# TODO: replace DEBUG_ and print with exceptionhandler/logging


# TODO: Write only one plot function that plots all relevant data
def plot_with_px(df: DataFrame, name: str, city: str):
    timeseries = df.index.get_level_values('date')
    fig = px.line(df, x=timeseries, y=[["mosmix_value", "icon_value", "icon_eu_value"]])
    fig.update_layout(title=f"{city} - {name}")
    fig.update_traces(textposition="bottom right")
    fig.write_html(f"{name}.html")
    fig.show()
