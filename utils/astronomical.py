# https://astral.readthedocs.io/en/latest/
from datetime import datetime
from typing import List, Dict

import pytz
from astral import LocationInfo
from _datetime import datetime, timedelta, timezone, tzinfo
from astral.sun import sun
from utils.constants_weatherdata import LAT, LON

my_tz = "Europe/Berlin"


def add_timedelta_to_current_time(hours: float) -> datetime:
    return datetime.now(tz=pytz.timezone(my_tz)) + timedelta(hours=hours)


def get_sun_info_from_location(lat=LAT, lon=LON, tz=my_tz, date=datetime.now(), days=1) -> list[dict[str, datetime]]:
    """
    get local times of sunrise, sunset, dawn, dusk for the next days from astral package
    :param lat: latitude of location in int
    :param lon: longitude of location in int
    :param tz: timezone as string
    :param date: datetime object, default is now
    :param days: number of days to get sun information for
    :return: dict[str, datetime] containing Dawn, Sunrise, Sunset and Dusk
    """
    city = LocationInfo(timezone=tz, latitude=lat, longitude=lon)
    sun_info = []

    for i in range(0, days):
        s = sun(city.observer, date=date+timedelta(days=i))
        dusk = s['dusk'].replace(tzinfo=pytz.utc)
        dawn = s['dawn'].replace(tzinfo=pytz.utc)
        dusk = dusk.astimezone(tz=pytz.timezone(my_tz))
        dawn = dawn.astimezone(tz=pytz.timezone(my_tz))
        dd = {
            "dusk": dusk,
            "dawn": dawn
        }
        sun_info.append(dd)


    return sun_info


if __name__ == '__main__':
    sun_info_home = get_sun_info_from_location()
