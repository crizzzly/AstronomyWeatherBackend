from weatherdata import DwdDataFetcher

cloud_base_convective = []
cloud_cover_above_7_km = []
cloud_cover_below_1000_ft = []
cloud_cover_below_500_ft = []
cloud_cover_effective = []
cloud_cover_total = []
temperature_air_max_200 = []
temperature_air_min_200 = []
visibility_range = []
wind_speed = []


def main():
    data_fetcher = DwdDataFetcher()
    mosmix_forecast = data_fetcher.get_mosmix_forecast()
    icon_eu_forecast = data_fetcher.get_icon_eu_forecast()
    icon_forecast = data_fetcher.get_icon_forecast()
    observation = data_fetcher.get_observation()
    # observation
    
    append_vals(mosmix_forecast)
    append_vals(icon_forecast)
    append_vals(icon_eu_forecast)



def append_vals(vals_dict):
    cloud_base_convective.append(vals_dict['cloud_base_convective'])
    cloud_cover_above_7_km.append(vals_dict['cloud_cover_above_7_km'])
    cloud_cover_below_1000_ft.append(vals_dict['cloud_cover_below_1000_ft'])
    cloud_cover_below_500_ft.append(vals_dict['cloud_cover_below_500_ft'])
    cloud_cover_effective.append(vals_dict['cloud_cover_effective'])
    cloud_cover_total.append(vals_dict['cloud_cover_total'])
    temperature_air_max_200.append(vals_dict['temperature_air_max_200'])
    temperature_air_min_200.append(vals_dict['temperature_air_min_200'])
    visibility_range.append(vals_dict['visibility_range'])
    wind_speed.append(vals_dict['wind_speed'])


if __name__ == '__main__':
    main()