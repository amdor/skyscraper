# -*- coding: utf-8 -*-
import logging

from skyscraper.utils.constants import CAR_KEY, WORTH_KEY
from skyscraper.utils.value_parser import ValueParser


class CarComparator:
	@staticmethod
	def __get_car_value(car_data):
		"""
		This function enumerates through parameters of given car's primary parameters
		and generates their worth from them.
		Orders the values to descending, returns the ordered array, in which each element has a Name and Value property
		"""
		value_parser = ValueParser(car_data)
		car_worth = value_parser.get_power_value()
		car_worth += value_parser.get_condition_value()
		car_worth += value_parser.get_trunk_value()
		car_worth += value_parser.get_mass_value()
		car_worth += value_parser.get_speedometer_value()
		car_worth += value_parser.get_price_value()
		car_worth += value_parser.get_age_value()

		return round(car_worth, 2) + 30

	@staticmethod
	def compare_cars(cars_data):
		"""
		This should be the entry point of this library
		Requires a data dictionary, where only 'CarUri' is mandatory key
		all the keys are optional see all accepted keys at the constants library,
		or the docs.
		Modifies input parameter structure: adds a "worth" key to it
		:rtype: list
		:param cars_data: list of cars with appropriate features
		:return: cars_data
		"""
		for car_data in cars_data:
			if CAR_KEY in car_data:
				logging.debug('Getting value of %s (analyzing data)', CAR_KEY)
				car_data[WORTH_KEY] = CarComparator.__get_car_value(car_data)
		return cars_data
