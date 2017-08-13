from services.constants import POWER_KEY,CONDITION_KEY, Conditions, TRUNK_KEY
from services.constants import MASS_KEY


class ValueParser:

	def __init__(self, car_data):
		self.car_data = car_data

	@staticmethod
	def __get_first_number(string_value):
		return [int(s) for s in string_value.split() if s.isdigit()][0]

	def get_power_value(self):
		"""
		Parses the the horsepower value of the car from the HTML text
		representation
		car_data[POWER_KEY]: the text representation e.g. '62 LE'
		:return: the value e.g. 62 or null if power is not present
		"""
		return self.__get_first_number(self.car_data.get(POWER_KEY, '0')) / 14

	def get_condition_value(self):
		"""
		Parses the value for condition.
		Enumerated conditions are viewed as good, and thus handled
		as baseline. Anything else (including empty value) is added as penalty
		:return: the value for condition
		"""
		condition_text = self.car_data.get(CONDITION_KEY,'')
		if condition_text == Conditions.COMMON.value \
			or condition_text == Conditions.EXCELLENT.value \
			or condition_text == Conditions.UNDAMAGED.value \
			or condition_text == Conditions.PRESERVED.value \
			or condition_text == Conditions.NOVEL.value:
			return 0
		else:
			return -20

	def get_trunk_value(self):
		"""
		Presumably trunk space is in liter
		:return: the value for trunk space
		"""
		trunk_space_text = self.car_data.get(TRUNK_KEY, '0')
		trunk_space_value = self.__get_first_number(trunk_space_text)
		return round(trunk_space_value / 150.0)

	def get_mass_value(self):
		"""
		Car's mass in kilograms converted to car worth
		:return: the value for mass
		"""
		mass_text = self.car_data.get(MASS_KEY, '0')
		mass_value = self.__get_first_number(mass_text)
		return round(mass_value / 500.0)
