import pandas as pd
import logging

from dataplotter.background_figure import get_background_figure

logger = logging.getLogger("exceptionhandler")
filepath = "../figures/plotly_gradient_bg.html"

bg_color = f'rgba(0, 0, 10, 1)'



def gradient_plot():
    fig = get_background_figure()

    # Customize layout
    fig.update_layout(
        title='Day-Night View',
        xaxis_title='Time',
        yaxis_title='Value',
        showlegend=True,
        plot_bgcolor=bg_color,
        paper_bgcolor=bg_color,
        # fgcolor=bg_color,
        xaxis=dict(showgrid=False, zeroline=False),
        yaxis=dict(showgrid=False, zeroline=False),
        # barmode='overlay',
        bargroupgap=0,
        bargap=0,

        # width=1200,
        # height=400
    )

    # Show the plot
    # fig.show()

    try:
        fig.write_html(filepath)
    except IOError:
        logging.error("plotly gradient.py", "failed to write file")
    finally:
        logging.info("plotly gradient.py", "writing file to disc successful")



if __name__ == '__main__':
    gradient_plot()



# fig.update_layout(
#         title='Day-Night Gradient Background',
#         xaxis_title='Time',
#         yaxis_title='Value',
#         showlegend=False,
#         xaxis=dict(showgrid=False, zeroline=False),
#         yaxis=dict(showgrid=False, zeroline=False),
#         barmode='overlay',
#         bargroupgap=0,
#         bargap=0,
#         width=1200,
#         height=400,
#         # Increase bar width
#         xaxis_range=[df['Time'].min() - pd.Timedelta('1h'), df['Time'].max() + pd.Timedelta('1h')],
#         # Adjust alpha color
#         # paper_bgcolor='rgba(0,0,0,0)',
#         # plot_bgcolor='rgba(0,0,0,0)',
#         # Remove gridlines
#         xaxis_showgrid=False,
#         yaxis_showgrid=False,
#         grid=dict(
#             rows=1,
#             columns=1,
#             pattern='independent',
#     ))

#
# def gradient_plot():
#     # styling variable
#     bar_alpha = 0.8
#     # Sample data
#     # Let's assume we have hourly data for a week
#     # For demonstration, I'm just using random values
#     hours = pd.date_range(start='2024-04-01', end='2024-04-08', freq='h')
#     values = [0.5] * len(hours)  # Sample values
#
#     # Create a DataFrame
#     df = pd.DataFrame({'Time': hours, 'Value': values})
#
#     # Function to determine if it's night or day
#     def is_night(hour):
#         # TODO: use astronomical module instead
#         return 1 if hour < 7 or hour >= 19 else 0  # Assuming night is from 7 PM to 6 AM
#
#     # Assign colors based on night or day
#     # colors = ['blue' if is_night(hour.hour) else 'orange' for hour in df['Time']]
#     colors = [f'rgba(0, 0, 100, {bar_alpha})' if is_night(hour.hour) else f'rgba(0, 0, 255, {bar_alpha})' for hour in
#               df['Time']]
#
#     # Split the data into night and day segments
#     night_values = df[df['Time'].apply(lambda x: is_night(x.hour))]
#     day_values = df[~df['Time'].apply(lambda x: is_night(x.hour))]
#
#     # Create traces for night and day segments
#     night_trace = go.Scatter(
#         x=night_values['Time'],
#         y=night_values['Value'],
#         fill='tozeroy',  # Fill area below the trace
#         fillcolor='rgba(0, 0, 100, 0.5)',  # Dark blue for night
#         line=dict(color='rgba(0, 0, 0, 0)'),  # Hide line
#         name='Night'
#     )
#
#     day_trace = go.Scatter(
#         x=day_values['Time'],
#         y=day_values['Value'],
#         fill='tozeroy',  # Fill area below the trace
#         fillcolor='rgba(0, 0, 255, 0.5)',  # Middle blue for day
#         line=dict(color='rgba(0, 0, 0, 0)'),  # Hide line
#         name='Day'
#     )
#
#     # Create the bar chart
#     fig = go.Figure(go.Bar(
#         fig=go.figure([night_trace, day_trace])
#         # x=df['Time'],
#         # y=df['Value'],
#         # marker_color=colors,
#         # width=60 * 60 * 1000,  # Set width of bars to one hour (in milliseconds)
#     ))
#
#     # TODO: remove grid, increase bar with, set alpha to 90-97%
#     # Remove grid and increase bar width
#
#     try:
#         fig.write_html("gradient_bg.html")
#     except IOError:
#         logging.error("plotly gradient.py", "failed to write file")
#     else:
#         logging.info("plotly gradient.py", "writing file to disc successful")
#
#     # Show the plot
#     fig.show()