import math

import matplotlib.pyplot as plt
from matplotlib.figure import Figure
# import matplotlib.dates as mdates
import plotly.express as px
from pandas import DataFrame

from utils.constants import DEBUG_PLOTTER

plt_style = "classic"  # seaborn-v0_8-darkgrid"


# def plot_forecast_dataset(df: DataFrame):
#     clouds, temp, rest = prepare_datasets(df)
#     if DEBUG_PLOTTER:
#         print(f"plot_forecast_datasets: {clouds}\n\n\n")
#         print(f"plot_forecast_datasets: {temp}\n\n\n")
#         print(f"plot_forecast_datasets: {rest}\n\n\n")
#     fig_clouds = plot_dataset(CLOUDS_TITLE, clouds)
#     fig_temp = plot_dataset(TEMP_TITLE, temp)
#     fig_rest = plot_dataset(REST_TITLE, rest)
#
#     plot_with_px(clouds)
#
#     if DEBUG_PLOTTER:
#         fig_temp.show()
#         fig_clouds.show()
#         fig_rest.show()

# TODO: Write only one plot function that plots all relevant data
def plot_with_px(df: DataFrame, name: str):
    timeseries = df.index.get_level_values('date')
    fig = px.line(df, x=timeseries, y=[["mosmix_value", "icon_value", "icon_eu_value"]])
    fig.update_traces(textposition="bottom right")
    fig.write_html(f"{name}.html")
    fig.show()


def prepare_datasets(datasets: dict[str, DataFrame]) -> list[dict[str, DataFrame]]:
    """
    prepare datasets for plotting:
    splits into cloud-values, temperature-values, and wind&visibility values
    :param datasets: dictionary of parameters with forecast-DataFrame for each
    :return: 3 dictionaries, one with cloud-values, one with temperature-values and one with wind&visibility values
    """
    clouds = {}
    temp = {}
    rest = {}
    for name, df in datasets.items():
        print(f"name: {name}") if DEBUG_PLOTTER else None
        if "cloud" in name.lower():
            clouds[name] = df
        elif "temp" in name.lower():
            temp[name] = df
        else:
            rest[name] = df

    if DEBUG_PLOTTER:
        print(f"Clouds: \n{clouds}")
        print(f"Temp: \n{temp}")
        print(f"Rest: \n{rest}")
    return [clouds, temp, rest]


def plot_dataset(title: str, data: dict[str, DataFrame]) -> Figure:
    first_entry = next(iter(data))
    print(f"dict: {data[first_entry]}") if DEBUG_PLOTTER else None
    print(f"dict: {type(data)}") if DEBUG_PLOTTER else None
    print(f"first_entry: {first_entry}") if DEBUG_PLOTTER else None
    xmin = data[first_entry]["date"].min()
    xmax = data[first_entry]["date"].max()

    num_plots = len(data)
    rows = 2
    cols = math.ceil(num_plots / rows)
    print(f"num_plots: {num_plots}, rows: {rows}, cols: {cols}")

    # plt.close()
    plt.style.use(plt_style)
    plt.xlim(xmin, xmax)
    plt.ylim(0, 100)
    fig, axs = plt.subplots(
        nrows=rows, ncols=cols,
        sharex=True,
        sharey=True,
        figsize=(7, 7),
        constrained_layout=True,
    )
    fig.suptitle(title)

    axs = axs.flatten()

    counter = 0
    for name, data_df in data.items():
        ax = axs[counter]
        ax.set_title(str(name))
        ax.plot(data_df["date"], data_df["mosmix_value"], label="Mosmix")
        ax.plot(data_df["date"], data_df["icon_value"], label="Icon")
        ax.plot(data_df["date"], data_df["icon_eu_value"], label="Icon_EU")
        ax.legend(loc="lower left")
        counter += 1

    try:
        plt.savefig(f"../figures/{title}.png")
    except FileNotFoundError as e:
        print("Error in plotter.py - prepare_datasets")
        print(e.errno)

    return fig
