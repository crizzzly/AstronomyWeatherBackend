import os

from datetime import datetime
from pprint import pprint

import pandas as pd
import pytz
from wetterdienst import Period  #, Parameter
from wetterdienst.provider.dwd.dmo import DwdDmoType, DwdDmoRequest
from wetterdienst.provider.dwd.mosmix import DwdMosmixRequest, DwdMosmixType

from utils.constants import DEBUG_DWD_FETCHER, FORECAST_FROM_FILE
from utils.constants_weatherdata import PARAMS_MOSMIX, LAT, LON, DISTANCE_TO_STATION
from exceptionhandler.exception_handler import print_function_info, \
    print_debug_message, print_error_message
from utils.file_utils import save_json_to_file, load_json_from_file

# TODO: MapWithoutReturnDtypeWarning: Calling `map_elements` without specifying `return_dtype` can lead to
#  unpredictable results. Specify `return_dtype` to silence this warning.
#   df = df.with_columns(

_filename = os.path.basename(__file__)


class DwdDataFetcher:
    """"
    Dwd Data Fetcher for Mosmix, Icon, Icon EU and Observation data
    searches for closest weather station first
    returns forecast/observation weatherdata for closest weather station
    """

    def __init__(self):
        self.mosmix_stations: DwdMosmixRequest  # = None
        self.icon_stations = None
        self.icon_eu_stations = None
        self.local_timezone = pytz.timezone("Europe/Berlin")

        self.time_of_data: datetime
        self.station_id: str = "None"
        self.city: str = "None"

        self._init_forecast_stations()

    def _init_forecast_stations(self):
        # TODO: Catch exceptions
        if not FORECAST_FROM_FILE:
            self.mosmix_stations = DwdMosmixRequest(
                parameter=PARAMS_MOSMIX,
                mosmix_type=DwdMosmixType.LARGE
            )
            self.icon_stations = DwdDmoRequest(
                parameter=PARAMS_MOSMIX,
                station_group="single_stations",
                dmo_type=DwdDmoType.ICON,
            )
            self.icon_eu_stations = DwdDmoRequest(
                parameter=PARAMS_MOSMIX,
                station_group="single_stations",
                dmo_type=DwdDmoType.ICON_EU,
            )
            save_json_to_file("mosmix_stations", self.mosmix_stations.all().df.to_pandas())
            save_json_to_file("icon_stations", self.icon_stations.all().df.to_pandas())
            save_json_to_file("icon_eu_stations", self.icon_eu_stations.all().df.to_pandas())
            
        else:
            self.mosmix_stations = pd.read_json(load_json_from_file("mosmix_stations"))
            self.icon_stations = pd.read_json(load_json_from_file("icon_stations"))
            self.icon_eu_stations = pd.read_json(load_json_from_file("icon_eu_stations"))



    def get_icon_forecast(self, lat=LAT, lon=LON):
        print_function_info(_filename, "getting df_icon forecast") if DEBUG_DWD_FETCHER else None
        return self._get_data_from_closest_station(self.icon_stations, lat, lon)

    def get_icon_eu_forecast(self, lat=LAT, lon=LON):
        print_function_info(_filename, "getting icon_eu forecast") if DEBUG_DWD_FETCHER else None

        return self._get_data_from_closest_station(self.icon_eu_stations, lat, lon)

    def get_mosmix_forecast(self, lat=LAT, lon=LON):
        """
        returns the closest station
        :param lon:
        :param lat:
        :return: closest station as df, containing one row with lists of forecast data
        """
        print_function_info(_filename, "getting df_mosmix forecast") if DEBUG_DWD_FETCHER else None

        return self._get_data_from_closest_station(self.mosmix_stations, lat, lon)

    def _get_data_from_closest_station(self, stations, lat, lon) -> dict[str, pd.DataFrame]:
        """
        Returns only data from the closest weather station based on given lat and lon.
        Filters the stations based on distance, retrieves data from the two closest stations,
        converts the Values-Result of those station data to Pandas DataFrame
        returns the data from either the first or second station depending on the station ID.

        :param stations: Polaris DataFrame containing StationResult from dwd data.
        :param lat: Latitude of the location.
        :param lon: Longitude of the location.
        :return: dictionary containing the city name (str) and Pandas DataFrame from the closest station.
        """

        # TODO: GET FUCKING RID OF FOLLOWING WARNING:
        # /Users/cr/Programming/PyCharm/wetterdienst_api/venv/lib/python3.11/site-packages/wetterdienst/provider/dwd/dmo/api.py:1288:
        # MapWithoutReturnDtypeWarning: Calling `map_elements` without specifying `return_dtype` can lead to
        # unpredictable results. Specify `return_dtype` to silence this warning.
        #   df = df.with_columns( ...
        if DEBUG_DWD_FETCHER:
            print_function_info(_filename, "_get_data_from_closest_station")
            print_debug_message(stations)

        i = 0
        while True:
            try:
                closest_stations = stations.all().stations.filter_by_distance(
                    latlon=(lat, lon),
                    distance=DISTANCE_TO_STATION,
                    unit="km"
                )
            except FileNotFoundError as e:
                text = f"Download attempt {i+1} failed. \n"
                text += "Trying again ...\n"

                print_error_message(_filename, text + str(e))
            else:
                break

        if DEBUG_DWD_FETCHER:
            print_debug_message(f"closest stations:")
            pprint(closest_stations)
            print_debug_message(f"closest stations values:")
            pprint(closest_stations.parameter)

        first_station_id = closest_stations.df.row(0)[0]
        second_station_id = closest_stations.df.row(1)[0]
        first_station = stations.filter_by_station_id(station_id=[first_station_id])
        second_station = stations.filter_by_station_id(station_id=[second_station_id])

        # convert polars to pandas
        values1 = first_station.values.all().df.to_pandas()
        city1 = first_station.df["name"][0].title()
        values2 = second_station.values.all().df.to_pandas()
        city2 = second_station.df["name"][0].title()

        if DEBUG_DWD_FETCHER:
            print_function_info(_filename, "_get_data_from_closest_station")
            print_debug_message("\n\n")
            print_debug_message("first station.type", type(values1))
            print_debug_message("first station.value", values1)
            print_debug_message("first:", city1[0])
            pprint(first_station)
            print_debug_message("second station.type", type(values2))
            print_debug_message("second station.value", values2)
            print_debug_message("second:", city2[0])
            pprint(second_station)

        # TODO: Check if really necessary. Both stations should receive same values!
        x_in_first_id = True if "X" in first_station_id else False
        print(f"X in ID1: {x_in_first_id}") if DEBUG_DWD_FETCHER else None

        if "X" in first_station_id:
            print(f"returning second station: {values2}") if DEBUG_DWD_FETCHER else None
            self.city = city2
            return values2
        else:
            print(f"returning first station: {values1}\ncols: {values1.columns}") if DEBUG_DWD_FETCHER else None
            self.city = city1
            return values1


if __name__ == '__main__':
    dwd_data_fetcher = DwdDataFetcher()
    pprint(dwd_data_fetcher.get_mosmix_forecast())
