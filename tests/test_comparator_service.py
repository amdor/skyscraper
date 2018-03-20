# -*- coding: utf-8 -*-

import unittest

from skyscraper.comparator_service import CarComparator
from skyscraper.utils.constants import SPEEDOMETER_KEY
from skyscraper.utils.constants import WORTH_KEY, CAR_KEY, CONDITION_KEY

compare_cars = CarComparator.compare_cars


class TestHappyPaths(unittest.TestCase):
	defaultInput = []

	def setUp(self):
		self.defaultInput = [
			{
				CAR_KEY: 'http://hasznaltauto.hu/auto',
				CONDITION_KEY: 'Újszerű',
				SPEEDOMETER_KEY: '0 km'
			}
		]

	def test_null_worth(self):
		car = self.defaultInput[0]
		compare_cars(self.defaultInput)
		self.assertEqual(car[WORTH_KEY], 30)

	def test_no_properties(self):
		car = {
			CAR_KEY: 'http://hasznaltauto.hu/auto'
		}
		compare_cars([car])
		self.assertEqual(car[WORTH_KEY], 10)
