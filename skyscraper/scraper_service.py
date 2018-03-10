import argparse
import re
import requests
from bs4 import BeautifulSoup

from skyscraper.comparator_service import CarComparator

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
	def __init__(self, car_urls=[], htmls = {}):
		self.car_urls = car_urls
		self.htmls = htmls

	@staticmethod
	def __parse_car(soup, url):
		mileage = soup.find(text=re.compile('^((\d{1,3}[\.| |,]?){1,3})km|miles$'))
		return mileage

	def get_car_data(self):
		"""
		Gets car data from the urls the service was initialized with, or uses prefetched html data
		:rtype: dict
		:return: car data in dictionary. For keys see CAR_FEATURE_KEY_MAP's values
		"""
		car_data = []
		headers = {'User-Agent': 'Chrome/60.0.3112.113'}
		for car_url in self.car_urls:
			if car_url not in self.htmls:
				response = requests.get(car_url, headers=headers)
				content = response.content
			else:
				content = str(self.htmls[car_url], encoding='utf-8')
			content = content.replace('\xa0', ' ')
			car_soup = BeautifulSoup(content, 'lxml')
			car_data.append(ScraperService.__parse_car(car_soup, car_url))
		return car_data


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
		htmls = {url_list[i]:content_list[i] for i in range(len(url_list))}
		return ScraperService(url_list, htmls)

	@staticmethod
	def get_for_dict(htmls: dict) -> ScraperService:
		"""
		Convenience method for ScraperService creation
		:param htmls: dictionary where the keys are urls and the values are the html contents of the urls
		:return: a ScraperService of the given data
		"""
		return ScraperService([*htmls], htmls)


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
