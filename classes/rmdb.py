from sqlalchemy import Column, Integer, String, create_engine, Table, Float, inspect
from sqlalchemy.orm import sessionmaker, declarative_base, Session

import settings

# from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Hourly(Base):
    __tablename__ = 'hourly'

    id = Column(Integer, primary_key=True, autoincrement=True)
    day = Column(String)
    hour = Column(Integer)
    time_epoch = Column(Integer)
    date_time = Column(String)
    temperature = Column(Float)
    is_day = Column(Integer)
    condition = Column(String)
    wind_mph = Column(Float)
    wind_degree = Column(Integer)
    wind_direction = Column(String)
    pressure = Column(Float)
    precipitation = Column(Float)
    snow = Column(Float)
    humidity = Column(Integer)
    cloud = Column(Integer)
    real_feel = Column(Float)
    windchill = Column(Float)
    heat_index = Column(Float)
    dewpoint = Column(Float)
    will_it_rain = Column(Integer)
    chance_of_rain = Column(Integer)
    will_it_snow = Column(Integer)
    chance_of_snow = Column(Integer)
    visibility_range = Column(Float)
    gust_mph = Column(Float)
    uv = Column(Float)
    timestamp_date = Column(String)
    timestamp_time = Column(String)

    def __init__(self, session: Session, hourly_dict: dict):
        self.session = session
        self.table_count = self.count_records(self.session, True)
        # self.id = self.table_count - 1
        self.day = hourly_dict['day']
        self.hour = hourly_dict['hour']
        self.time_epoch = hourly_dict['time_epoch']
        self.date_time = str(hourly_dict['date_time'])
        self.temperature = hourly_dict['temperature']
        self.is_day = hourly_dict['is_day']
        self.condition = hourly_dict['condition']
        self.wind_mph = hourly_dict['wind_mph']
        self.wind_degree = hourly_dict['wind_degree']
        self.wind_direction = hourly_dict['wind_direction']
        self.pressure = hourly_dict['pressure']
        self.precipitation = hourly_dict['precipitation']
        self.snow = hourly_dict['snow']
        self.humidity = hourly_dict['humidity']
        self.cloud = hourly_dict['cloud']
        self.real_feel = hourly_dict['real_feel']
        self.windchill = hourly_dict['windchill']
        self.heat_index = hourly_dict['heat_index']
        self.dewpoint = hourly_dict['dewpoint']
        self.will_it_rain = hourly_dict['will_it_rain']
        self.chance_of_rain = hourly_dict['chance_of_rain']
        self.will_it_snow = hourly_dict['will_it_snow']
        self.chance_of_snow = hourly_dict['chance_of_snow']
        self.visibility_range = hourly_dict['visibility_range']
        self.gust_mph = hourly_dict['gust_mph']
        self.uv = hourly_dict['uv']
        self.timestamp_date = hourly_dict['timestamp_date']
        self.timestamp_time = hourly_dict['timestamp_time']

    @classmethod
    def count_records(cls, session: Session, self: bool = False):
        number_of_records = session.query(cls).count()
        if self is False:
            if number_of_records > 1:
                print(
                    f'There are {number_of_records} records in table {cls.__tablename__}.')
            else:
                print(
                    f'There is {number_of_records} record in table {cls.__tablename__!r}.')
        return number_of_records

    def add_record(self):
        self.session.add(self)
        print('added')
        for instance in self.session.new:
            print(f'new: {instance}')

    def __repr__(self):
        return (f"Hourly(id={self.id}, day={self.day}, hour={self.hour}, "
                f"time_epoch={self.time_epoch}, date_time={self.date_time}, "
                f"temperature={self.temperature}, is_day={self.is_day}, "
                f"condition={self.condition}, wind_mph={self.wind_mph}, "
                f"wind_degree={self.wind_degree}, wind_direction={self.wind_direction}, "
                f"pressure={self.pressure}, precipitation={self.precipitation}, "
                f"snow={self.snow}, humidity={self.humidity}, cloud={self.cloud}, "
                f"real_feel={self.real_feel}, windchill={self.windchill}, "
                f"heat_index={self.heat_index}, dewpoint={self.dewpoint}, "
                f"will_it_rain={self.will_it_rain}, chance_of_rain={self.chance_of_rain}, "
                f"will_it_snow={self.will_it_snow}, chance_of_snow={self.chance_of_snow}, "
                f"visibility_range={self.visibility_range}, gust_mph={self.gust_mph}, "
                f"uv={self.uv}, timestamp_date={self.timestamp_date}, "
                f"timestamp_time={self.timestamp_time})"
                )


