import unittest
from services.comparator_service import compare_cars
from services.constants import POWER_KEY, WORTH_KEY, CAR_KEY, CONDITION_KEY
from services.constants import TRUNK_KEY, MASS_KEY, SPEEDOMETER_KEY


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

	def test_power_worth(self):
		car = self.defaultInput[0]
		car[POWER_KEY] = '42 LE'

		compare_cars(self.defaultInput)

		self.assertEqual(car[WORTH_KEY], 3)

	def test_condition_worth(self):
		car1 = self.defaultInput[0]

		compare_cars(self.defaultInput)

		self.assertEqual(car1[WORTH_KEY], 0)

	def test_trunk_worth(self):
		car1 = self.defaultInput[0]
		car1[TRUNK_KEY] = '290 l'

		compare_cars(self.defaultInput)

		self.assertEqual(car1[WORTH_KEY], 2)

	def test_mass_worth(self):
		car1 = self.defaultInput[0]
		car1[MASS_KEY] = '1600 kg'

		compare_cars(self.defaultInput)

		self.assertEqual(car1[WORTH_KEY], 3)

	def test_speedometer_worth(self):
		car1 = self.defaultInput[0]

		car1[SPEEDOMETER_KEY] = '92 000 km'
		compare_cars(self.defaultInput)
		self.assertEqual(car1[WORTH_KEY], -9)

		car1[SPEEDOMETER_KEY] = '140 000 km'
		compare_cars(self.defaultInput)
		self.assertEqual(car1[WORTH_KEY], -12)

		car1[SPEEDOMETER_KEY] = '240 000 km'
		compare_cars(self.defaultInput)
		self.assertEqual(car1[WORTH_KEY], -16)
