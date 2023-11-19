from pandas import DataFrame

from weatherdata import DataHandler
import dataplotter

DF_LENGTH = 78
TEST = True
MOSMIX = "mosmix_fore"
ICON = "icon"
ICON_EU = "icon_eu"


def main():
    data_handler = DataHandler()

    wd_dict = data_handler.get_weather_data()
    # dataplotter.plot_forecast_datasets(wd_dict["today"])






if __name__ == '__main__':
    main()