import unittest
from services.value_parser import ValueParser
from services.constants import SPEEDOMETER_KEY, WORTH_KEY, CAR_KEY, CONDITION_KEY
from services.constants import POWER_KEY, TRUNK_KEY, MASS_KEY, PRICE_KEY


class TestHappyPaths(unittest.TestCase):
	default_input = {}
	value_parser = ValueParser(default_input)

	def setUp(self):
		self.default_input = {
				CAR_KEY: 'http://hasznaltauto.hu/auto',
				CONDITION_KEY: 'Újszerű',
				SPEEDOMETER_KEY: '0 km'
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
		car = self.default_input

		car[SPEEDOMETER_KEY] = '92 000 km'
		speedo_worth = self.value_parser.get_speedometer_value()
		self.assertEqual(speedo_worth, -9)

		car[SPEEDOMETER_KEY] = '140 000 km'
		speedo_worth = self.value_parser.get_speedometer_value()
		self.assertEqual(speedo_worth, -12)

		car[SPEEDOMETER_KEY] = '240 000 km'
		speedo_worth = self.value_parser.get_speedometer_value()
		self.assertEqual(speedo_worth, -16)

	def test_price_worth(self):
		car = self.default_input

		#no power, no price
		price_value = self.value_parser.get_price_value()
		self.assertEqual(price_value, 0)

		#no power
		car[PRICE_KEY] = '6.000.000 Ft'
		price_value = self.value_parser.get_price_value()
		self.assertEqual(price_value, 0)

		#no price
		del car[PRICE_KEY]
		car[POWER_KEY] = '100 kW'
		price_value = self.value_parser.get_price_value()
		self.assertEqual(price_value, 0)

		#price and power
		car[PRICE_KEY] = '6.000.000 Ft'
		price_value = self.value_parser.get_price_value()
		self.assertEqual(price_value, 10)
