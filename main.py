from weatherdata import DataHandler

DF_LENGTH = 78
TEST = True
MOSMIX = "mosmix_fore"
ICON = "icon"
ICON_EU = "icon_eu"


def main():
    data_handler = DataHandler()
    data_handler.get_weather_data()
