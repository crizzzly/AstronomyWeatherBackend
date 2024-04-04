from wetterdienst.core.timeseries.result import StationsResult

from utils.constants import  DEBUG_DWD_FETCHER
from utils.constants_weatherdata import PARAMS_OBSERVATION, PARAMS_MOSMIX, LAT, LON, DISTANCE_TO_STATION
from exceptionhandler.exception_handler import handle_standard_exception

from datetime import datetime, timedelta
from pprint import pprint

import pandas as pd
import pytz
from wetterdienst import Period, Parameter
from wetterdienst.provider.dwd.dmo import DwdDmoType, DwdDmoRequest
from wetterdienst.provider.dwd.mosmix import DwdMosmixRequest, DwdMosmixType
from wetterdienst.provider.dwd.observation import DwdObservationRequest, DwdObservationResolution
# from wetterdienst.provider.dwd.observation.util.parameter. import DwdObservationTime
# from wetterdienst.provider.dwd.observation.values import DwdObservationValue



def _get_data_from_closest_station(stations, lat, lon) -> pd.DataFrame:
    """
    Returns only data from closest weather station based on given lat and lon.
    Filters the stations based on distance, retrieves data from the two closest stations,
    converts the VaulesResult of those station data to Pandas DataFrame
    returns the data from either the first or second station depending on the station ID.

    :param stations: Polaris DataFrame containing StationResult from dwd data.
    :param lat: Latitude of the location.
    :param lon: Longitude of the location.
    :return: Pandas DataFrame from the closest station.
    """


    print(f"{datetime.now()} - getting closest station") if DEBUG_DWD_FETCHER else None
    print(stations)
    closest_stations = stations.all().stations.filter_by_distance(
        latlon=(lat, lon),
        distance=DISTANCE_TO_STATION,
        unit="km"
    )
    if DEBUG_DWD_FETCHER:
        print(f"dwd_data_fetcher.py - _get_data_from_closest_station()")
        print(f"closest stations:")
        pprint(closest_stations)
        print(f"closest stations values:")
        pprint(closest_stations.parameter)

    first_station_id = closest_stations.df.row(0)[0]
    second_station_id = closest_stations.df.row(1)[0]
    first_station = stations.filter_by_station_id(station_id=[first_station_id])
    second_station = stations.filter_by_station_id(station_id=[second_station_id])

    # convert polars to pandas
    values1 = first_station.values.all().df.to_pandas()
    values2 = second_station.values.all().df.to_pandas()


    if DEBUG_DWD_FETCHER:
        print(f"dwd_data_fetcher.py - _get_data_from_closest_station()")
        print(f"\n\nfirst station.type = {type(values1)}")
        print(f"first station.value = {values1}")
        print("first:")
        pprint(first_station)
        print(f"second station.type = {type(values2)}")
        print(f"second station.value = {values2}")
        print("second:")
        pprint(second_station)


    # TODO: Check if really necessary
    x_in_first_id = True if "X" in first_station_id else False
    print(f"X in ID1: {x_in_first_id}") if DEBUG_DWD_FETCHER else None

    if "X" in first_station_id:
        print(f"returning second station: {values2}") if DEBUG_DWD_FETCHER else None
        return values2
    else:
        print(f"returning first station: {values1}\ncols: {values1.columns}") if DEBUG_DWD_FETCHER else None
        return values1


def _get_observation_data_from_best_station(stations: DwdObservationRequest, lat, lon) -> pd.DataFrame:
    if DEBUG_DWD_FETCHER:
        print(f"{datetime.now()} - dwd_data_fetcher.py - _get_observation_data_from_best_station") if DEBUG_DWD_FETCHER else None
        print(f"{datetime.now()} - getting closest station") if DEBUG_DWD_FETCHER else None
        print(stations.all().df)

    # filter StationsResult by distance
    try:
        closest_stations = stations.filter_by_distance(
            latlon=(lat, lon),
            distance=DISTANCE_TO_STATION,
            unit="km"
        )
        if DEBUG_DWD_FETCHER:
            print(f"closest stations:")
            pprint(closest_stations)
            print(f"closest stations values:")
            pprint(closest_stations.parameter)
    except Exception as e:
        handle_standard_exception("dwd_data_fetcher.py - _get_observation_data_from_best_station", e)
    else:
        first_station_id = closest_stations.df.row(0)[0]
        second_station_id = closest_stations.df.row(1)[0]
        first_station = stations.filter_by_station_id(station_id=[first_station_id])
        second_station = stations.filter_by_station_id(station_id=[second_station_id])

        values1 = first_station.values.all().df.to_pandas()
        values2 = second_station.values.all().df.to_pandas()

        if DEBUG_DWD_FETCHER:
            print(f"\n\nfirst station.type = {type(values1)}")
            print(f"first station.value = {values1}")
            print("first:")
            pprint(first_station)
            print(f"second station.type = {type(values2)}")
            print(f"second station.value = {values2}")
            print("second:")
            pprint(second_station)


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
        self.mosmix_stations = None
        self.icon_stations = None
        self.icon_eu_stations = None
        self.observation_stations = None
        self.local_timezone = pytz.timezone("Europe/Berlin")

        # self._init_observation_stations()
        self._init_forecast_stations()


    def _init_forecast_stations(self):
        self.mosmix_stations = DwdMosmixRequest(
            parameter=self.mosmix_params,
            mosmix_type=DwdMosmixType.LARGE
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


    def _init_observation_stations(self):

        self.observation_stations = DwdObservationRequest(
            parameter=PARAMS_OBSERVATION,
            resolution=DwdObservationResolution.HOURLY,
            period=Period.RECENT,
        )


    def get_icon_forecast(self, lat=LAT, lon=LON):
        print(f"{datetime.now()} - getting icon forecast") if DEBUG_DWD_FETCHER else None
        return _get_data_from_closest_station(self.icon_stations, lat, lon)


    def get_icon_eu_forecast(self, lat=LAT, lon=LON):
        print(f"{datetime.now()} - getting icon_eu forecast") if DEBUG_DWD_FETCHER else None

        return _get_data_from_closest_station(self.icon_eu_stations, lat, lon)


    def get_mosmix_forecast(self, lat=LAT, lon=LON):
        """
        returns the closest station
        :param lon:
        :param lat:
        :return: closest station as df, containing one row with lists of forecast data
        """
        print(f"{datetime.now()} - getting mosmix forecast") if DEBUG_DWD_FETCHER else None

        return _get_data_from_closest_station(self.mosmix_stations, lat, lon)


# TODO: using observation data? really needed?
    def get_observation(self, lat=LAT, lon=LON):
        print(f"{datetime.now()} - getting observation") if DEBUG_DWD_FETCHER else None

        return _get_observation_data_from_best_station(self.observation_stations, lat, lon)
        # pprint(station.values.all().df)
        # return get_forecast_per_day_as_list(self.observation_stations, self.observation_params)




if __name__ == '__main__':
    dwd_data_fetcher = DwdDataFetcher()
    pprint(dwd_data_fetcher.get_mosmix_forecast())

