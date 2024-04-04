"""
DMO is a new forecast product of the DWD that takes model output and extracts it at known meteorological stations
to produce consumable timeseries.
In opposition to the Mosmix product, DMO is not a statistical postprocessing but a pure extraction of model output.
The DMO product is available for the ICON model in its global (ICON) and regional (ICON-EU) configuration.
For ICON-EU, the DMO product is available in hourly resolution with a lead time of 78 hours.
For ICON, the DMO product is available in hourly resolution with a lead time of 78 hours and
in 3-hourly resolution with a lead time of 168 hours.
"""

from wetterdienst.provider.dwd.dmo import DwdDmoRequest, DwdDmoType, DwdDmoStationGroup
from wetterdienst import Resolution, Period

import pandas as pd
from datetime import datetime as dt
from datetime import timedelta
import pytz

