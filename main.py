from polars import DataFrame
import polars as pl

from dataplotter import plot_dataframe
from weatherdata import DwdDataFetcher

DF_LENGTH = 78


def main():
    # cloud_base_convective = DataFrame()
    # cloud_cover_above_7_km = DataFrame()
    # cloud_cover_below_1000_ft = DataFrame()
    # cloud_cover_below_500_ft = DataFrame()
    # cloud_cover_effective = DataFrame()
    # cloud_cover_total = DataFrame()
    # temperature_air_max_200 = DataFrame()
    # temperature_air_min_200 = DataFrame()
    # visibility_range = DataFrame()
    # wind_speed = DataFrame()

    data_fetcher = DwdDataFetcher()
    mosmix_forecast = data_fetcher.get_mosmix_forecast()
    icon_eu_forecast = data_fetcher.get_icon_eu_forecast()
    icon_forecast = data_fetcher.get_icon_forecast()
    # observation = data_fetcher.get_observation()

    print(mosmix_forecast)
    date_col = mosmix_forecast['cloud_cover_total']['date'].head(DF_LENGTH)
    vals_col = mosmix_forecast['cloud_cover_total']['value'].head(DF_LENGTH)
    icon_eu_col = icon_eu_forecast['cloud_cover_total']['value'].head(DF_LENGTH)
    icon_col = icon_forecast['cloud_cover_total']['value'].head(DF_LENGTH)
    cloud_cover_total = pl.DataFrame().with_columns(date=date_col)
    cloud_cover_total = cloud_cover_total.with_columns(mosmix_value=vals_col)
    cloud_cover_total = cloud_cover_total.with_columns(icon_eu_value=icon_eu_col)
    cloud_cover_total = cloud_cover_total.with_columns(icon_value=icon_col)

    plot_dataframe(cloud_cover_total)

    # print(cloud_cover_total)
    # print(f"observation: \n{observation}")





if __name__ == '__main__':
    main()