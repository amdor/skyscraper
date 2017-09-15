import requests
from bs4 import BeautifulSoup
import argparse

"""
The scraper/html parser module for the hasznaltauto.hu's car detail pages.
Usage:
	- From console: run 'python scraper_service.py url1 url2 ...'
"""
class ScraperService:

	def __init__(self, car_urls):
		self.car_urls = car_urls

	def __parse_car(self, soup):
		data = soup.find('table', class_='hirdetesadatok')
		print(data)


	def get_car_data(self):
		headers = {'User-Agent': 'Chrome/60.0.3112.113'}
		for carURL in car_urls:
			response = requests.get(carURL, headers=headers)
			car_soup = BeautifulSoup(response.content, 'lxml')
			car_features = self.__parse_car(car_soup)



if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Provide car URLs for scraping.')
	parser.add_argument('car_urls', nargs='+', metavar='URLs', help='At least one car URL is required')
	namespace = parser.parse_args()
	car_urls = namespace.car_urls

	scraper = ScraperService(car_urls)
	data = scraper.get_car_data()
