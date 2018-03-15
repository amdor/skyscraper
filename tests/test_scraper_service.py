import os
import unittest

from skyscraper.scraper_service import ScraperServiceFactory
from skyscraper.utils.constants import SPEEDOMETER_KEY, AGE_KEY, CAR_KEY, PRICE_KEY, POWER_KEY
from common_test_utils import gather_extension_files, VALIDATION_DATA


class TestScraping(unittest.TestCase):
	files_under_test = set()

	@classmethod
	def setUpClass(cls):
		path = os.path.dirname(os.path.realpath(__file__))
		cls.files_under_test = gather_extension_files(path)

	def test_scraping(self):
		for file_name in [*VALIDATION_DATA]:
			abs_path = list(filter(lambda test_file: test_file.endswith(file_name), self.files_under_test))[0]
			with open(abs_path, 'rb') as html_file:
				file_content = html_file.read()
				scraper = ScraperServiceFactory.get_for_dict({file_name: file_content})
				car_data = scraper.get_car_data()
				actual_value = car_data[0]
				expected_value = VALIDATION_DATA[file_name]
				print(actual_value[CAR_KEY] + ' assertions')
				self.assertEqual(expected_value[SPEEDOMETER_KEY], actual_value[SPEEDOMETER_KEY])
				self.assertEqual(expected_value[AGE_KEY], actual_value[AGE_KEY])
				self.assertEqual(expected_value[PRICE_KEY], actual_value[PRICE_KEY])
				self.assertEqual(expected_value[POWER_KEY], actual_value[POWER_KEY])
