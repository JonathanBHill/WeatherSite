import datetime
from datetime import datetime as dt
import attr
import pandas as pd


def dataclass_to_df(raw: list | dict, data_type: str):
    """
    Converts a dataclass object or a list of dataclass objects to a pandas DataFrame.

    Args:
        raw (list | dict): The dataclass object or list of dataclass objects to convert.
        data_type (str): The type of data contained in the dataclass object(s).
                         This can be 'current', 'location', 'hour', 'day', or 'astro'.

    Returns:
        pandas.DataFrame: A DataFrame representation of the dataclass object(s).

    Raises:
        ValueError: If the data_type is not one of the expected types ('current', 'location', 'hour', 'day', 'astro').

    Examples:
        >>> dataclass_to_df(current_data, 'current')
        >>> dataclass_to_df(location_data, 'location')
    """
    data = []
    if data_type == 'current' or data_type == 'location':
        if isinstance(raw, list):
            for current_or_location in raw:
                data.append(attr.asdict(current_or_location))
            return pd.DataFrame(data)
        else:
            return pd.DataFrame(attr.asdict(raw), index=[0])
    for day in raw:
        if isinstance(raw, list):
            raise TypeError('Cannot parse multiple weeks worth of hourly data.')
        if data_type == 'hour':
            for hour in raw[day]:
                raw_as_dict = {'day': day, 'hour': hour}
                raw_as_dict.update(attr.asdict(raw[day][hour]))
                data.append(raw_as_dict)
        elif data_type == 'day' or data_type == 'astro':
            raw_as_dict = {'day': day}
            raw_as_dict.update(attr.asdict(raw[day]))
            data.append(raw_as_dict)
    df = pd.DataFrame(data)
    return df


def parse_time(dt_object: str) -> dt:
    """
    Parses a string representing a time into a datetime object.

    Args:
        dt_object (str): The datetime object to parse in the format, 'YYYY-MM-DD HH:MM'.

    Returns:
        datetime: The parsed date and time as a datetime object.

    """
    local_date, local_time = dt_object.split(' ')
    year, month, day = local_date.split('-')
    hour, minute = local_time.split(':')
    return dt(int(year), int(month), int(day), int(hour), int(minute))


def change_key(dictionary: dict, old_key: str, new_key: str = None) -> dict:
    """
    Changes the key of a dictionary. If new_key is None, the old key is simply removed.

    Args:
        dictionary (dict): The dictionary to change.
        old_key (str): The old key 'label' to change.
        new_key (str, optional): The new key 'label' that replaces the old key.
        Defaults to None.

    Returns:
        dict: The dictionary with the changed key label.

    Examples:
        >>> change_key({'a': 1, 'b': 2}, 'a', 'c')
        {'c': 1, 'b': 2}
        >>> change_key({'a': 1, 'b': 2}, 'a')
        {'b': 2}
    """
    if new_key is None:
        dictionary.pop(old_key)
        return dictionary
    dictionary[new_key] = dictionary.pop(old_key)
    return dictionary


def convert_cm_to_inch(cm: float) -> float:
    """
    Converts a length measured in centimeters to inches.

    Args:
        cm (float): The length in centimeters.

    Returns:
        float: The length in inches.
    """
    return round((cm * 0.393701), 3)


@attr.dataclass
class Location:
    """
    A dataclass representing a location.

    Attributes:
        city (str): The city of the location.
        region (str): The region of the location.
        country (str): The country of the location.
        latitude (float): The latitude of the location.
        longitude (float): The longitude of the location.
        timezone (str): The timezone of the location.
        localtime_epoch (int): The localtime epoch of the location.
        localtime (dt): The localtime of the location.
    """
    city: str
    region: str
    country: str
    latitude: float
    longitude: float
    timezone: str
    localtime_epoch: int
    localtime: dt
    # city: str
    # region: str
    # country: str
    # latitude: float
    # longitude: float
    # timezone: str
    # localtime_epoch: int
    # localtime: str

    @classmethod
    def from_dict(cls, location_dict: dict):
        """
        Creates a Location object from a dictionary containing location data.

        Args:
            location_dict (dict): Location dictionary from a weatherapi json
            response.

        Returns:
            Location: The location object.
        """
        location_dict = change_key(location_dict, 'name', 'city')
        location_dict = change_key(location_dict, 'lat', 'latitude')
        location_dict = change_key(location_dict, 'lon', 'longitude')
        location_dict = change_key(location_dict, 'tz_id', 'timezone')
        location_dict['localtime'] = location_dict['localtime']
        return cls(**location_dict)


