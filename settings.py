import os
from pathlib import Path

from dotenv.main import DotEnv

PROJECT_PATH = Path(os.path.dirname(__file__))
ENV_PATH = PROJECT_PATH / '.env'
DATA_PATH = PROJECT_PATH / 'data'
HTML_PATH = PROJECT_PATH / 'static/html'
WEATHER_DB_PATH = DATA_PATH / 'weather.db'
WORKDAYS = ['Tuesday', 'Thursday', 'Friday', 'Saturday']
LOCATIONS = ['Boulder CO', 'Louisville CO', 'Superior CO', 'Lafayette CO', 'Erie CO']

MONGO_URI = DotEnv(ENV_PATH).get('MONGO_DB_URI')

# print(ENV_PATH)
print(HTML_PATH.as_posix())
