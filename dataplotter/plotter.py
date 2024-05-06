import os

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from pandas import DataFrame
from pandas.core.groupby import DataFrameGroupBy
from plotly.subplots import make_subplots

from dataplotter.plotly_figure_configs import figure_layout, figure_axes_config
from dataplotter.plotly_gradient_bg import gradient_plot
from exceptionhandler.exception_handler import print_function_info, print_info_message, print_debug_message, \
    print_exception
from utils.constants import DEBUG_PLOTTER
from utils.data_exploration import explore_dataframe

_filename = os.path.basename(__file__)

plt_style = "classic"  # seaborn-v0_8-darkgrid"


# TODO: replace DEBUG_ and print with exceptionhandler/logging

# aliceblue, antiquewhite, aqua, aquamarine, azure,
#             beige, bisque, black, blanchedalmond, blue,
#             blueviolet, brown, burlywood, cadetblue,
#             chartreuse, chocolate, coral, cornflowerblue,
#             cornsilk, crimson, cyan, darkblue, darkcyan,
#             darkgoldenrod, darkgray, darkgrey, darkgreen,
#             darkkhaki, darkmagenta, darkolivegreen, darkorange,
#             darkorchid, darkred, darksalmon, darkseagreen,
#             darkslateblue, darkslategray, darkslategrey,
#             darkturquoise, darkviolet, deeppink, deepskyblue,
#             dimgray, dimgrey, dodgerblue, firebrick,
#             floralwhite, forestgreen, fuchsia, gainsboro,
#             ghostwhite, gold, goldenrod, gray, grey, green,
#             greenyellow, honeydew, hotpink, indianred, indigo,
#             ivory, khaki, lavender, lavenderblush, lawngreen,
#             lemonchiffon, lightblue, lightcoral, lightcyan,
#             lightgoldenrodyellow, lightgray, lightgrey,
#             lightgreen, lightpink, lightsalmon, lightseagreen,
#             lightskyblue, lightslategray, lightslategrey,
#             lightsteelblue, lightyellow, lime, limegreen,
#             linen, magenta, maroon, mediumaquamarine,
#             mediumblue, mediumorchid, mediumpurple,
#             mediumseagreen, mediumslateblue, mediumspringgreen,
#             mediumturquoise, mediumvioletred, midnightblue,
#             mintcream, mistyrose, moccasin, navajowhite, navy,
#             oldlace, olive, olivedrab, orange, orangered,
#             orchid, palegoldenrod, palegreen, paleturquoise,
#             palevioletred, papayawhip, peachpuff, peru, pink,
#             plum, powderblue, purple, red, rosybrown,
#             royalblue, rebeccapurple, saddlebrown, salmon,
#             sandybrown, seagreen, seashell, sienna, silver,
#             skyblue, slateblue, slategray, slategrey, snow,
#             springgreen, steelblue, tan, teal, thistle, tomato,
#             turquoise, violet, wheat, white, whitesmoke,
#             yellow, yellowgreen

plot_bg = "#000033"
paper_bg = "black"
fg_color = "dimgray"

default_tracecolors = ["#1f77b4", "#ff7f0e", "#2ca0"]


def plot_dataframes(group: DataFrameGroupBy, city: str):
    print_function_info(_filename, "plot_grouped_df") if DEBUG_PLOTTER else None

    # TODO: move this to dataframe_utils.py
    # group = group.all().dropna(axis=0)  # .fillna(method="ffill").f
    # group = group.all().df.sort_index(ascending=True)  # , inplace=True


    clouds_df: pd.DataFrame = group.get_group("cloud_cover_total")
    clouds_df = clouds_df.dropna(axis=0)
    clouds_df = clouds_df.sort_index(ascending=True)

    wind_df: pd.DataFrame = group.get_group("wind_speed")
    #clouds_df.drop(index="parameter", inplace=True)

    if DEBUG_PLOTTER:
        explore_dataframe(clouds_df)

    timeseries = clouds_df.index.get_level_values('date')

    mosmix = clouds_df["Mosmix"]
    icon = clouds_df["Icon"]
    icon_eu = clouds_df["Icon EU"]
    if DEBUG_PLOTTER:
        print_info_message(f"df.columns:", clouds_df.columns)
        print_info_message(f"df.index:", clouds_df.index)
        print_debug_message("df.head()", clouds_df.head())
        print_debug_message("df.tail()", clouds_df.tail())

        # #print_debug_message(
        # #    f"{_filename} - _plot_with_px - timeseries", timeseries)
        # print_info_message(f"{df.columns[0]} Values", df[df.columns[0]])
        # print_debug_message(f"{df.columns[-1]} df size:", df[df.columns[-1]].size)
        # print_debug_message(f"Icon Values", df.loc[df.columns[0]])
        # print_debug_message(f"Icon df size:", df.loc[df.columns[0]].size)
        # print_debug_message(f"Icon EU Values", df.loc[df.columns[1]])
        # print_debug_message(f"Icon EU df size:", df.loc[df.columns[1]].size)


    text="mosmix"
    # fig = px.line(df, x=timeseries, y=["Mosmix", "Icon", "Icon EU"])
    print(mosmix.head(5))
    # fig = go.Figure()
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True) #, vertical_spacing=0.0 )
    fig.add_trace(go.Scatter(x=timeseries, y=mosmix, name="Mosmix"), row=1, col=1)
    fig.add_trace(go.Scatter(x=timeseries, y=icon, name="Icon"), row=1, col=1)
    fig.add_trace(go.Scatter(x=timeseries, y=icon_eu, name="Icon EU"), row=1, col=1)

    mosmix = wind_df["Mosmix"]
    icon = wind_df["Icon"]
    icon_eu = wind_df["Icon EU"]

    fig.add_trace(go.Scatter(x=timeseries, y=mosmix, name="Mosmix"), row=2, col=1)
    fig.add_trace(go.Scatter(x=timeseries, y=icon, name="Icon"), row=2, col=1)
    fig.add_trace(go.Scatter(x=timeseries, y=icon_eu, name="Icon EU"), row=2, col=1)

    fig = figure_layout(fig, city, 'Cloud Coverage', "%")
    fig = figure_axes_config(fig)


    # save figure as html
    try:
        fig.write_html(f"templates/{city}-{'Cloud Coverage'}.html")
        # fig.write_html("/")
    except IOError as e:
        print_exception(f"{_filename} - _plot_with_px", e)

    #fig.show()