@attr.dataclass
class Current:
    """
    A dataclass representing the current weather conditions.

    Attributes:
        last_updated_epoch (int): The last updated epoch of the weather data.
        last_updated (dt): The last updated time of the weather data.
        temperature (float): The current temperature.
        is_day (int): Indicates whether it's day (1) or night (0).
        condition (str): The current weather condition.
        wind_mph (float): The wind speed in miles per hour.
        wind_degree (float): The wind direction in degrees.
        wind_direction (str): The wind direction as a string.
        pressure (float): The atmospheric pressure.
        precipitation (float): The amount of precipitation.
        humidity (float): The humidity percentage.
        cloud (float): The cloud cover percentage.
        real_feel (float): The 'feels like' temperature.
        visibility_range (float): The visibility range in miles.
        uv (float): The UV index.
        gust_mph (float): The gust speed in miles per hour.
        aq_co (float): The air quality index for carbon monoxide.
        aq_no2 (float): The air quality index for nitrogen dioxide.
        aq_o3 (float): The air quality index for ozone.
        aq_so2 (float): The air quality index for sulfur dioxide.
        aq_pm2_5 (float): The air quality index for particulate matter (PM2.5).
        aq_pm10 (float): The air quality index for particulate matter (PM10).
        aq_epa (float): The US EPA air quality index.
        aq_gb (float): The GB DEFRA air quality index.
    """
    last_updated_epoch: int
    last_updated: dt
    temperature: float
    is_day: int
    condition: str
    wind_mph: float
    wind_degree: float
    wind_direction: str
    pressure: float
    precipitation: float
    humidity: float
    cloud: float
    real_feel: float
    visibility_range: float
    uv: float
    gust_mph: float
    aq_co: float
    aq_no2: float
    aq_o3: float
    aq_so2: float
    aq_pm2_5: float
    aq_pm10: float
    aq_epa: float
    aq_gb: float

    @classmethod
    def from_dict(cls, current_dict: dict):
        """
        Creates a Current object from a dictionary containing data on the real-time
        data for a particular location.

        Args:
            current_dict (dict): Current dictionary from a weatherapi json
            response.

        Returns:
            Current: The current object.
        """
        current_dict = change_key(current_dict, 'temp_f', 'temperature')
        current_dict = change_key(current_dict, 'wind_dir', 'wind_direction')
        current_dict = change_key(current_dict, 'pressure_in', 'pressure')
        current_dict = change_key(current_dict, 'precip_in', 'precipitation')
        current_dict = change_key(current_dict, 'feelslike_f', 'real_feel')
        current_dict = change_key(current_dict, 'vis_miles', 'visibility_range')
        current_dict['aq_co'] = current_dict['air_quality']['co']
        current_dict['aq_no2'] = current_dict['air_quality']['no2']
        current_dict['aq_o3'] = current_dict['air_quality']['o3']
        current_dict['aq_so2'] = current_dict['air_quality']['so2']
        current_dict['aq_pm2_5'] = current_dict['air_quality']['pm2_5']
        current_dict['aq_pm10'] = current_dict['air_quality']['pm10']
        current_dict['aq_epa'] = current_dict['air_quality']['us-epa-index']
        current_dict['aq_gb'] = current_dict['air_quality']['gb-defra-index']
        current_dict['last_updated'] = parse_time(current_dict['last_updated'])
        current_dict.pop('air_quality')
        return cls(**current_dict)