class Location(Base):
    __tablename__ = 'location'

    id = Column(Integer, primary_key=True, autoincrement=True)
    city = Column(String)
    region = Column(String)
    country = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    timezone = Column(String)
    localtime_epoch = Column(Integer)
    local_date = Column(String)
    local_time = Column(String)

    def __init__(self, session: Session, location_dict: dict):
        self.session = session
        self.table_count = self.count_records(self.session, True)
        # self.id = self.table_count - 1
        self.city = location_dict['city']
        self.region = location_dict['region']
        self.country = location_dict['country']
        self.latitude = location_dict['latitude']
        self.longitude = location_dict['longitude']
        self.timezone = location_dict['timezone']
        self.localtime_epoch = location_dict['localtime_epoch']
        self.local_date = location_dict['localtime'].split(' ')[0]
        self.local_time = location_dict['localtime'].split(' ')[1]

    @classmethod
    def count_records(cls, session: Session, self: bool = False):
        number_of_records = session.query(cls).count()
        if self is False:
            if number_of_records > 1:
                print(f'There are {number_of_records} records in table {cls.__tablename__}.')
            else:
                print(f'There is {number_of_records} record in table {cls.__tablename__!r}.')
        return number_of_records

    def add_record(self):
        self.session.add(self)
        print('added')
        for instance in self.session.new:
            print(f'new: {instance}')

    def __repr__(self):
        return (f"Location(id={self.id}, city={self.city}, country={self.country}, "
                f"latitude"
                f"={self.latitude}, longitude={self.longitude}, timezone_id"
                f"={self.timezone}, localtime_epoch={self.localtime_epoch}, "
                f"localtime={self.localtime})"
                )


class TableManagement:
    def __init__(self, engine, table_name=None, autoload=True, autoload_with=None):
        self.engine = engine
        self.table_name = table_name
        self.metadata = Base.metadata
        self.autoload = autoload
        self.autoload_with = autoload_with

    def drop_table(self, engine):
        self.metadata.tables[self.table_name].drop(engine)

    def create_table(self, engine):
        self.metadata.tables[self.table_name].create(engine)


class Database:
    def __init__(self, db_name):
        self.url = f'sqlite:///{settings.DATA_PATH.as_posix()}/{db_name}.db'
        self.engine = create_engine(self.url)
        self.Session = sessionmaker(bind=self.engine)

    def create_tables(self):
        Base.metadata.create_all(self.engine)

    def remove_tables(self, table_name: str):
        Table(table_name, Base.metadata, autoload=True, autoload_with=self.engine).drop(
            self.engine)

    def add_hourly_records(self, hourly: dict | list[dict]):
        session = self.Session()
        if isinstance(hourly, dict):
            record = Hourly(session, hourly)
            session.add(record)
        elif isinstance(hourly, list):
            records = [Hourly(session, hour) for hour in hourly]
            session.add_all(records)
        # session.add(location)
        session.commit()
        session.close()

    def add_location_records(self, location: dict | list[dict]):
        session = self.Session()
        if isinstance(location, dict):
            record = Location(self.Session(), location)
            session.add(record)
        elif isinstance(location, list):
            records = [Location(self.Session(), loc) for loc in location]
            session.add_all(records)
        # session.add(location)
        session.commit()
        session.close()

    def add_location_records_2(self, location: dict | list[dict]):
        session = self.Session()
        if isinstance(location, dict):
            existing_record = session.query(Location).filter_by(
                city=location['city']).first()
            if existing_record is not None:
                # Update existing record
                for key, value in location.items():
                    setattr(existing_record, key, value)
            else:
                # Add new record
                record = Location(session, location)
                session.add(record)
        elif isinstance(location, list):
            for loc in location:
                # loc = loc[0]
                existing_record = session.query(Location).filter_by(city=loc['city']).first()
                if existing_record is not None:
                    loc['local_date'] = loc['localtime'].split(' ')[0]
                    loc['local_time'] = loc['localtime'].split(' ')[1]
                    del loc['localtime']
                    # Update existing record
                    for key, value in loc.items():
                        setattr(existing_record, key, value)
                else:
                    # Add new record
                    record = Location(session, loc)
                    session.add(record)
        session.commit()
        session.close()

    def wipe_table(self, table_object):
        session = self.Session()
        session.query(table_object).delete()
        session.commit()

    # def count_records(self, table_name):
    #     return self.Session().query(table_name).count()

    def get_location(self, user_id):
        session = self.Session()
        user = session.query(Location).filter_by(id=user_id).first()
        return user

    def get_table_names(self):
        assert inspect(self.engine) is not None
        inspector = inspect(self.engine)
        return inspector.get_table_names()

    # def print_staged_changes(self):
    #     print('staged changes:')
    #     print(self.Session().new)
    #     for instance in self.Session().new:
    #         print(f'new: {instance}')


def main():
    db = Database('weather')
    # tbl = TableManagement(db.engine, 'location')
    db.Session()
    db.get_table_names()
    # db.create_tables()

    # mock_dict = {'city': 'Denver', 'region': 'Colorado',
    #                     'country': 'USA',
    #                     'latitude': 39.7392, 'longitude': 104.9903,
    #                     'timezone': 'MST', 'localtime_epoch': 1631481600,
    #              'localtime': '2021-09-13 20:00'}
    # mock_list = [mock_dict, mock_dict]
    # db.wipe_table(Location)
    # db.engine.connect().execute()
    # print(db.count_records(Location))
    # db.add_location_records(mock_list)
    # location = Location(db.Session(), mock_dict)
    # location.add_record()
    # location.add_record()
    # db.Session()
    # db.print_staged_changes()
    # print(Location.count_records(db.Session()))
    # print(location)
    # db.add_location(location)
    # location = db.get_location(1)
    # db.remove_tables('users')
    # print(location)


if __name__ == '__main__':
    main()
