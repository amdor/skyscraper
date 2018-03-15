# -*- coding: utf-8 -*-

import unittest
from datetime import date

from skyscraper.utils.constants import POWER_KEY, TRUNK_KEY, MASS_KEY, PRICE_KEY, AGE_KEY
from skyscraper.utils.constants import SPEEDOMETER_KEY, CAR_KEY, CONDITION_KEY
from skyscraper.utils.value_parser import ValueParser


class TestBasicPaths(unittest.TestCase):
	default_input = {}
	value_parser = ValueParser(default_input)

	@staticmethod
	def date_to_age(years, months):
		today = date.today()
		month_diff = today.month - months
		if month_diff <= 0:
			years += 1
			months = 12 - month_diff
		else:
			months = month_diff
		return date(today.year - years, months, 1).strftime("%Y/%m")

	def setUp(self):
		self.default_input = {
				CAR_KEY: 'http://hasznaltauto.hu/auto',
				CONDITION_KEY: 'Újszerű',
				SPEEDOMETER_KEY: '0 km',
				AGE_KEY: date.today().strftime("%Y/%m")
			}
		self.value_parser = ValueParser(self.default_input)

	def test_power_worth(self):
		car = self.default_input
		car[POWER_KEY] = '42 kW'

		power_worth = self.value_parser.get_power_value()

		self.assertEqual(power_worth, 3)

	def test_condition_worth(self):
		condition_worth = self.value_parser.get_condition_value()
		self.assertEqual(condition_worth, 0)

		car = self.default_input
		car[CONDITION_KEY] = ''
		condition_worth = self.value_parser.get_condition_value()
		self.assertEqual(condition_worth, -20)

	def test_trunk_worth(self):
		car = self.default_input
		car[TRUNK_KEY] = '290 l'

		trunk_worth = self.value_parser.get_trunk_value()

		self.assertEqual(trunk_worth, 2)

	def test_mass_worth(self):
		car = self.default_input
		car[MASS_KEY] = '1600 kg'

		mass_worth = self.value_parser.get_mass_value()

		self.assertEqual(mass_worth, 3)

	def test_speedometer_worth(self):
		self.assert_speedo('0km', 0)
		self.assert_speedo('0 km', 0)
		self.assert_speedo('92,000 km', -9)
		self.assert_speedo('140 000 km', -12)
		self.assert_speedo('240 000 km', -16)

	def test_price_worth(self):
		car = self.default_input

		#no power, no price
		price_worth = self.value_parser.get_price_value()
		self.assertEqual(price_worth, 0)

		#no power
		car[PRICE_KEY] = '6.000.000 Ft'
		price_worth = self.value_parser.get_price_value()
		self.assertEqual(price_worth, 0)

		#no price
		del car[PRICE_KEY]
		car[POWER_KEY] = '100 kW'
		price_worth = self.value_parser.get_price_value()
		self.assertEqual(price_worth, 0)

		#price and power
		car[PRICE_KEY] = '€ 26.535'
		price_worth = self.value_parser.get_price_value()
		self.assertEqual(price_worth, 10)

	def test_age_worth(self):
		self.assert_age(0, 3, -3)
		self.assert_age(1, 0, -10)
		self.assert_age(10, 0, -23)
		self.assert_age(30, 0, -25)
		self.assert_age(50, 0, -1)

	'''ASSERTIONS'''

	def assert_speedo(self, kilometers, expected):
		car = self.default_input

		car[SPEEDOMETER_KEY] = kilometers
		speedo_worth = self.value_parser.get_speedometer_value()
		self.assertEqual(speedo_worth, expected)

	def assert_age(self, years, months, expected):
		car = self.default_input
		car[AGE_KEY] = TestBasicPaths.date_to_age(years, months)
		age_worth = self.value_parser.get_age_value()
		self.assertEquals(age_worth, expected)
