import os

LAT = float(os.environ["MY_LAT"])
LON = float(os.environ["MY_LON"])
DISTANCE_TO_STATION = 30.0
DF_LENGTH = 78

MOSMIX = "mosmix_forecast"
ICON = "icon_forecast"
ICON_EU = "icon_eu_forecast"
OBSERVATION = "observation_current"

PARAMS_MOSMIX = ['cloud_cover_above_7_km', 'cloud_cover_below_1000_ft', 'cloud_cover_below_500_ft',
                 'cloud_cover_between_2_to_7_km', 'cloud_cover_effective', 'cloud_cover_total',
                 'temperature_air_max_200', 'temperature_air_mean_200', 'temperature_air_min_200',
                 'temperature_dew_point_mean_200',
                 'visibility_range', 'wind_direction', 'wind_speed', ]



PARAMS_OBSERVATION = ["cloud_cover_layer1", "cloud_cover_layer2", "cloud_cover_layer3", "cloud_cover_layer4",
                      "cloud_type_layer1", "cloud_type_layer2", "cloud_type_layer3", "cloud_type_layer4",
                      "cloud_height_layer1", "cloud_height_layer2", "cloud_height_layer3", "cloud_height_layer4",
                      "cloud_cover_total",
                      "humidity",  #
                      "temperature_air_mean_200",
                      "weather",  #
                      "wind_direction",  #
                      "wind_gust_max",  #
                      "wind_speed",
                      #
                      "visibility_range"  #
                      ]

