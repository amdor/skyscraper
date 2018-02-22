import requests
from bs4 import BeautifulSoup
import argparse
from skyscraper.utils.constants import CAR_KEY, CAR_FEATURE_KEY_MAP
from skyscraper.comparator_service import CarComparator

"""
The scraper/html parser module for the hasznaltauto.hu's car detail pages.
Usage:
	- From console: run 'python scraper_service.py url1 url2 ...'
	- As a Python class: initialize the class with an array of strings as parameter. The array must contain the URLs
"""


class ScraperService:
	def __init__(self, car_urls=[]):
		self.car_urls = car_urls

	@staticmethod
	def __table_to_dictionary(table_tag) -> dict:
		"""
		Turns a two column beautiful soup Tag table into a dictionary by taking the first
		column (of every row) as key and the second as value
		:rtype: dict
		:param table_tag: the table to process
		"""
		rows = {}
		for row in table_tag.findAll('tr'):
			columns = row.findAll('td')
			if len(columns) == 2:
				# Removes every unneeded characters that might pop up + whitespaces
				rows[columns[0].text.strip().strip(":-")] = columns[1].text.strip().replace(u'\xa0', u' ')
		return rows

	@staticmethod
	def __build_car_data(raw_data, car_url) -> dict:
		car_data = {CAR_KEY: car_url}
		for feature_key, feature_value in raw_data.items():
			if feature_key in CAR_FEATURE_KEY_MAP:
				data_key = CAR_FEATURE_KEY_MAP[feature_key]
				car_data[data_key] = feature_value
		return car_data

	@staticmethod
	def __parse_car(soup, url):
		table = soup.find('table', class_='hirdetesadatok')
		table_dict = ScraperService.__table_to_dictionary(table)
		return ScraperService.__build_car_data(table_dict, url)

	def get_car_data(self, html = ''):
		"""
		Gets car data from the initialized urls
		:rtype: dict
		:return: car data in dictionary. For keys see CAR_FEATURE_KEY_MAP's values
		"""
		car_data = []
		if html:
			car_soup = BeautifulSoup(html, 'lxml')
			car_data.append(ScraperService.__parse_car(car_soup, self.car_urls[0]))
			return car_data
		headers = {'User-Agent': 'Chrome/60.0.3112.113'}
		for car_url in self.car_urls:
			response = requests.get(car_url, headers=headers)
			car_soup = BeautifulSoup(response.content, 'lxml')
			car_data.append(ScraperService.__parse_car(car_soup, car_url))
		return car_data


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
