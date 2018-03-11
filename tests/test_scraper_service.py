import os
import unittest

from skyscraper.scraper_service import ScraperServiceFactory
from skyscraper.utils.constants import SPEEDOMETER_KEY

VALIDATION_DATA = {
	'bmw_530xd_automata-12119695.html': {
		SPEEDOMETER_KEY: '98 100 km'
	},
	'audi_a4_avant.html': {
		SPEEDOMETER_KEY: '56,488 km'
	}
}


def gather_extension_files(root):
	"""
	Traverses through all subdirectories of root collecting *.js filenames. Recursive.
	:param root: the basepoint of search
	:rtype: set
	:return: all found js filenames
	"""
	extension_files = set()
	for child in os.listdir(root):
		abs_path = os.path.join(root, child)
		if os.path.isdir(abs_path):
			extension_files |= gather_extension_files(abs_path)
		elif child.endswith(".html"):
			extension_files.add(abs_path)
	return extension_files


class TestBasicPaths(unittest.TestCase):
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
				self.assertEqual(VALIDATION_DATA[file_name][SPEEDOMETER_KEY], car_data[0][SPEEDOMETER_KEY])
