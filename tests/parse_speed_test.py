from os import listdir
from bs4 import BeautifulSoup
from services.scraper_service import ScraperService

DIR_NAME = './resources/html/'

def parse_html():
	files = listdir(DIR_NAME)
	car_data = []
	for file in files:
		with open(DIR_NAME + file) as fp:
			car_soup = BeautifulSoup(fp, 'lxml')
			car_data.append(ScraperService.parse_car(car_soup, file))
	print(car_data)


parse_html()