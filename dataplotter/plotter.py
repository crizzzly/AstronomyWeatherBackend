import math

import matplotlib.pyplot as plt
from pandas import DataFrame

from utils import TEMP_TITLE, CLOUDS_TITLE, REST_TITLE, DEBUG_PLOTTER

plt_style = "classic"  # seaborn-v0_8-darkgrid"



def plot_forecast_datasets(df: dict[str, DataFrame]):
    clouds, temp, rest = prepare_datasets(df)
    if DEBUG_PLOTTER:
        # print(f"plot_forecast_datasets: {df}\n\n\n")
        print(f"plot_forecast_datasets: {clouds}\n\n\n")
        print(f"plot_forecast_datasets: {temp}\n\n\n")
        print(f"plot_forecast_datasets: {rest}\n\n\n")
    plot_datasets(CLOUDS_TITLE, clouds)
    plot_datasets(TEMP_TITLE, temp)
    plot_datasets(REST_TITLE, rest)


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

    # return_dict = {
    #     "Clouds": clouds,
    #     "Temperature": temp,
    #     "WindVisibility": rest
    # }
    #
    # return return_dict



def plot_datasets(title: str, data: dict[str, DataFrame]):
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

    plt.style.use(plt_style)
    plt.xlim(xmin, xmax)
    plt.ylim(0, 100)
    fig, ax = plt.subplots(
        nrows=rows, ncols=cols,
        sharex=True,
        sharey=True,
        figsize=(7, 7),
        constrained_layout=True,
    )
    fig.suptitle(title)

    counter = 1
    for name, data_df in data.items():
        # ax = fig.subplots(counter)
        ax = plt.subplot(rows, cols, counter)
        ax.set_title(name)
        ax.plot(data_df["mosmix_value"], label="Mosmix")
        ax.plot(data_df["icon_value"], label="Icon")
        ax.plot(data_df["icon_eu_value"], label="Icon_EU")
        ax.legend(loc="lower left")
        counter += 1

    plt.savefig(f"figures/{title}.png")
    plt.show()
