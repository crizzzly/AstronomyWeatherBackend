from weatherdata.data_handler import DataHandler

DF_LENGTH = 78
TEST = True
MOSMIX = "mosmix_fore"
ICON = "icon"
ICON_EU = "icon_eu"


def main():
    data_handler = DataHandler()
    data_handler.load_new_dataset()
#    data_handler.get_weather()
