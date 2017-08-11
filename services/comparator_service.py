# -*- coding: utf-8 -*-
import logging
from services.constants import CAR_KEY, WORTH_KEY
from services.value_parser import get_power, get_condition


def get_car_value(car_data):
	"""
	This function enumerates through parameters of given car's primary parameters
	and generates their worth from them.
	Orders the values descendingly, returns the ordered array, in which each element has a Name and Value property
	"""
	power = get_power(car_data)

	condition = get_condition(car_data)

	car_worth = power / 14 + condition
	return car_worth


def compare_cars(cars_data):
	"""
	This should be the entry point of this library
	Requires a data dictionary, where only 'CarUri' is mandatory key
	all the keys are optional see all accepted keys at the constants library,
	or the docs.
	Modifies input parameter structure: adds a "worth" key to it
	"""
	for car_data in cars_data:
		if CAR_KEY in car_data:
			logging.debug('Getting value of %s (analyzing data)', CAR_KEY)
			car_data[WORTH_KEY] = get_car_value(car_data)
