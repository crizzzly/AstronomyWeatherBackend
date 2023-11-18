import matplotlib.pyplot as plt
from polars import DataFrame


def plot_dataframe(df: DataFrame):

    fig, ax = plt.subplots()
    ax.plot(df["date"], df["mosmix_value"])
    ax.plot(df["date"], df["icon_value"])
    ax.plot(df["date"], df["icon_eu_value"])

    plt.show()
