from datetime import date


def is_string_year(year_string):
	current_date = date.today()
	return 1900 <= int(year_string) <= int(current_date.year)


def is_string_month(month_string):
	return 1 <= int(month_string) <= 12
