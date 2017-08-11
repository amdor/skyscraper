from services.constants import POWER_KEY,CONDITION_KEY, Conditions


def __get_first_number(value):
	return [int(s) for s in value.split() if s.isdigit()][0]


def get_power(car_data):
	"""
	Parses the the horsepower value of the car from the HTML text
	representation
	:param car_data: the text representation e.g. '62 LE'
	:return: the value e.g. 62 or null if power is not present
	"""
	return __get_first_number(car_data.get(POWER_KEY, '0'))


def get_condition(car_data):
	condition_text = car_data.get(CONDITION_KEY,'')
	if condition_text == Conditions.COMMON.value \
		or condition_text == Conditions.EXCELLENT.value \
		or condition_text == Conditions.UNDAMAGED.value \
		or condition_text == Conditions.PRESERVED.value \
		or condition_text == Conditions.NOVEL.value:
		return 0
	else:
		return -20
