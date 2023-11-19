from datetime import datetime

from pandas import DataFrame

from exceptionhandler import handle_standard_exception
from utils import FORECAST_FROM_FILE, DF_LENGTH, get_sun_info_from_location, save_to_file, DEBUG_SORT_DATA, LOCAL_TZ


def group_df_per_parameter(df: DataFrame, params: list[str]) -> dict[str, DataFrame]:
    print(f"{datetime.now()} - group_df_per_parameter") if DEBUG_SORT_DATA else None
    df.reset_index(inplace=True)
    print(f"df columns: {df.columns}") if DEBUG_SORT_DATA else None
    # grouped_df = df.groupby(df['parameter'], group_keys=True).apply(lambda x: x)
    # print(grouped_df) if DEBUG_SORT_DATA else None
    weather_data: dict[str, DataFrame] = {}
    for param in params:

        filtered_df = df[df['parameter'] == param]
        if DEBUG_SORT_DATA:
            print(f"filtered data - {param}")
            print(filtered_df)
        weather_data[param] = filtered_df
        # except Exception as e:
        #     handle_standard_exception("group_df_per_parameter", e)
    print(f"grouped weather data: {weather_data}") if DEBUG_SORT_DATA else None
    return weather_data


def sort_df_per_param(params, mosmix, icon, icon_eu, name) -> dict[str, DataFrame]:
    print(f"sort_df_per_param") if DEBUG_SORT_DATA else None
    sorted_df = {}
    for param in params:
        df = create_mixed_df_for_param(param, mosmix[param], icon[param], icon_eu[param])
        if not df.empty:
            sorted_df[param] = df
            if not FORECAST_FROM_FILE:
                save_to_file(f"{name}/{param}", df)
    # print(sorted_df) if DEBUG_SORT_DATA else None
    return sorted_df


def create_mixed_df_for_param(
        parameter: list,
        mosmix_forecast: DataFrame,
        icon_forecast: DataFrame,
        icon_eu_forecast: DataFrame
) -> DataFrame:
    """
    creates dataframe for parameter with values from forecasts
    :param parameter:
    :param mosmix_forecast:
    :param icon_forecast:
    :param icon_eu_forecast:
    :return:
    """
    print(f"{datetime.now()} - create_mixed_dxf_for {parameter}") if DEBUG_SORT_DATA else None

    df = DataFrame()
    # try:
    date_col = mosmix_forecast['date'].head(DF_LENGTH)
    vals_col = mosmix_forecast['value'].head(DF_LENGTH)
    param_col = mosmix_forecast['parameter'].head(DF_LENGTH)
    icon_eu_col = icon_eu_forecast['value'].head(DF_LENGTH)
    icon_col = icon_forecast['value'].head(DF_LENGTH)
    df['date'] = date_col
    df['parameter'] = param_col
    df['mosmix_value'] = vals_col
    df['icon_value'] = icon_col
    df['icon_eu_value'] = icon_eu_col
    return df
    save_to_file(parameter, df)
# except Exception as e:
#     handle_standard_exception("Exception in create_mixed_df_for_param", e)


def get_nights_only_as_list(df: DataFrame) -> list[DataFrame]:
    """
    creates list of night values
    :rtype: object
    :param df:
    :return:
    """
    # print(f"{datetime.now()} - get_nights_only_as_list\n{df}") if DEBUG_SORT_DATA else None
    sun_info = get_sun_info_from_location(days=4)

    df['date'] = df['date'].dt.tz_convert(LOCAL_TZ)
    # print(f"\n\n\ndtype of date col: {df['date'].dtype}\n\n\n")
    # df['date'] = df['date'].apply(datetime.fromtimestamp).astimezone(tzlocal.get_localzone())

    dusk_dawn_tonight = [sun_info[0]["dusk"], sun_info[1]["dawn"]]
    dusk_dawn_tomorrow = [sun_info[1]["dusk"], sun_info[2]["dawn"]]
    dusk_dawn_tomorrow2 = [sun_info[2]["dusk"], sun_info[3]["dawn"]]
    tonight = df[df['date'].between(dusk_dawn_tonight[0], dusk_dawn_tonight[1])]
    tomorrow = df[df['date'].between(dusk_dawn_tomorrow[0], dusk_dawn_tomorrow[1])]
    tomorrow2 = df[df['date'].between(dusk_dawn_tomorrow2[0], dusk_dawn_tomorrow2[1])]

    # if DEBUG_SORT_DATA:
    #     print(f"get_nights_only_as_list - tonight:\n{tonight}")
    #     print(f"get_nights_only_as_list - tomorrow:\n{tomorrow}")
    #     print(f"get_nights_only_as_list - tomorrow2:\n{tomorrow2}")

    return [DataFrame(tonight), DataFrame(tomorrow), DataFrame(tomorrow2)]
