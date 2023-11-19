# https://astral.readthedocs.io/en/latest/

from astral import LocationInfo
from _datetime import datetime, timedelta
from astral.sun import sun
from constants_weatherdata import LAT, LON

my_tz = "Europe/Berlin"


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
    print(city)
    suninfo = []

    for i in range(0, days):
        s = sun(city.observer, date=date+timedelta(days=i))
        suninfo.append(s)
        print(s.items())
        print("today:")
        print((
            f'Dawn:    {s["dawn"]}\n'
            f'Sunrise: {s["sunrise"]}\n'
            f'Noon:    {s["noon"]}\n'
            f'Sunset:  {s["sunset"]}\n'
            f'Dusk:    {s["dusk"]}\n'
        ))

    return suninfo


if __name__ == '__main__':
    sun_info_home = get_sun_info_from_location()