@attr.dataclass
class Day:
    """
    A dataclass representing the weather conditions for a day.

    Attributes:
        max_temp (float): The maximum temperature for the day.
        min_temp (float): The minimum temperature for the day.
        avg_temp (float): The average temperature for the day.
        max_wind (float): The maximum wind speed for the day.
        total_precipitation (float): The total precipitation for the day.
        total_snow (float): The total snowfall for the day.
        avg_visibility (float): The average visibility for the day.
        avg_humidity (float): The average humidity for the day.
        will_it_rain (float): Indicates whether it will rain (1) or not (0).
        chance_of_rain (float): The chance of rain as a percentage.
        will_it_snow (float): Indicates whether it will snow (1) or not (0).
        chance_of_snow (float): The chance of snow as a percentage.
        condition (str): The weather condition for the day.
        uv (float): The UV index for the day.
        aq_co (float): The air quality index for carbon monoxide for the day.
        aq_no2 (float): The air quality index for nitrogen dioxide for the day.
        aq_o3 (float): The air quality index for ozone for the day.
        aq_so2 (float): The air quality index for sulfur dioxide for the day.
        aq_pm2_5 (float): The air quality index for particulate matter (PM2.5) for the
        day.
        aq_pm10 (float): The air quality index for particulate matter (PM10) for the day.
        aq_epa (float): The US EPA air quality index for the day.
        aq_gb (float): The GB DEFRA air quality index for the day.
    """
    max_temp: float
    min_temp: float
    avg_temp: float
    max_wind: float
    total_precipitation: float
    total_snow: float
    avg_visibility: float
    avg_humidity: float
    will_it_rain: float
    chance_of_rain: float
    will_it_snow: float
    chance_of_snow: float
    condition: str
    uv: float
    # aq_co: float
    # aq_no2: float
    # aq_o3: float
    # aq_so2: float
    # aq_pm2_5: float
    # aq_pm10: float
    # aq_epa: float
    # aq_gb: float

    @classmethod
    def from_dict(cls, day_dict: dict):
        """
        Creates a Day object from a dictionary containing data on the weather across a
        specified number of days.

        Args:
            day_dict (dict): Day dictionary from a weatherapi json response.

        Returns:
            Day: The day object.
        """
        # print(day_dict.keys())
        day_dict = change_key(day_dict, 'maxtemp_f', 'max_temp')
        day_dict = change_key(day_dict, 'mintemp_f', 'min_temp')
        day_dict = change_key(day_dict, 'avgtemp_f', 'avg_temp')
        day_dict = change_key(day_dict, 'maxwind_mph', 'max_wind')
        day_dict = change_key(day_dict, 'totalprecip_in', 'total_precipitation')
        day_dict = change_key(day_dict, 'totalsnow_cm', 'total_snow')
        day_dict = change_key(day_dict, 'avgvis_miles', 'avg_visibility')
        day_dict = change_key(day_dict, 'avghumidity', 'avg_humidity')
        day_dict = change_key(day_dict, 'daily_will_it_rain', 'will_it_rain')
        day_dict = change_key(day_dict, 'daily_chance_of_rain', 'chance_of_rain')
        day_dict = change_key(day_dict, 'daily_will_it_snow', 'will_it_snow')
        day_dict = change_key(day_dict, 'daily_chance_of_snow', 'chance_of_snow')
        day_dict = change_key(day_dict, 'uv', 'uv')
        day_dict['total_snow'] = convert_cm_to_inch(day_dict['total_snow'])
        day_dict['condition'] = day_dict['condition']['text']
        # if 'air_quality' in list(day_dict.keys()):
        # try:
        #     if len(day_dict['air_quality'].keys()) > 1:
        #
        #         day_dict['aq_co'] = day_dict['air_quality']['co']
        #         day_dict['aq_no2'] = day_dict['air_quality']['no2']
        #         day_dict['aq_o3'] = day_dict['air_quality']['o3']
        #         day_dict['aq_so2'] = day_dict['air_quality']['so2']
        #         day_dict['aq_pm2_5'] = day_dict['air_quality']['pm2_5']
        #         day_dict['aq_pm10'] = day_dict['air_quality']['pm10']
        #         day_dict['aq_epa'] = day_dict['air_quality']['us-epa-index']
        #         day_dict['aq_gb'] = day_dict['air_quality']['gb-defra-index']
        #     else:
        #         day_dict['aq_co'] = None
        #         day_dict['aq_no2'] = None
        #         day_dict['aq_o3'] = None
        #         day_dict['aq_so2'] = None
        #         day_dict['aq_pm2_5'] = None
        #         day_dict['aq_pm10'] = None
        #         day_dict['aq_epa'] = None
        #         day_dict['aq_gb'] = None
        #     day_dict.pop('air_quality')
        # except:
        #     day_dict['aq_co'] = None
        #     day_dict['aq_no2'] = None
        #     day_dict['aq_o3'] = None
        #     day_dict['aq_so2'] = None
        #     day_dict['aq_pm2_5'] = None
        #     day_dict['aq_pm10'] = None
        #     day_dict['aq_epa'] = None
        #     day_dict['aq_gb'] = None
        # try:
        #     day_dict.pop('air_quality')
        # except:
        #     pass
        return cls(**day_dict)


