import unittest
from services.comparator_service import compare_cars
from services.constants import POWER_KEY, WORTH_KEY, CAR_KEY, CONDITION_KEY
from services.constants import TRUNK_KEY, MASS_KEY


class TestHappyPaths(unittest.TestCase):
	defaultInput = []

	def setUp(self):
		self.defaultInput = [
			{
				CAR_KEY: 'http://hasznaltauto.hu/auto',
				CONDITION_KEY: 'Újszerű'
			},
			{
				CAR_KEY: 'http://hasznaltauto.hu/auto'
			}
		]

	def test_null_worth(self):
		car = self.defaultInput[0]
		compare_cars(self.defaultInput)
		self.assertEqual(car[WORTH_KEY], 0)

	def test_power_worth(self):
		car = self.defaultInput[0]
		car[POWER_KEY] = '42 LE'

		compare_cars(self.defaultInput)

		self.assertEqual(car[WORTH_KEY], 3)

	def test_condition_worth(self):
		car1 = self.defaultInput[0]
		car2 = self.defaultInput[1]
		car2[CONDITION_KEY] = ''

		compare_cars(self.defaultInput)

		self.assertEqual(car1[WORTH_KEY], 0)
		self.assertEqual(car2[WORTH_KEY], -20)

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
