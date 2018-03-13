from datetime import date
from math import log10

from skyscraper.utils.constants import MASS_KEY, SPEEDOMETER_KEY, PRICE_KEY, AGE_KEY
from skyscraper.utils.constants import POWER_KEY, CONDITION_KEY, Conditions, TRUNK_KEY


class ValueParser:

	def __init__(self, car_data):
		self.car_data = car_data

	@staticmethod
	def __get_first_number(string_value):
		"""
		Parses the first number of a string, that starts with a number.
		:rtype: int
		:param string_value: string to parse
		:return: the first number followed by any regarded delimiter. Space, dot, coma delimited numbers are regarded
		"""
		string_value = string_value.replace('.', '').replace(',', '').lstrip("-")
		num_str_arr = [s for s in string_value.split()]
		num_string = ''
		i = 0
		while i < len(num_str_arr) and num_str_arr[i].isdigit():
			num_string = num_string + num_str_arr[i]
			i += 1
		if i > 0:
			return int(num_string)
		else:
			return 0

	def get_power_value(self):
		"""
		Parses the the kilowatt value of the car from the HTML text
		representation
		car_data[POWER_KEY]: the text representation e.g. '62 kW'
		:return: the value e.g. 62 or null if power is not present
		"""
		return ValueParser.__get_first_number(self.car_data.get(POWER_KEY, '0')) / 14

	def get_condition_value(self):
		"""
		Parses the value for condition.
		Enumerated conditions are viewed as good, and thus handled
		as baseline. Anything else (including empty value) is added as penalty
		:return: the value for condition
		"""
		condition_text = self.car_data.get(CONDITION_KEY, '')
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
		trunk_space_value = ValueParser.__get_first_number(trunk_space_text)
		return round(trunk_space_value / 150)

	def get_mass_value(self):
		"""
		Car's mass in kilograms converted to car worth
		:return: the value for mass
		"""
		mass_text = self.car_data.get(MASS_KEY, '0')
		mass_value = ValueParser.__get_first_number(mass_text)
		return round(mass_value / 500)

	def get_speedometer_value(self):
		"""
		Speedometer value: first 100 000km is 0-10 proportionately,
		the part from 100 000 to 200 000 is plus 1-5 penalty point similarly
		from 200 000 it's 2.5 penalty for every 100 000 (proportionately)
		The more a car runs, the less it's worth
		:return: value for speedometer
		"""
		speedometer_text = self.car_data.get(SPEEDOMETER_KEY, '-12')
		speedometer_value = ValueParser.__get_first_number(speedometer_text)
		if 0 < speedometer_value:
			speedometer_value = speedometer_value / 10000
		else:
			return speedometer_value
		if 10.0 < speedometer_value < 20:
			speedometer_value = 10 + (speedometer_value - 10) / 2
		elif 20.0 < speedometer_value:
			speedometer_value = 15 + (speedometer_value - 20) / 4
		return round(speedometer_value) * -1

	def get_price_value(self):
		"""
		Price is calculated from the price and the power, if there is no problem
		(like no power or price data), NOTE: max cap
		:return: price to power ratio or 0 if there is no price or power
		"""
		power = ValueParser.__get_first_number(self.car_data.get(POWER_KEY, '0'))
		ratio = 5000 * power
		price_text = self.car_data.get(PRICE_KEY, '0')
		price_value = ValueParser.__get_first_number(price_text)
		if min(price_value, power) <= 0:
			return 0
		price_value = round(price_value / ratio)
		return min(price_value, 10)

	def get_age_value(self):
		"""
		The date of production is required for this feature in YYYY[/MM/*]? format
		The base point of car worth loss was
		http://www.edmunds.com/car-buying/how-fast-does-my-new-car-lose-value-infographic.html
		:return: the worth loss by the car's age
		"""
		prod_date = self.car_data.get(AGE_KEY, 0)
		if prod_date == 0:
			return 0
		current_date = date.today()

		# toInt
		prod_date = prod_date.replace('.', '/')
		prod_date_arr = list(map(int, prod_date.split('/')))
		if len(prod_date_arr) == 1:
			if not self.__is_string_year(prod_date_arr[0]):
				return 0
			prod_date = date(prod_date_arr[0], 12, 1)
		elif len(prod_date_arr) >= 2:
			# 2005/03
			if self.__is_string_year(prod_date_arr[0]):
				year_string = prod_date_arr[0]
				if self.__is_string_month(prod_date_arr[1]):
					month_string = prod_date_arr[1]
				else:
					return 0
			# 03/2005
			elif self.__is_string_year(prod_date_arr[1]):
				year_string = prod_date_arr[1]
				if self.__is_string_month(prod_date_arr[0]):
					month_string = prod_date_arr[0]
				else:
					return 0
			# 25/03/2005
			elif self.__is_string_year(prod_date_arr[2]):
				year_string = prod_date_arr[2]
				if self.__is_string_month(prod_date_arr[1]):
					month_string = prod_date_arr[1]
				else:
					return 0
			else:
				return 0
			prod_date = date(year_string, month_string, 1)

		months_old = current_date.month - prod_date.month
		years_old = current_date.year - prod_date.year
		if months_old < 0 < years_old:
			months_old = 12 + months_old
			years_old = max(current_date.year - prod_date.year - 1, 0)
		price_loss = -months_old
		if years_old <= 0 and months_old <= 3:
			return price_loss
		elif years_old <= 5:
			price_loss -= 11 * years_old + 19
		elif years_old <= 30:
			price_loss -= log10(years_old - 3) * 10 + 60
		else:
			price_loss -= log10(years_old - 3) * 10 + 60 - 0.0006 * years_old ** 3
		return round(price_loss / 3)

	@staticmethod
	def __is_string_year(year_string):
		current_date = date.today()
		return 1900 <= int(year_string) <= int(current_date.year)

	@staticmethod
	def __is_string_month(month_string):
		return 1 <= int(month_string) <= 12