@attr.dataclass
class Astro:
    """
    A dataclass representing the astronomical conditions for a day.

    Attributes:
        sunrise (str): The time of sunrise.
        sunset (str): The time of sunset.
        moonrise (str): The time of moonrise.
        moonset (str): The time of moonset.
        moon_phase (str): The phase of the moon.
        moon_illumination (float): The illumination of the moon.
        is_moon_up (bool): Indicates whether the moon is up (1) or not (0).
        is_sun_up (bool): Indicates whether the sun is up (1) or not (0).
    """
    sunrise: str
    sunset: str
    moonrise: str
    moonset: str
    moon_phase: str
    moon_illumination: float
    is_moon_up: bool
    is_sun_up: bool

    @classmethod
    def from_dict(cls, astro_dict: dict):
        """
        Creates an Astro object from a dictionary containing astronomical data.

        Args:
            astro_dict (dict): Astro dictionary from a weatherapi json response.

        Returns:
            Astro: The astro object.
        """
        parse = lambda time: dt.strptime(time, '%I:%M %p').strftime('%H:%M')
        astro_dict['sunrise'] = parse(astro_dict['sunrise'])
        astro_dict['sunset'] = parse(astro_dict['sunset'])
        try:
            astro_dict['moonrise'] = parse(astro_dict['moonrise'])
        except ValueError:
            astro_dict['moonrise'] = astro_dict['moonrise']
        try:
            astro_dict['moonset'] = parse(astro_dict['moonset'])
        except ValueError:
            astro_dict['moonset'] = astro_dict['moonset']
        return cls(**astro_dict)


