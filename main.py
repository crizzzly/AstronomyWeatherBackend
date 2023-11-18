from weatherdata import DataHandler
import dataplotter

DF_LENGTH = 78
TEST = True
MOSMIX = "mosmix_fore"
ICON = "icon"
ICON_EU = "icon_eu"


def main():
    data_handler = DataHandler()

    wd_dict = data_handler.get_latest_weather_datasets()
    dataplotter.plot_dataframes(wd_dict)

    # print(cloud_cover_total)
    # print(f"observation: \n{observation}")





if __name__ == '__main__':
    main()