import plotly.graph_objects as go
import pandas as pd
from pandas import DataFrame

bar_alpha = 0.9
color_night = f'rgba(0, 0, 20, {bar_alpha})'
color_day = f'rgba(0, 0, 80, {bar_alpha})'
bg_color = f'rgba(0, 0, 10, 1)'
line_transparent = dict(color='rgba(0, 0, 0, 0)')

# Sample data
# TODO: replace with real data
hours = pd.date_range(start='2024-04-01', end='2024-04-03', freq='h')
values = [0.5] * len(hours)  # Sample values

# TODO: exclude df creation
df = pd.DataFrame({'Time': hours, 'Value': values})


def is_night(hour):
    return 1 if hour < 7 or hour >= 19 else 0  # Assuming night is from 7 PM to 6 AM


def get_background_figure() -> go.Figure:
    # Add a column to DataFrame to indicate night or day
    df['Night'] = df['Time'].apply(lambda x: is_night(x.hour))

    # Split the data into night and day segments
    night_values = df[df['Night'] == 1]
    day_values = df[df['Night'] == 0]

    # Create traces for night and day segments
    night_trace = go.Scatter(
        x=night_values['Time'],
        y=night_values['Value'],
        fill='tozeroy',
        # Fill area below the trace
        fillcolor=color_night,
        line=line_transparent,  # Hide line
        name='Night')

    day_trace = go.Scatter(
        x=day_values['Time'],
        y=day_values['Value'],
        fill='tozeroy',  # Fill area in height completely
        fillcolor=color_day,  # Middle blue for day
        line=line_transparent,  # Hide line
        name='Day',
    )

    return go.Figure([night_trace, day_trace])
