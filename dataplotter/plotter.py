import matplotlib.pyplot as plt
from polars import DataFrame


def plot_dataframes(df: dict[str, DataFrame]):
    num_plots = len(df)

    fig, ax = plt.subplots(
        ncols=1,
        nrows=num_plots,
        sharex="row",
        figsize=(200, 600)
    )
    fig.suptitle("Weather Forecast")

    counter = 1

    for name, df in df.items():
        ax = plt.subplot(num_plots, 1, counter)
        ax.set_title(name)
        ax.plot(df["date"], df["mosmix_value"], label="Mosmix")
        ax.plot(df["date"], df["icon_value"], label="Icon")
        ax.plot(df["date"], df["icon_eu_value"], label="Icon_EU")
        ax.legend(loc="lower left")
        counter += 1

    plt.show()
    # ax.set_title('Cloud Coverage')
    # ax.plot(df["date"], df["mosmix_value"], label="Mosmix")
    # ax.plot(df["date"], df["icon_value"], label="Icon")
    # ax.plot(df["date"], df["icon_eu_value"], label="Icon_EU")
    # ax.legend(loc="lower left")


    plt.show()
