import plotly.graph_objects as go

from utils.color_constants import PLOT_BG_COLOR, PAPER_BG_COLOR, FG_COLOR


def figure_layout(fig: go.Figure, city: str, value_name: str, ticksuffix: str):
    fig.update_layout(
            title=dict(
                text=f"{city} - {value_name}",
                x=0.5,
            ),
            plot_bgcolor=PLOT_BG_COLOR
        ,
            paper_bgcolor=PAPER_BG_COLOR,
            font_color=FG_COLOR,
            font_size=10,
            legend=dict(title="Model"),
            legend_title=dict(side="top center"),
            xaxis=dict(
                title="",
                showgrid=True,
                gridcolor=FG_COLOR,
                zeroline=False,
                type="date",
            ),
            yaxis=dict(
                title= value_name,# "Cloud Coverage",
                showgrid=True,
                gridcolor=FG_COLOR,
                zeroline=False,
                maxallowed=110,
                ticksuffix=ticksuffix,
            ),
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
