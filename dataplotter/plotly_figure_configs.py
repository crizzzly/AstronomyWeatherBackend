import pandas as pd
import plotly.graph_objects as go
from plotly.graph_objs import Figure

from utils.color_constants import PLOT_BG_COLOR, PAPER_BG_COLOR, FG_COLOR


def _create_trace(timeseries: pd.Series, y: pd.Series, model_name: str, parameter_name: str, ) -> go.Scatter:
    """
        This function creates a Scatter trace for a given timeseries, y-values, model name, and parameter name.

        Parameters:
        timeseries (pd.Series): The timeseries data for the x-axis.
        y (pd.Series): The y-values for the scatter trace.
        model_name (str): The name of the model.
        parameter_name (str): The name of the parameter.

        Returns:
        go.Scatter: A Scatter trace object with the specified properties.
        """
    fig = go.Scatter(
        x=timeseries,
        y=y,
        name=model_name,
        legendgroup=parameter_name,
        legendgrouptitle=dict(text=parameter_name),
    )

    return fig


def create_subplot(
        fig: go.Figure,
        timeseries: pd.Series,
        df: pd.DataFrame,
        parameter_name: str,
        row: int,
        ticksuffix: str,
) -> Figure:
    """
        This function creates a subplot for a given figure, timeseries, dataframe, parameter name, row number, and tick suffix.
        It adds traces for Mosmix, Icon, and Icon EU models to the figure, and configures the y-axis.

        Parameters:
        fig (go.Figure): The figure to which the subplot will be added.
        timeseries (pd.Series): The timeseries data for the x-axis.
        df (pd.DataFrame): The dataframe containing the model data.
        parameter_name (str): The name of the parameter.
        row (int): The row number for the subplot.
        ticksuffix (str): The suffix for the y-axis ticks.

        Returns:
        go.Figure: The updated figure with the added subplot.
        """
    mosmix = df["Mosmix"]
    icon = df["Icon"]
    icon_eu = df["Icon EU"]

    fig.add_trace(
        _create_trace(timeseries, mosmix, "Mosmix", parameter_name),
        row=row, col=1
    )
    fig.add_trace(
        _create_trace(timeseries, icon, "Icon", parameter_name),
        row=row, col=1
    )
    fig.add_trace(
        _create_trace(timeseries, icon_eu, "Icon EU", parameter_name),
        row=row, col=1
    )

    fig.update_yaxes(
        showgrid=True,
        gridcolor=FG_COLOR,
        zeroline=False,
        maxallowed=110,
        ticksuffix=ticksuffix,
        row=2, col=1
    )

    return fig




def figure_layout(fig: go.Figure, city: str):
    fig.update_layout(
            title=dict(
                text=f"{city}",
                x=0.5,
            ),
            plot_bgcolor=PLOT_BG_COLOR
        ,
            paper_bgcolor=PAPER_BG_COLOR,
            font_color=FG_COLOR,
            font_size=10,
            legend=dict(title="Model"),
            legend_title=dict(side="top center"),
            hovermode="x unified"
        )
    return fig


def figure_axes_config(fig: go.Figure) -> go.Figure:
    fig.update_xaxes(
        minor=dict(
        ),
        labelalias="Date",
        #tickformat="%H:%M",
        tickangle=30,

        ticklabelmode="period",
        #Determines where tick labels are drawn with respect to
            # their corresponding ticks and grid lines. Only has an
            # effect for axes of `type` "date" When set to "period",
            # tick labels are drawn in the middle of the period
            # between ticks.
        ticklabelposition="outside top",
    )
    fig.update_traces(
        textposition="top center",

    )

    return fig
