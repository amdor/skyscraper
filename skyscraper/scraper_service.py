import argparse
import re

import requests
import unicodedata
from bs4 import BeautifulSoup

from skyscraper.comparator_service import CarComparator
from skyscraper.utils.constants import SPEEDOMETER_KEY, CAR_KEY, AGE_KEY, PRICE_KEY, POWER_KEY

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
	def __parse_car(soup, url):
		parsed_data = {CAR_KEY: url}
		soup_text = soup.text.replace('\xa0', ' ')
		print('Soup text is ' + soup_text)

		# numbers delimited by dot, space or coma, find the first
		search_result = re.search('((\d{1,3}[., ]?){1,3})km|miles', soup_text)
		print('Search result for miles ' + search_result)
		mileage = ScraperService.__extract_result(search_result)
		parsed_data[SPEEDOMETER_KEY] = mileage

		# all yyyy/mm and mm/yyyy formats are accepted (days also)
		# note: parser must check values
		search_result = re.search('(\d{4}(/\d{1,2}){1,2})|(\d{1,2}(/\d{1,2})?/\d{4})', soup_text)
		print('Search result for prod_date ' + search_result)
		prod_date = ScraperService.__extract_result(search_result)
		parsed_data[AGE_KEY] = prod_date

		search_result = re.search('((€|£|(Ft)) ?(\d{1,3}[., ]?){1,3})|((\d{1,3}[., ]?){1,3}(€|£|(Ft)))', soup_text)
		print('Search result for price ' + search_result)
		price = ScraperService.__extract_result(search_result)
		parsed_data[PRICE_KEY] = price

		search_result = re.search('\d{1,4} ?kW', soup_text)
		print('Search result for power ' + search_result)
		power = ScraperService.__extract_result(search_result)
		# get only the kW part
		parsed_data[POWER_KEY] = power
		return parsed_data

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
