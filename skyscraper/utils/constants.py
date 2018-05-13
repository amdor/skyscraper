# -*- coding: utf-8 -*-
import os
from enum import Enum

CAR_KEY = 'CarUri'
WORTH_KEY = 'worth'

AGE_KEY = 'prod_date'
CONDITION_KEY = 'condition'
MASS_KEY = 'mass'
POWER_KEY = 'power'
PRICE_KEY = 'price'
SPEEDOMETER_KEY = 'speedometer'
TRUNK_KEY = 'trunk'


ACCEPTED_CURRENCIES = ['$', '€', '£', 'Ft', 'FT', 'HUF']
ACCEPTED_CURRENCY_KEYS = {'$': 'USD',
						  '€': 'EUR',
						  '£': 'GBP',
						  'Ft': 'HUF',
						  'FT': 'HUF',
						  'HUF': 'HUF'}


class Conditions(Enum):
	COMMON = 'Normál'
	EXCELLENT = 'Kitűnő'
	UNDAMAGED = 'Sérülésmentes'
	PRESERVED = 'Megkímélt'
	NOVEL = 'Újszerű'

URL_KEY = 'carUrls'
HTML_KEY = 'htmls'
USER_ID_TOKEN_KEY = 'idToken'
CAR_DATA_KEY = 'carData'
MONGO_URL = 'mongodb://heroku_3dl7hhzd:mt7air71j1vggp2mm5hpnsu9at@ds239029.mlab.com:39029/heroku_3dl7hhzd'
# MONGO_URL = os.environ.get('MONGODB_URI')
DB_NAME = 'heroku_3dl7hhzd'
# DB_NAME = os.environ.get('DB_NAME')
CAR_DETAILS = 'car_details'
