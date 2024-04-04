from datetime import datetime

from dateutil.tz import tzlocal
from pandas import DataFrame

from exceptionhandler.exception_handler import handle_standard_exception
from utils.constants import FORECAST_FROM_FILE, DEBUG_SORT_DATA, LOCAL_TZ
from utils.utils import save_to_file
from utils.astronomical import get_sun_info_from_location
from utils.constants_weatherdata import DF_LENGTH


def group_df_per_parameter(df: DataFrame, params: list[str]) -> dict[str, DataFrame]:
    """
    Group the given DataFrame `df` per parameter.

    :param df: The DataFrame to be grouped.
    :param params: The list of parameters to group the DataFrame by.
    :return: A dictionary containing parameter names as keys and the corresponding grouped DataFrames as values.
   """
    print(f"{datetime.now()} sort_data.py - group_df_per_parameter") if DEBUG_SORT_DATA else None
    df.reset_index(inplace=True)
    print(f"df columns: {df.columns}") if DEBUG_SORT_DATA else None
    # grouped_df = df.groupby(df['parameter'], group_keys=True).apply(lambda x: x)
    # print(grouped_df) if DEBUG_SORT_DATA else None
    weather_data: dict[str, DataFrame] = {}

    # Creates dict with a dataFrame for every param in params (PARAMS_MOSMIX in constants_weatherdata.py)
    for param in params:
        # TODO: make obsolete by only downloading relevant data
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
    """
    To display the forecasts of different models, each parameter is fetched from
    each model and combined in one df.
    Sorts the dataframes per parameter and returns a dictionary of sorted dataframes.
    :param params: A list of parameters.
    :param mosmix: A dictionary containing the mosmix data for each parameter.
    :param icon: A dictionary containing the icon data for each parameter.
    :param icon_eu: A dictionary containing the icon_eu data for each parameter.
    :param name: The name of the parameter.
    :return: A dictionary containing the sorted dataframes per parameter.
    """

    print(f"sort_data.py - sort_df_per_param") if DEBUG_SORT_DATA else None
    sorted_df = {}
    for param in params:
        df = _create_mixed_df_for_param(param, mosmix[param], icon[param], icon_eu[param])
        if not df.empty:
            sorted_df[param] = df
            if not FORECAST_FROM_FILE:
                save_to_file(f"{name}/{param}", df)

    print(sorted_df) if DEBUG_SORT_DATA else None
    return sorted_df


def _create_mixed_df_for_param(
        parameter: list,
        mosmix_forecast: DataFrame,
        icon_forecast: DataFrame,
        icon_eu_forecast: DataFrame
) -> DataFrame:
    """
    To display the forecasts of different models, each parameter is fetched from
    each model and combined in one df.
    creates dataframe for parameter with values from forecasts
    :param parameter:
    :param mosmix_forecast:
    :param icon_forecast:
    :param icon_eu_forecast:
    :return:
    """
    print(f"{datetime.now()} - create_mixed_dxf_for {parameter}") if DEBUG_SORT_DATA else None

    df = DataFrame()

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
    # save_to_file(parameter, df)
    return df


def get_nights_only_as_list(df: DataFrame) -> list[DataFrame]:
    """
    This function creates a list of night values from a DataFrame.
    It uses sun information to determine nighttime, filters the DataFrame based on nighttime,
    and returns a list of DataFrames for tonight, tomorrow, and the day after tomorrow.
    :rtype: object
    :param df:
    :return:
    """
    print(f"{datetime.now()} - get_nights_only_as_list\n{df}") if DEBUG_SORT_DATA else None

    sun_info = get_sun_info_from_location(days=4)

    df['date'] = df['date'].dt.tz_convert(LOCAL_TZ)
    print(f"\n\n\ndtype of date col: {df['date'].dtype}\n\n\n")  if DEBUG_SORT_DATA else None

    df['date'] = df['date'].apply(datetime.fromtimestamp).astimezone(tzlocal.get_localzone())

    dusk_dawn_tonight = [sun_info[0]["dusk"], sun_info[1]["dawn"]]
    dusk_dawn_tomorrow = [sun_info[1]["dusk"], sun_info[2]["dawn"]]
    dusk_dawn_tomorrow2 = [sun_info[2]["dusk"], sun_info[3]["dawn"]]
    tonight = df[df['date'].between(dusk_dawn_tonight[0], dusk_dawn_tonight[1])]
    tomorrow = df[df['date'].between(dusk_dawn_tomorrow[0], dusk_dawn_tomorrow[1])]
    tomorrow2 = df[df['date'].between(dusk_dawn_tomorrow2[0], dusk_dawn_tomorrow2[1])]

    if DEBUG_SORT_DATA:
        print(f"get_nights_only_as_list - tonight:\n{tonight}")
        print(f"get_nights_only_as_list - tomorrow:\n{tomorrow}")
        print(f"get_nights_only_as_list - tomorrow2:\n{tomorrow2}")

    return [DataFrame(tonight), DataFrame(tomorrow), DataFrame(tomorrow2)]
