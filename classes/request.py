import datetime
from pathlib import Path

import pandas as pd
import requests
import attr
from dotenv.main import DotEnv

import settings
from classes.dclasses import Location, Current, Astro, Day, Hour
from settings import ENV_PATH


class Request:
    def __init__(self, city, days=7, aqi='yes', alerts='yes'):
        self.key = DotEnv(ENV_PATH).get('API_KEY')
        self._html_table_path = settings.HTML_PATH
        self.url = f"https://api.weatherapi.com/v1/forecast.json?key={self.key}&q={city}&days={days}&aqi={aqi}&alerts={alerts}"
        self.response = requests.get(self.url).json()
        self.location = Location.from_dict(self.response['location'])
        self.current = Current.from_dict(self.response['current'])
        self.astro = {}
        self.days = {}
        self.days_by_hour = {}
        self.get_days()
        self.location_df: pd.DataFrame = self.dataclass_to_df(self.location, 'location')
        self.current_df: pd.DataFrame = self.dataclass_to_df(self.current, 'current')
        self.astro_df: pd.DataFrame = self.dataclass_to_df(self.astro, 'astro')
        self.day_df: pd.DataFrame = self.dataclass_to_df(self.days, 'day')
        self.hour_df: pd.DataFrame = self.dataclass_to_df(self.days_by_hour, 'hour')
        self.write_to_html()


    def get_days(self):
        by_day = {}
        for day in self.response['forecast']['forecastday']:
            day_of_week = datetime.datetime.strptime(day['date'], '%Y-%m-%d').strftime('%A')
            self.astro[day_of_week] = Astro.from_dict(day['astro'])
            self.days[day_of_week] = Day.from_dict(day['day'])
            self.days_by_hour[day_of_week] = {}
            for hour in day['hour']:
                formatted_hour = Hour.from_dict(hour)
                self.days_by_hour[day_of_week][formatted_hour.date_time.hour] = formatted_hour

    def write_to_html(self):
        # self.location_df.to_html(f'{self._html_table_path}/location.html')
        self.current_df.to_html(f'{self._html_table_path}/current.html')
        self.astro_df.to_html(f'{self._html_table_path}/astro.html')
        self.day_df.to_html(f'{self._html_table_path}/day.html')
        self.hour_df.to_html(f'{self._html_table_path}/hour.html')

    @staticmethod
    def dataclass_to_df(raw: list | dict, data_type: str):
        data = []
        if data_type == 'current' or data_type == 'location':
            return pd.DataFrame(attr.asdict(raw), index=[0])
        # elif data_type == 'astro':
        #     pass
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
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        timestamp_date, timestamp_time = timestamp.split(' ')
        df['timestamp_date'] = timestamp_date
        df['timestamp_time'] = timestamp_time
        return df


def overview():
    location_by_hour_dict = {}
    location_temp_avg_dict = {}
    for location in settings.LOCATIONS:
        key = location.split(' ')[0].lower()
        req_obj = Request(location)
        location_by_hour_dict[key] = req_obj.hour_df['temperature']
        stats = {}
        stats['max_temp'] = req_obj.day_df['max_temp']
        stats['min_temp'] = req_obj.day_df['min_temp']
        stats['avg_temp'] = req_obj.day_df['avg_temp']
        stats['precipitation'] = req_obj.day_df['total_precipitation']
        stats['snow'] = req_obj.day_df['total_snow']
        stats['chance_of_rain'] = req_obj.day_df['chance_of_rain']
        stats['chance_of_snow'] = req_obj.day_df['chance_of_snow']
        stats['uv'] = req_obj.day_df['uv']
        location_temp_avg_dict[key] = stats
    return_dict = {'temp_hr': location_by_hour_dict, 'daily_stats':
        location_temp_avg_dict}
    return return_dict
