from wetterdienst.core.timeseries.result import StationsResult

from utils.constants_weatherdata import PARAMS_OBSERVATION, FORECAST_PARAMS, LAT, LON, DISTANCE_TO_STATION
from utils.constants import DEBUG_DWD_FETCHER

from datetime import datetime, timedelta
from pprint import pprint

import pandas as pd
import pytz
from wetterdienst import Period, Parameter
from wetterdienst.provider.dwd.observation import DwdObservationRequest, DwdObservationResolution
# from wetterdienst.provider.dwd.observation.util.parameter. import DwdObservati


