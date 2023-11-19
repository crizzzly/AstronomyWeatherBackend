import json
from datetime import datetime
from pprint import pprint

import pandas as pd
import pytz
from polars import DataFrame
from wetterdienst import Period
from wetterdienst.core.timeseries.result import ValuesResult
from wetterdienst.provider.dwd.dmo import DwdDmoType, DwdDmoRequest
from wetterdienst.provider.dwd.mosmix import DwdMosmixRequest, DwdMosmixType
from wetterdienst.provider.dwd.observation import DwdObservationRequest, DwdObservationResolution

from exceptionhandler import handle_standard_exception
from utils import PARAMS_OBSERVATION, PARAMS_MOSMIX, LAT, LON, DISTANCE_TO_STATION

DEBUG_DWD_FETCHER = True


def get_closest_station(stations, lat, lon):
    print(f"{datetime.now()} - getting closest station") if DEBUG_DWD_FETCHER else None
    print(stations)
    closest_stations = stations.all().stations.filter_by_distance(
        latlon=(lat, lon),
        distance=DISTANCE_TO_STATION,
        unit="km"
    )
    if DEBUG_DWD_FETCHER:
        print(f"closest stations:")
        pprint(closest_stations)
        print(f"closest stations values:")
        pprint(closest_stations.parameter)

    first_station_id = closest_stations.df.row(0)[0]
    second_station_id = closest_stations.df.row(1)[0]
    first_station = stations.filter_by_station_id(station_id=[first_station_id])
    second_station = stations.filter_by_station_id(station_id=[second_station_id])

    if DEBUG_DWD_FETCHER:
        print("first:")
        pprint(first_station)
        print(f"IDs: {first_station_id}, {second_station_id}")
        x_in_first_id = True if "X" in first_station_id else False
        print(f"X in ID1: {x_in_first_id}")

    if "X" in first_station_id:
        print(f"returning second station: {second_station}") if DEBUG_DWD_FETCHER else None
        return second_station
    else:
        print(f"returning first station: {first_station}") if DEBUG_DWD_FETCHER else None
        return first_station


def get_forecast_for_station(df: ValuesResult, params) -> dict[str, pd.DataFrame]:
    print(f"{datetime.now()} - fetching forecast for station") if DEBUG_DWD_FETCHER else None
    values = df.values.all()  #  .df.values.groupby("parameter").all()

    grouped_by_param = values.df.group_by("parameter").all()

    weather_data: dict[str, DataFrame] = {}
    for param in params:
        try:
            filtered_df = grouped_by_param.filter(grouped_by_param['parameter'] == param).drop('parameter')
            weather_data[param] = filtered_df.explode(['date', 'value']).to_pandas()
        except Exception as e:
            handle_standard_exception("get_forecast_for_station", e)

    print(f"{datetime.now()} - weather_data: {weather_data}") if DEBUG_DWD_FETCHER else None

    return weather_data


# def save_to_file(filename: str, weather_data):
#     print(f"{datetime.now()} - saving weather data") if DEBUG_DWD_FETCHER else None
#
#     with open(f"json_data/{filename}.csv", "w") as outfile:
#         json.dump(weather_data, outfile)
#
#

class DwdDataFetcher:
    """"
    Dwd Data Fetcher for Mosmix, Icon, Icon EU and Observation data
    searches for closest weatherstation first
    returns forecast/observation weatherdata for closest weatherstation
    """

    observation_params = PARAMS_OBSERVATION
    mosmix_params = PARAMS_MOSMIX
    icon_params = PARAMS_MOSMIX


    def __init__(self):
        self.local_timezone = pytz.timezone("Europe/Berlin")
        self.mosmix_stations = DwdMosmixRequest(
            parameter=self.mosmix_params,
            mosmix_type=DwdMosmixType.SMALL
        )

        self.icon_stations = DwdDmoRequest(
            parameter=self.icon_params,
            # station_group="single_stations",
            dmo_type=DwdDmoType.ICON,
        )
        self.icon_eu_stations = DwdDmoRequest(
            parameter=self.icon_params,
            # station_group="single_stations",
            dmo_type=DwdDmoType.ICON_EU,
        )

        self.observation_stations = DwdObservationRequest(
            parameter=self.observation_params,
            resolution=DwdObservationResolution.HOURLY,
            period=Period.NOW
        )


    def get_observation(self, lat=LAT, lon=LON):
        print(f"{datetime.now()} - getting observation") if DEBUG_DWD_FETCHER else None

        # station = get_closest_station(self.observation_stations, lat, lon)
        # pprint(station.values.all().df)
        # save_to_file("observation", station.values.all().to_csv())
        return get_forecast_for_station(self.observation_stations, self.observation_params)


    def get_icon_forecast(self, lat=LAT, lon=LON):
        print(f"{datetime.now()} - getting icon forecast") if DEBUG_DWD_FETCHER else None
        station = get_closest_station(self.icon_stations, lat, lon)
        return get_forecast_for_station(station, self.icon_params)


    def get_icon_eu_forecast(self, lat=LAT, lon=LON):
        print(f"{datetime.now()} - getting icon_eu forecast") if DEBUG_DWD_FETCHER else None

        station = get_closest_station(self.icon_eu_stations, lat, lon)
        return get_forecast_for_station(station, self.icon_params)


    def get_mosmix_forecast(self, lat=LAT, lon=LON):
        """
        returns the closest station
        :param lon:
        :param lat:
        :return: closest station as df, containing one row with lists of forecast data
        """
        print(f"{datetime.now()} - getting mosmix forecast") if DEBUG_DWD_FETCHER else None

        closest_stations = get_closest_station(self.mosmix_stations, lat, lon)
        return get_forecast_for_station(closest_stations, self.mosmix_params)



if __name__ == '__main__':
    dwd_data_fetcher = DwdDataFetcher()
    pprint(dwd_data_fetcher.get_mosmix_forecast())