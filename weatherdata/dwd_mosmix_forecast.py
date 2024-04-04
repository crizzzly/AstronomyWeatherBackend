from wetterdienst.provider.dwd.mosmix.api import DwdMosmixRequest, DwdMosmixType, DwdMosmixValues
# from wetterdienst import Resolution, Period

import matplotlib.dates as mdates
import plotly.express as px

import pandas as pd

from datetime import datetime as dt
from datetime import timedelta
import pytz

mosmix_params = [
    'cloud_base_convective',
    'cloud_cover_above_7_km',
    'cloud_cover_below_1000_ft',
    'cloud_cover_below_500_ft',
    'cloud_cover_between_2_to_7_km',
    'cloud_cover_effective',
    'cloud_cover_total',
    'temperature_air_max_200',
    'temperature_air_mean_200',
    'temperature_air_min_200',
    'temperature_dew_point_mean_200',
    'visibility_range',
    'wind_direction',
    'wind_speed',
]

temperature_params = [
    'temperature_air_max_200',
    'temperature_air_mean_200',
    'temperature_air_min_200',
    'temperature_dew_point_mean_200',
]

station1_id = "X379"  # "N1038"# "X229" GD obernheim: N1038 10818
station1_name = "Meßstetten"
station2_id = "10818"  # "10818"

add_to_kelvin = -273.15

# Get Data

mosmix_stations = DwdMosmixRequest(
    parameter=mosmix_params,
    mosmix_type=DwdMosmixType.LARGE
)

closest_stations = mosmix_stations.all().stations.filter_by_distance(
    latlon=(48.175521, 8.847180),
    # (48.175521, 8.847180),  # (48.593, 9.498), # 48.5938126,9.4986557 Zainingen, 48.8, 9.9 home
    distance=15.0,
    unit="km"
)
print(closest_stations)  # P0251 N1107 N1038 10818

## get close stations and convert to pd

df_as_list = []

for stat_id in closest_stations.df["station_id"]:
    df = mosmix_stations.filter_by_station_id(stat_id)
    df = df.values.all().df.to_pandas()

    df_as_list.append(df)

valsdf_per_station = df_as_list
# valsdf_per_station


result = mosmix_stations.filter_by_station_id(closest_stations.df["station_id"])
print(result)

values_df = result.values.all().df.to_pandas().drop(["quality", "dataset"], axis=1)
print(values_df)

## data cleanup and conversions
# - drop quality columnn as not always containing numbers
# - convert to local datetime
# - calculate Celcius from Kelvin
# - reduce dataset to 48h

local_tz = pytz.timezone('Europe/Berlin')

now = dt.now()
end_date = now + timedelta(days=2.0)
end_date = end_date.replace(tzinfo=pytz.utc).astimezone(local_tz)

values_df['date'] = values_df['date'].dt.tz_convert("Europe/Berlin")
values_df = values_df.loc[values_df["date"] <= end_date]
print(values_df)

for param in temperature_params:
    values_df.loc[values_df["parameter"] == param, "value"] += add_to_kelvin

print(values_df)

values_df['parameter'].unique()

for df in valsdf_per_station:
    df.drop(axis=1, columns=["quality", "dataset"], inplace=True)

    df['date'] = pd.to_datetime(df['date'], utc=True)
    df['date'] = df['date'].dt.tz_convert("Europe/Berlin")

    # df.loc[df["date"] <= end_date]
    for param in temperature_params:
        df.loc[df["parameter"] == param, "value"] += add_to_kelvin

print(valsdf_per_station[0])

## rearrange dataset

print(values_df)

print(values_df.dtypes)

pivot_df = values_df.pivot(index=['date', 'station_id'], columns='parameter', values='value')
print(pivot_df)

grouped_df = pivot_df.groupby("station_id")
grouped_df.describe()

print(grouped_df.cloud_cover_above_7_km)

df_list = []
station2_name = "Obernheim2"
for df in valsdf_per_station:
    # df.dropna(inplace=True)
    new_df = df.pivot(index=['date', 'station_id'], columns=['parameter'], values='value')  # .reset_index()
    # new_df = new_df.set_index("date")
    df_list.append(new_df)
    # df_per_station.append(new_df)

valsdf_per_station = df_list

pivot_df.head(2)

print(valsdf_per_station[0].index)

### separate temp/cloud/wind data

cloud_params = ['cloud_cover_above_7_km', 'cloud_cover_below_1000_ft',
                'cloud_cover_below_500_ft', 'cloud_cover_between_2_to_7_km',
                'cloud_cover_effective', 'cloud_cover_total']

temp_params = ['temperature_air_max_200',
               'temperature_air_mean_200', 'temperature_air_min_200',
               'temperature_dew_point_mean_200']

wind_params = ['visibility_range', 'wind_direction',
               'wind_speed']

# Show Data


## notebook presentation

pd.options.display.float_format = '{:,.2f}'.format

# Create locators for ticks on the time axis
years = mdates.YearLocator()
months = mdates.MonthLocator()
days = mdates.DayLocator()
hours = mdates.HourLocator(byhour=[8, 18])
min30 = mdates.MinuteLocator(byminute=30)
time_fmt = mdates.DateFormatter('%d')

from pandas.plotting import register_matplotlib_converters

register_matplotlib_converters()

print(valsdf_per_station[0].columns)

## plot cloud coverages

### pyplot

### plotly

values = ['cloud_cover_above_7_km' 'cloud_cover_below_1000_ft'
          'cloud_cover_below_500_ft' 'cloud_cover_between_2_to_7_km'
          'cloud_cover_effective' 'cloud_cover_total' 'temperature_air_max_200'
          'temperature_air_mean_200' 'temperature_air_min_200'
          'temperature_dew_point_mean_200' 'visibility_range' 'wind_direction'
          'wind_speed']

station1 = grouped_df.get_group(station1_id)  # 10836 X229
station2 = grouped_df.get_group(station2_id)  # 10836 X229
print(station1)

timeseries = station1.index.get_level_values('date')

fig = px.line(station1, x=timeseries, y=cloud_params, title=station1_name)  # title=f"{station_id} {param}"
fig.update_traces(textposition="bottom right")
fig.write_html(f"{station1_name}.html")
fig.show()

fig = px.line(station2, x=timeseries, y=cloud_params, title=station2_name)  # title=f"{station_id} {param}"
fig.update_traces(textposition="bottom right")
fig.write_html(f"{station2_name}.html")
fig.show()
