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
CURRENCY_KEY = 'currency'
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