@attr.dataclass
class Hour:
    """
    A dataclass representing the weather conditions for an hour.

    Attributes:
        time_epoch (str): The time epoch.
        date_time (dt): The date and time.
        temperature (float): The temperature.
        is_day (int): Indicates whether it's day (1) or night (0).
        condition (str): The weather condition.
        wind_mph (float): The wind speed in miles per hour.
        wind_degree (float): The wind direction in degrees.
        wind_direction (str): The wind direction as a string.
        pressure (float): The atmospheric pressure.
        precipitation (float): The amount of precipitation.
        snow (float): The amount of snow.
        humidity (float): The humidity percentage.
        cloud (float): The cloud cover percentage.
        real_feel (float): The 'feels like' temperature.
        windchill (float): The wind chill.
        heat_index (float): The heat index.
        dewpoint (float): The dew point.
        will_it_rain (float): Indicates whether it will rain (1) or not (0).
        chance_of_rain (float): The chance of rain as a percentage.
        will_it_snow (float): Indicates whether it will snow (1) or not (0).
        chance_of_snow (float): The chance of snow as a percentage.
        visibility_range (float): The visibility range in miles.
        gust_mph (float): The gust speed in miles per hour.
        uv (float): The UV index.
        aq_co (float): The air quality index for carbon monoxide.
        aq_no2 (float): The air quality index for nitrogen dioxide.
        aq_o3 (float): The air quality index for ozone.
        aq_so2 (float): The air quality index for sulfur dioxide.
        aq_pm2_5 (float): The air quality index for particulate matter (PM2.5).
        aq_pm10 (float): The air quality index for particulate matter (PM10).
        aq_epa (float): The US EPA air quality index.
        aq_gb (float): The GB DEFRA air quality index.
        shortwave_radiation (float): The shortwave radiation.
        diffuse_horizontal_irradiation (float): The diffuse horizontal irradiation.
    """
    time_epoch: str
    date_time: str
    temperature: float
    is_day: int
    condition: str
    wind_mph: float
    wind_degree: float
    wind_direction: str
    pressure: float
    precipitation: float
    snow: float
    humidity: float
    cloud: float
    real_feel: float
    windchill: float
    heat_index: float
    dewpoint: float
    will_it_rain: float
    chance_of_rain: float
    will_it_snow: float
    chance_of_snow: float
    visibility_range: float
    gust_mph: float
    uv: float
    # aq_co: float
    # aq_no2: float
    # aq_o3: float
    # aq_so2: float
    # aq_pm2_5: float
    # aq_pm10: float
    # aq_epa: float
    # aq_gb: float
    # shortwave_radiation: float
    # diffuse_horizontal_irradiation: float

    @classmethod
    def from_dict(cls, hour_dict: dict):
        """
        Creates an Hour object from a dictionary containing weather data for a single
        day on an hourly basis.

        Args:
            hour_dict (dict): Hour dictionary from a weatherapi json response.

        Returns:
            Hour: The hour object.
        """
        hour_dict = change_key(hour_dict, 'temp_f', 'temperature')
        hour_dict = change_key(hour_dict, 'wind_dir', 'wind_direction')
        hour_dict = change_key(hour_dict, 'windchill_f', 'windchill')
        hour_dict = change_key(hour_dict, 'pressure_in', 'pressure')
        hour_dict = change_key(hour_dict, 'precip_in', 'precipitation')
        hour_dict = change_key(hour_dict, 'feelslike_f', 'real_feel')
        hour_dict = change_key(hour_dict, 'heatindex_f', 'heat_index')
        hour_dict = change_key(hour_dict, 'dewpoint_f', 'dewpoint')
        hour_dict = change_key(hour_dict, 'will_it_rain', 'will_it_rain')
        hour_dict = change_key(hour_dict, 'chance_of_rain', 'chance_of_rain')
        hour_dict = change_key(hour_dict, 'will_it_snow', 'will_it_snow')
        hour_dict = change_key(hour_dict, 'chance_of_snow', 'chance_of_snow')
        hour_dict = change_key(hour_dict, 'vis_miles', 'visibility_range')
        # try:
        #     hour_dict = change_key(hour_dict, 'short_rad', 'shortwave_radiation')
        # except:
        #     hour_dict['shortwave_radiation'] = None
        # try:
        #     hour_dict = change_key(hour_dict, 'diff_rad',
        #                            'diffuse_horizontal_irradiation')
        # except:
        #     hour_dict['diffuse_horizontal_irradiation'] = None
        hour_dict['condition'] = hour_dict['condition']['text']
        hour_dict['date_time'] = parse_time(hour_dict['time'])
        hour_dict['snow'] = convert_cm_to_inch(hour_dict['snow_cm'])
        # try:
        #     if len(hour_dict['air_quality'].keys()):
        #         hour_dict['aq_co'] = hour_dict['air_quality']['co']
        #         hour_dict['aq_no2'] = hour_dict['air_quality']['no2']
        #         hour_dict['aq_o3'] = hour_dict['air_quality']['o3']
        #         hour_dict['aq_so2'] = hour_dict['air_quality']['so2']
        #         hour_dict['aq_pm2_5'] = hour_dict['air_quality']['pm2_5']
        #         hour_dict['aq_pm10'] = hour_dict['air_quality']['pm10']
        #         hour_dict['aq_epa'] = hour_dict['air_quality']['us-epa-index']
        #         hour_dict['aq_gb'] = hour_dict['air_quality']['gb-defra-index']
        #     else:
        #         hour_dict['aq_co'] = None
        #         hour_dict['aq_no2'] = None
        #         hour_dict['aq_o3'] = None
        #         hour_dict['aq_so2'] = None
        #         hour_dict['aq_pm2_5'] = None
        #         hour_dict['aq_pm10'] = None
        #         hour_dict['aq_epa'] = None
        #         hour_dict['aq_gb'] = None
        #     hour_dict.pop('air_quality')
        # except:
        #     hour_dict['aq_co'] = None
        #     hour_dict['aq_no2'] = None
        #     hour_dict['aq_o3'] = None
        #     hour_dict['aq_so2'] = None
        #     hour_dict['aq_pm2_5'] = None
        #     hour_dict['aq_pm10'] = None
        #     hour_dict['aq_epa'] = None
        #     hour_dict['aq_gb'] = None
        hour_dict.pop('time')
        hour_dict.pop('snow_cm')
        return cls(**hour_dict)
