#from utils import (PARAMS_OBSERVATION, LAT, LON)


import logging

from wetterdienst import Settings, Period, Parameter
from wetterdienst.provider.dwd.observation import (
    DwdObservationDataset,
    DwdObservationRequest,
    DwdObservationResolution,
)

DISTANCE_TO_STATION = 30.0

log = logging.getLogger()

"""Retrieve temperature data by DWD and filter by sql statement."""
settings = Settings(ts_shape="long", ts_humanize=True, ts_si_units=False)

request = DwdObservationRequest(
    parameter=Parameter.CLOUD_COVER_TOTAL, # [DwdObservationDataset.CLOUD_TYPE],
    resolution=DwdObservationResolution.DAILY,
    # start_date="2024-01-05",
    # end_date="2024-01-17",
    period=Period.RECENT,
    settings=settings,
)

stations = request.filter_by_distance(latlon=(48.8, 9.9), distance=DISTANCE_TO_STATION)

print(stations.df)

for end in stations.df["station_id"]:
    print(end)