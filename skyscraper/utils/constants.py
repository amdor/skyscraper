# -*- coding: utf-8 -*-
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

AGE_PARSE_KEY = 'Évjárat'
CONDITION_PARSE_KEY = 'Állapot'
MASS_PARSE_KEY = 'Saját tömeg'
POWER_PARSE_KEY = 'Teljesítmény'
PRICE_PARSE_KEY = 'Vételár'
SALE_PRICE_PARSE_KEY = 'Akciós ár'
SPEEDOMETER_PARSE_KEY = 'Kilométeróra állása'
TRUNK_PARSE_KEY = 'Csomagtartó'

CAR_FEATURE_KEY_MAP = {AGE_PARSE_KEY: AGE_KEY,
					   CONDITION_PARSE_KEY: CONDITION_KEY,
					   MASS_PARSE_KEY: MASS_KEY,
					   POWER_PARSE_KEY: POWER_KEY,
					   PRICE_PARSE_KEY: PRICE_KEY,
					   SALE_PRICE_PARSE_KEY: PRICE_KEY,
					   SPEEDOMETER_PARSE_KEY: SPEEDOMETER_KEY,
					   TRUNK_PARSE_KEY: TRUNK_KEY}

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
