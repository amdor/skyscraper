import unittest

from services.comparator_service import compare_cars
from services.utils.constants import SPEEDOMETER_KEY
from services.utils.constants import WORTH_KEY, CAR_KEY, CONDITION_KEY


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
		self.assertEqual(car[WORTH_KEY], 0)

	def test_no_properties(self):
		car = {
			CAR_KEY: 'http://hasznaltauto.hu/auto'
		}
		compare_cars([car])
		self.assertEqual(car[WORTH_KEY], -32)
