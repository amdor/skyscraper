import argparse
import re

import requests
from bs4 import BeautifulSoup

from skyscraper.comparator_service import CarComparator
from skyscraper.utils.constants import SPEEDOMETER_KEY, CAR_KEY, AGE_KEY, PRICE_KEY, POWER_KEY
from skyscraper.utils.date_helper import is_string_year, is_string_month

"""
The scraper/html parser module for the hasznaltauto.hu's car detail pages.
Usage:
	- From console: run 'python scraper_service.py url1 url2 ...'
	- As a Python class: 
		* Initialize the class with an array of strings as parameter. The array must contain the URLs
		* Optionally use a dictionary called htmls, which must contain the car_urls as keys and the corresponding
		html pages as values.
"""


class ScraperService:
	def __init__(self, car_urls=[], htmls={}):
		self.car_urls = car_urls
		self.htmls = htmls

	@staticmethod
	def __extract_result(search_result):
		return '' if not search_result else search_result[0]

	@staticmethod
	def __search_for_regex(expression, text, start_pos=0, end_pos=-1):
		search_result = re.compile(expression).search(text, start_pos, end_pos)
		# fallback
		if not search_result and start_pos > 0:
			return ScraperService.__search_for_regex(expression, text, 0, len(text)-1)
		return ScraperService.__extract_result(search_result)

	@staticmethod
	def __parse_car(soup, url):
		parsed_data = {CAR_KEY: url}
		soup_text = soup.text.replace('\xa0', ' ')
		# at first we search from the start of texts, then trying start-delta
		data_assumed_start_position = 0
		data_radius = 1000

		# our kinda fix position
		search_result = re.search('\d{1,4} ?kW', soup_text)

		print('Search result for power ' + str(search_result))
		power = ScraperService.__extract_result(search_result)
		parsed_data[POWER_KEY] = power

		if search_result:
			search_result_start = search_result.span()[0]
			data_assumed_start_position = search_result_start - data_radius if search_result_start > data_radius else 0
			data_assumed_end_position = search_result_start + data_radius
			data_assumed_end_position = data_assumed_end_position if data_assumed_end_position < len(soup_text) else -1

		# numbers delimited by dot, space or coma, find the first
		parsed_data[SPEEDOMETER_KEY] = ScraperService.__search_for_regex('((\d{1,3}[., ]?){1,3})([kK][mM])|(miles)',
												 soup_text, data_assumed_start_position, data_assumed_end_position)

		# all yyyy/mm and mm/yyyy formats are accepted (days also)
		# note: parser must check values
		date_string = ScraperService.__search_for_regex('(\d{4}([/.]\d{1,2}){1,2})|(\d{1,2}([/.]\d{1,2})?[/.]\d{4})',
												 soup_text, data_assumed_start_position, data_assumed_end_position)
		parsed_data[AGE_KEY] = date_string if ScraperService.__is_date_valid(date_string) else ''

		parsed_data[PRICE_KEY] = ScraperService.__search_for_regex(
			'((€|£|(Ft)|(HUF)) ?(\d{1,3}[., ]?){2,3})|((\d{1,3}[., ]?){2,3}(€|£|(Ft)|(HUF)))', soup_text,
			data_assumed_start_position, data_assumed_end_position)
		return parsed_data

	@staticmethod
	def __is_date_valid(date_string):
		"""
		Validates the date string
		Valid values are YYYY/MM[/*] and [DD/]MM/YYYY
		Delimiter can be . and /
		:rtype Boolean
		:return True if string is a date False otherwise
		"""
		if date_string == '':
			return False
		date_string = date_string.replace('.', '/')
		prod_date_arr = list(map(int, date_string.split('/')))
		if len(prod_date_arr) < 2:
			return False
		elif len(prod_date_arr) >= 2:
			# 2005/03
			if is_string_year(prod_date_arr[0]):
				return is_string_month(prod_date_arr[1])
			# 03/2005
			elif is_string_year(prod_date_arr[1]):
				return is_string_month(prod_date_arr[0])
			# 25/03/2005
			else:
				return len(prod_date_arr) > 2 and is_string_year(prod_date_arr[2]) and is_string_month(prod_date_arr[1])

	def get_car_data(self):
		"""
		Gets car data from the urls the service was initialized with, or uses prefetched html data
		:rtype: dict
		:return: car data in dictionary. For keys see CAR_FEATURE_KEY_MAP's values
		"""
		cars = []
		headers = {'User-Agent': 'Chrome/60.0.3112.113'}
		for car_url in self.car_urls:
			if car_url not in self.htmls:
				response = requests.get(car_url, headers=headers)
				content = str(response.content, encoding='utf-8')
			else:
				content = self.htmls[car_url]
			content = content.replace('\\xa0', ' ')
			car_soup = BeautifulSoup(content, 'lxml')
			cars.append(ScraperService.__parse_car(car_soup, car_url))
		return cars


class ScraperServiceFactory:
	def __init__(self):
		pass

	@staticmethod
	def get_for_lists(url_list, content_list) -> ScraperService:
		"""
		Constructs a new Scraper sercice from two lists
		:param url_list: list of urls
		:param content_list: list of html pages in same order as in url list
		:return: new ScraperService instance with the given content
		"""
		htmls = {url_list[i]: content_list[i] for i in range(len(url_list))}
		return ScraperService(url_list, htmls)

	@staticmethod
	def get_for_dict(htmls: dict) -> ScraperService:
		"""
		Convenience method for ScraperService creation
		:param htmls: dictionary where the keys are urls and the values are the html contents of the urls
		:return: a ScraperService of the given data
		"""
		return ScraperService([*htmls], htmls)

	@staticmethod
	def get_for_list_and_dict(url_list: list, htmls: dict) -> ScraperService:
		"""
		Convenience method for ScraperService creation. Urls might be different from urls in htmls' keys
		:param url_list: list of urls
		:param htmls: dictionary where the keys are urls and the values are the html contents of the urls
		:return: a ScraperService of the given data
		"""
		complete_url_list = list({*htmls} | set(url_list))
		return ScraperService(complete_url_list, htmls)


def main():
	parser = argparse.ArgumentParser(description='Provide car URLs for scraping.')
	parser.add_argument('car_urls', nargs='+', metavar='URLs', help='At least one car URL is required')
	namespace = parser.parse_args()
	car_urls = namespace.car_urls

	scraper = ScraperService(car_urls)
	data = scraper.get_car_data()
	CarComparator.compare_cars(data)
	for car in data:
		print(car['CarUri'])
		print(car['worth'])

	if __name__ == "__main__":
		main()
